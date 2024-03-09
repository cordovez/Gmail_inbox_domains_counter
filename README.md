# Gmail_inbox_domains_counter
Script to count how many emails from a given sender are in my inbox ... in order to get maximum satisfaction from a purge of emails. 🤓

## To use
Clone me: `git@github.com:cordovez/Gmail_inbox_domains_counter.git`

To use the script, you must have a Gmail address (obviously), and a Google Developer account from whence you can get an API Key and set up the OAuth. The result is a json document that you must download into the root folder of the project you've just cloned. [This is they Python guide for this process](https://developers.google.com/gmail/api/quickstart/python).

make sure you create a virtual env and activate it before pip installing the Google library as indicated in their instructions

The first time you run the file `python count_emails.py` it will guide you through the authorization process.

Attention, this can be a slow function to run. My inbox contained 1841 emails and that takes: 7 minutes and 39 seconds to process. 

Running the script writes a file called `domain_count.json` and prints a terminal message that looks like this:
```
File has been created
1635  where in the inbox
Execution time: 7 minutes 16 seconds
```

If you intend to save your copy of the script to github, make sure you to git ignore your credentials.json, token.json, and domain_count.json (the file will have the email of every sender in your inbox).

To manipulate and change the type of data you get in return, see [Gmail api reference.](https://developers.google.com/gmail/api/reference/rest/v1/users.messages)



