#!/usr/bin/python

import pymsteams
import sys


WEBHOOK_URL = ""


def push_msg(*args):

    # You must create the connector card object with the Microsoft Webhook URL
    team_msg = pymsteams.connectorcard(WEBHOOK_URL)

    # Add text to the message.
    team_msg.text(args[0][1])
    if len(args[0]) > 2:
        team_msg.title(args[0][2])

    # send the message.
    team_msg.send()


if __name__ == "__main__":
    print('args:', str(sys.argv))
    push_msg(sys.argv)