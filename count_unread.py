import os.path
from pprint import pprint
from collections import OrderedDict
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import time
import json
import re

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]


def establish_credentials():
    """Establish credentials and Call the GMAIL API"""
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    return creds


def define_gmail_service(creds):
    return build("gmail", "v1", credentials=creds)


def save_to_file(data):
    with open("unread_count.json", "w") as document:
        json.dump(data, document)


def extract_domain(sender: str) -> str:
    # sourcery skip: assign-if-exp, inline-immediately-returned-variable, use-named-expression
    match = re.search(r"<([^>]+)>", sender)
    if match:
        domain = match[1]
        return domain
    else:
        return ""


# def extract_domain(sender: str) -> str:
#     _, domain = sender.split("@", 1)
#     return f"@{domain}"


def get_message_ids(service) -> list:
    try:
        # Initialize the page token to None
        page_token = None
        messages = []
        while True:
            # Request a page of messages
            results = (
                service.users()
                .messages()
                .list(userId="me", labelIds=["UNREAD"], pageToken=page_token)
                .execute()
            )
            messages.extend(results.get("messages", []))

            # Get the next page token
            page_token = results.get("nextPageToken")

            # Break the loop if there are no more pages
            if not page_token:
                break

        return messages

    except HttpError as error:
        # TODO(developer) - Handle errors from Gmail API.
        print(f"An error occurred: {error}")


def count_domain_messages(messages, service):
    domains_count = {}

    for message in messages:
        # Get the sender from each message
        result = service.users().messages().get(userId="me", id=message["id"]).execute()

        if sender_info := next(
            (
                header
                for header in result["payload"]["headers"]
                if header["name"] == "From"
            ),
            None,
        ):

            sender = sender_info["value"]
            domain = extract_domain(sender)
            domains_count[domain.rstrip(">")] = domains_count.get(domain, 0) + 1

    return OrderedDict(sorted(domains_count.items(), key=lambda x: x[1], reverse=True))


def main():
    """
    Lists the user's email domains for items in the inbox, with the respective count.
    """
    credentials = establish_credentials()
    service = define_gmail_service(credentials)

    messages = get_message_ids(service)
    final_count = count_domain_messages(messages, service)

    save_to_file(final_count)

    print("File has been created")
    print(f"{len(messages)}  where in the inbox")
    # result = (
    #     service.users().messages().get(userId="me", id="18e1a0802be94aac").execute()
    # )
    # pprint(result)


if __name__ == "__main__":
    start_time = time.time()
    main()
    end_time = time.time()
    execution_time = end_time - start_time
    minutes = int(execution_time // 60)  # Get the whole number of minutes
    seconds = int(execution_time % 60)  # Get the remaining seconds

    print(f"Execution time: {minutes} minutes {seconds} seconds")
