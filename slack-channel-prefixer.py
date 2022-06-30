# Tim Barnes
# v1.0
# 2022-06-30
#
# Get a list of public slack channels in a Workspace and append a prefix to each.
# An administrator must first create the app, give it proper permissions
# on slack's servers, and install it to the workspace in order to generate
# the correct auth token needed for this script to connect to the api

import logging
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

logger = logging.getLogger(__name__)
token_prompt = "Enter your user auth token: "
prefix_prompt = "Enter the desired channel prefix: "

def get_user_input(prompt):
    return input(prompt)


def create_client(token):
    return WebClient(token)


def get_channel_list(client):
    try:
        result = client.conversations_list()
        return result["channels"]

    except SlackApiError as e:
        logger.error("Error fetching list of channels: {}".format(e))
        exit()



def prefix_channels(client, channel_list, channel_prefix):
    for channel in channel_list:
        channel_id = channel["id"]
        channel_name = channel["name"]
        new_name = channel_prefix + channel_name
        print(f"Adding {channel_prefix} to {channel_name}")
        try:
            client.conversations_rename(channel=channel_id, name=new_name)
            print(f"{channel_name} prefixed successfully\n")

        except SlackApiError as e:
            logger.error("Error prefixing {channel_name}: {}".format(e))
            exit()

def main():
    user_auth_token = get_user_input(token_prompt)
    client = create_client(user_auth_token)
    channel_list = get_channel_list(client)
    channel_prefix = get_user_input(prefix_prompt)
    prefix_channels(client, channel_list, channel_prefix)

main()