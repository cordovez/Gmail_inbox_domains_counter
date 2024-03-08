import os.path
from pprint import pprint
from collections import OrderedDict
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import timeit

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

domains_count = {}


def extract_domain(sender: str) -> str:
    _, domain = sender.split("@", 1)
    return f"@{domain}"


def get_senders(creds) -> list:
    senders = []
    try:
        # Call the Gmail API
        service = build("gmail", "v1", credentials=creds)

        # Initialize the page token to None
        page_token = None

        while True:
            # Request a page of messages
            results = (
                service.users()
                .messages()
                .list(userId="me", pageToken=page_token)
                .execute()
            )
            messages = results.get("messages", [])

            if not messages:
                print("No more messages found.")
                break

            for message in messages:
                # Get the sender from each message
                result = (
                    service.users()
                    .messages()
                    .get(userId="me", id=message["id"])
                    .execute()
                )
                if "INBOX" in result["labelIds"]:
                    # Find the 'From' header and extract the sender
                    sender_info = next(
                        (
                            header
                            for header in result["payload"]["headers"]
                            if header["name"] == "From"
                        ),
                        None,
                    )
                    if sender_info:
                        sender = sender_info["value"]
                        domain = extract_domain(sender)
                        senders.append(domain)
                        domains_count[domain.rstrip(">")] = (
                            domains_count.get(domain, 0) + 1
                        )

            # Get the next page token
            page_token = results.get("nextPageToken")

            # Break the loop if there are no more pages
            if not page_token:
                break

        sorted_domains_count = OrderedDict(
            sorted(domains_count.items(), key=lambda x: x[1], reverse=True)
        )
        return sorted_domains_count

    except HttpError as error:
        # TODO(developer) - Handle errors from Gmail API.
        print(f"An error occurred: {error}")


def main():
    """
    Lists the user's email domains for items in the inbox, with the respective count.
    """
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

    senders = get_senders(creds)
    with open("token.json", "w") as token:
            token.∏rite(creds.to_json())
            
            
    execution_time = timeit.timeit(
        stmt="get_senders(creds)",  # Function call to be timed
        setup="from __main__ import get_senders, creds",  # Import necessary functions and variables
        number=1,  # Execute the statement once
    )
    print(f"Execution time: {execution_time} seconds")
    pprint(senders)


if __name__ == "__main__":
    main()
