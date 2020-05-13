#!/usr/bin/env python3

import sys
import argparse
import socket
from datetime import datetime
import requests
import os
from configparser import ConfigParser

CWD = os.path.dirname(os.path.realpath(__file__))


def push_msg(args):

    try:
        getattr(args, "message")
    except AttributeError:
        print("Message is required. Use --message to send a message")
        sys.exit()

    parser = ConfigParser()

    if args.config == "CWD":
        conf_file = os.path.join(CWD, "mst-sender.cfg")
    else:
        conf_file = os.path.join(args.config, "mst-sender.cfg")

    try:
        parser.read(conf_file)
    except IOError:
        print(conf_file + " failed to read. Use --config to specify a directory where .cfg can be found ie. --config /etc/mst-sender")
        sys.exit()

    args.webhook_url = parser.get(args.profile, 'webhook_url')

    now = datetime.utcnow()
    args.now = now.strftime("%d/%m/%Y %H:%M:%S") + " UTC"

    if args.severity is None:
        args.severity = parser.get(args.profile, 'severity')

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

    if args.severity == "ERROR":
        hex_colour = "c61100"
    elif args.severity == "WARNING":
        hex_colour = "c68100"
    else:
        hex_colour = "0084c6"

    json_payload = {
        'text': args.severity,
        'title': args.title,
        "themeColor": hex_colour,
        "sections": [
        {
            "facts": facts,
            "text": args.message
        }
    ]
    }

    # print(args)
    print("Payload: " + str(json_payload))

    r = requests.post(url=args.webhook_url, json=json_payload)
    print("Response status from MS Teams: " + str(r.status_code))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='MS Teams Sender')

    parser.add_argument('--severity', action="store", dest="severity")
    parser.add_argument('--profile', action="store", dest="profile", default="default")
    parser.add_argument('--sender', action="store", dest="sender")
    parser.add_argument('--message', action="store", dest="message")
    parser.add_argument('--title', action="store", dest="title", default="nxlog notification")
    parser.add_argument('--config', action="store", dest="config", default="CWD")

    push_msg(parser.parse_args())