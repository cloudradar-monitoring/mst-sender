#!/usr/bin/python

import sys
import argparse
import socket
from datetime import datetime
import requests
import os
from ConfigParser import SafeConfigParser
import logging
import logging.config

CWD = os.path.dirname(os.path.realpath(__file__))

LOGGING_CONFIG = {
    'formatters': {
        'brief': {
            'format': '[%(asctime)s][%(levelname)s] %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'brief'
        },
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(CWD, "mst-sender.log"),
            'formatter': 'brief',
            'mode': 'a',
            'maxBytes': 1048576,
            'backupCount': 10
        },
    },
    'loggers': {
        'main': {
            'propagate': False,
            'handlers': ['console', 'file'],
            'level': 'INFO'
        }
    },
    'version': 1
}


def push_msg(args):

    parser = SafeConfigParser()
    conf_file = os.path.join(CWD, "mst-sender.cfg")

    with open(conf_file, "r") as fh:
        parser.readfp(fh)

    try:
        LOGGING_CONFIG['handlers']['file']['filename'] = os.path.join(parser.get(args.profile, 'logs'), 'mst-sender.log')
    except:
        pass

    logging.config.dictConfig(LOGGING_CONFIG)
    logger = logging.getLogger('main')

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

    logger.info(args)
    logger.info(json_payload)

    r = requests.post(url=args.webhook_url, json=json_payload)
    logger.info(r.status_code)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='MS Teams Sender')

    parser.add_argument('--log_level', action="store", dest="log_level")
    parser.add_argument('--profile', action="store", dest="profile", default="default")
    parser.add_argument('--sender', action="store", dest="sender")
    parser.add_argument('--message', action="store", dest="message")
    parser.add_argument('--title', action="store", dest="title", default="nxlog notification")

    push_msg(parser.parse_args())