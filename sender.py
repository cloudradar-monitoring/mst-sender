#!/usr/bin/python

import pymsteams
import sys
import argparse
import socket
from datetime import datetime
import requests


WEBHOOK_URL = "https://outlook.office.com/webhook/ff7a3383-c45e-4c7b-b7e1-2fdfd3e74e1b@c5f4d5ac-668c-41fc" \
                  "-b829-8c33e71aca58/IncomingWebhook/a02e939cba9b4de1bdcfa4f457f38135/249b239f-f979-4a2a-82db-2eeb7e36a241"


def push_msg(args):

    host_name = socket.gethostname()
    now = datetime.now()
    now_strf = now.strftime("%d/%m/%Y %H:%M:%S")

    if args.log_level == "ERROR":
        hex_colour = "c61100"
    elif args.log_level == "WARNING":
        hex_colour = "c68100"
    else:
        hex_colour = "0084c6"

    json_payload = {
        'text': args.log_level,
        'title': args.title,
        "themeColor": hex_colour,
        "sections": [
        {
            "facts": [
                {
                    "name": "Posted By:",
                    "value": host_name
                },
                {
                    "name": "Posted At:",
                    "value": now_strf
                }
            ],
            "text": args.message
        }
    ]
    }
    requests.post(url=WEBHOOK_URL, json=json_payload)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='MS Teams Sender')

    parser.add_argument('--log_level', action="store", dest="log_level", default="ERROR")
    parser.add_argument('--message', action="store", dest="message")
    parser.add_argument('--title', action="store", dest="title", default="nxlog notification")

    print(parser.parse_args())

    push_msg(parser.parse_args())