# Tim Barnes
# v1.0
# 2022-06-30
#
# Get a list of public slack channels in a Workspace
# and update the topic and description of each.
# An administrator must first create the app, give it proper permissions
# on slack's servers, and install it to the workspace in order to generate
# the correct auth token needed for this script to connect to the api

import logging
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

logger = logging.getLogger(__name__)
control_prompt = "Do you want to edit this channel, skip it, or exit? (e/s/x): "
token_prompt = "Enter your user auth token: "
topic_prompt = "What do you want to add to the topic? "
purpose_prompt = "What do you want to add to the description? "

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



def update_topic_purpose(client, channel_list):
    for channel in channel_list:
        while(True):
            print(f"The channel {channel['name']} is currently selected")
            decision = get_user_input(control_prompt)
            if(decision == "s"):
                break
            elif(decision == "x"):
                exit()
            elif(decision == "e"):
                channel_id = channel["id"]
                old_topic = channel["topic"]["value"]
                old_purpose = channel["purpose"]["value"]
                topic_add = get_user_input(topic_prompt)
                purpose_add = get_user_input(purpose_prompt)
                new_topic = topic_add + "\n" + old_topic
                new_purpose = purpose_add + "\n" + old_purpose
                print(f"Adding {topic_add} to the channel topic")
                try:
                    client.conversations_setTopic(channel=channel_id, topic=new_topic)
                    print("Topic updated successfully\n")

                except SlackApiError as e:
                    logger.error("Error updating {channel_name}'s topic: {}".format(e))
                    exit()

                print(f"Adding {purpose_add} to the channel description")
                try:
                    client.conversations_setPurpose(channel=channel_id, purpose=new_purpose)
                    print("Description updated successfully\n")

                except SlackApiError as e:
                    logger.error("Error updating {channel_name}'s description: {}".format(e))
                    exit()
            else:
                print("Invalid input, choose edit (e), skip (s), or exit (x)")


def main():
    user_auth_token = get_user_input(token_prompt)
    client = create_client(user_auth_token)
    channel_list = get_channel_list(client)
    update_topic_purpose(client, channel_list)

main()