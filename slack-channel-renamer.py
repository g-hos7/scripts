# Tim Barnes
# v1.0
# 2022-06-30
#
# Use Slack's API to get a list of channels in a Workspace and append a
# prefix to them.
# An administrator must first create the app and give it proper permissions
# on slack's servers in order to generate the correct auth token
# needed for this script to connect to the api

from slack_sdk import WebClient

USER_AUTH_TOKEN = ""
channel_prefix = ""

def connect_to_api(token):
    return WebClient(token)

def get_channel_list(api_connection):
    result = api_connection.conversations_list()
    return result["channels"]

def channel_rename(api_connection, channel_list, channel_prefix):
    for channel in channel_list:
        channel_id = channel["id"]
        channel_name = channel["name"]
        new_name = channel_prefix + channel_name
        api_connection.conversations_rename(channel=channel_id, name=new_name)


api_connection = connect_to_api(USER_AUTH_TOKEN)

channel_list = get_channel_list(api_connection)

channel_rename(api_connection, channel_list, channel_prefix)
