#!/usr/bin/python

import sys
import argparse
import socket
from datetime import datetime
import requests
import os
from ConfigParser import SafeConfigParser


def push_msg(args):

    parser = SafeConfigParser()

    with open(os.path.join(os.getcwd(), "mst-sender.cfg"), "r") as fh:
        parser.readfp(fh)

    args.webhook_url = parser.get(args.profile, 'webhook_url')

    now = datetime.utcnow()
    args.now = now.strftime("%d/%m/%Y %H:%M:%S") + " UTC"

    if args.log_level is None:
        args.log_level = parser.get(args.profile, 'log_level')

    if args.sender is None:
        try:
            args.sender = parser.get(args.profile, 'sender')
        except:
            args.sender = socket.gethostname()

    # config facts
    facts = []
    items = parser.items(args.profile)
    for item in items:
        if item[0].count("fact"):
            facts.append({
                    "name": item[0].split(".")[1],
                    "value": item[1]
                })

    # default facts
    facts.append({
                    "name": "Posted By:",
                    "value": args.sender
                })

    facts.append({
                    "name": "Posted At:",
                    "value": args.now
                })

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
            "facts": facts,
            "text": args.message
        }
    ]
    }

    print(args)

    r = requests.post(url=args.webhook_url, json=json_payload)
    print(r.status_code)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='MS Teams Sender')

    parser.add_argument('--log_level', action="store", dest="log_level")
    parser.add_argument('--profile', action="store", dest="profile", default="default")
    parser.add_argument('--sender', action="store", dest="sender")
    parser.add_argument('--message', action="store", dest="message")
    parser.add_argument('--title', action="store", dest="title", default="nxlog notification")

    print(parser.parse_args())

    push_msg(parser.parse_args())