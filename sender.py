#!/usr/bin/python

import sys
import argparse
import socket
from datetime import datetime
import requests


def push_msg(args):

    with open("webhookurl.conf", "r") as fh:
        webhook_url = fh.read()

    print("webhook_url: " + webhook_url)

    host_name = socket.gethostname()
    now = datetime.utcnow()
    now_strf = now.strftime("%d/%m/%Y %H:%M:%S") + " UTC"

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
    requests.post(url=webhook_url, json=json_payload)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='MS Teams Sender')

    parser.add_argument('--log_level', action="store", dest="log_level", default="ERROR")
    parser.add_argument('--message', action="store", dest="message")
    parser.add_argument('--title', action="store", dest="title", default="nxlog notification")

    print(parser.parse_args())

    push_msg(parser.parse_args())