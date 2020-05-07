#!/usr/bin/python

import pymsteams
import sys


WEBHOOK_URL = "https://outlook.office.com/webhook/ff7a3383-c45e-4c7b-b7e1-2fdfd3e74e1b@c5f4d5ac-668c-41fc" \
                  "-b829-8c33e71aca58/IncomingWebhook/a02e939cba9b4de1bdcfa4f457f38135/249b239f-f979-4a2a-82db-2eeb7e36a241"


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