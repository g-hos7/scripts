# Tim Barnes
# v1.4
# 2022-07-04
#
# Get a list of public slack channels in a Workspace.
# Choose to add a prefix to some or all channels.
# An administrator must first create the app, give it proper permissions
# on slack's servers, and install it to the workspace in order to generate
# the correct auth token needed for this script to connect to the api.

import logging
import re
import time
from webbrowser import get
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

logger = logging.getLogger(__name__)
token_prompt = "Enter your user auth token: "
prefix_prompt = "Enter the desired channel prefix (a hyphen will be added automatically): "
channel_list_limit = 1000

def get_user_input(prompt):
    return input(prompt)


def display_channels(list):
    for item in list:
        print(item["name"])


def name_check(prefix, name):
    pattern = r'(^|[^\w]){}([^\w]|$)'.format(prefix)
    pattern = re.compile(pattern, re.IGNORECASE)
    matches = re.search(pattern, name)
    return bool(matches)


def create_client(token):
    return WebClient(token)


def get_channel_list(client):
    try:
        result = client.conversations_list(channel_list_limit)
        return result["channels"]

    except SlackApiError as e:
        logger.error("Error fetching list of channels: {}".format(e))
        exit()


def prefix_channels(client, channel_list):
    channel_prefix = get_user_input(prefix_prompt)
    rate_counter = 0

    while(True):
        choice = get_user_input("Enter a positive integer to prefix some channels, a to prefix all, or x to go back: ")
        if(choice == "a"):
            for channel in channel_list:
                channel_id = channel["id"]
                channel_name = channel["name"]

                if(name_check(channel_prefix, channel_name) == True):
                    print(f"Prefix deteceted in {channel_name}, skipping")
                    continue

                else:
                    if(rate_counter == 20):
                        print("Pausing for 65 seconds due to rate limiting")
                        time.sleep(65)
                        rate_counter = 0
                        print("Resuming execution")

                    new_name = channel_prefix + "-" + channel_name
                    print(f"Adding {channel_prefix} to {channel_name}")
                    try:
                        client.conversations_rename(channel=channel_id, name=new_name)
                        print(f"{channel_name} prefixed successfully\n")
                        rate_counter += 1
    
                    except SlackApiError as e:
                        logger.error("Error prefixing {channel_name}: {}".format(e))
                        exit()

        elif(choice.isnumeric()):
            ceiling = int(choice)
            counter = 0

            for channel in channel_list:
                if(counter == ceiling):
                    break

                else:
                    channel_id = channel["id"]
                    channel_name = channel["name"]
                    if(name_check(channel_prefix, channel_name) == True):
                        continue

                    else:
                        new_name = channel_prefix + "-" + channel_name
                        print(f"Adding {channel_prefix} to {channel_name}")
                        try:
                            client.conversations_rename(channel=channel_id, name=new_name)
                            print(f"{channel_name} prefixed successfully\n")
                            counter += 1

                        except SlackApiError as e:
                            logger.error("Error prefixing {channel_name}: {}".format(e))
                            exit()

        elif(choice == "x"):
            break

        else:
            print("Invalid input, enter a positive integer, a, or x")

def main():
    user_auth_token = get_user_input(token_prompt)
    client = create_client(user_auth_token)
    channel_list = get_channel_list(client)

    while(True):
        control = get_user_input("List channels, prefix them, or exit? (l/p/x): ")
        if(control == "l"):
            display_channels(channel_list)
        elif(control == "p"):
            prefix_channels(client, channel_list)
        elif(control == "x"):
            exit()
        else:
            print("Invalid selection, choose l, p, or x")

main()