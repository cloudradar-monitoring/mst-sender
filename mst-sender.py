#!/usr/bin/env python3

import sys
import argparse
import socket
from datetime import datetime
import requests
import os
from configparser import ConfigParser
from os import path
import json
import fileinput
import re
from html import escape

CWD = os.path.dirname(os.path.realpath(__file__))


class MstSender:
    args = None
    webhook_url = None
    facts = []
    hex_colour = "0084c6"
    title = ''
    severity = ''
    debug = False
    message_facts_re = re.compile('\[(.*?)=(.*?)\]', re.IGNORECASE)

    def __init__(self, args):
        self.config = args
        parser = ConfigParser()

        if args.config is None:
            conf_file = None
            file_list = [os.path.join(CWD, "mst-sender.cfg"), '/etc/mst-sender/mst-sender.cfg', '/etc/mst-sender.cfg', '~/.mst-sender.cfg']
            for try_file in file_list:
                if path.exists(try_file):
                    conf_file = try_file
                    break
            if conf_file is None:
                sys.stderr.write("No config file mst-sender.cfg found in {}.\n".format(', '.join(file_list)))
                sys.exit(1)
        else:
            conf_file = args.config

        try:
            parser.read(conf_file)
        except IOError:
            print(conf_file + " failed to read. Use --config to specify a directory where .cfg can be found ie. --config /etc/mst-sender")
            sys.exit()

        args.webhook_url = parser.get(args.profile, 'webhook_url')

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

        self.facts = facts

        if args.severity == "ERROR":
            self.hex_colour = "c61100"
        elif args.severity == "WARNING":
            self.hex_colour = "c68100"
        else:
            self.hex_colour = "0084c6"

        self.title = args.title
        self.severity = args.severity
        self.debug = args.debug
        self.webhook_url = args.webhook_url

    def dispatch(self, message):
        now = datetime.utcnow()
        __facts = self.facts[:]
        __facts.append({
            "name": "Posted At:",
            "value": now.strftime("%d/%m/%Y %H:%M:%S") + " UTC"
        })
        # Extract more facts from the message, because nxlog can ony inject a single line
        msg_facts = re.search(self.message_facts_re, message)

        if msg_facts is not None:
            __facts.append({
                "name": msg_facts.group(1),
                "value": msg_facts.group(2)
            })
            message = re.sub(self.message_facts_re, '', message)
        json_payload = {
            'text': self.severity,
            'title': self.title,
            "themeColor": self.hex_colour,
            "sections": [
                {
                    "facts": __facts,
                    "text": escape(message)
                }
            ]
        }

        if self.webhook_url.startswith('file://'):
            file = self.webhook_url[7:]
            open(file, 'a').write(json.dumps(json_payload, indent=4) + "\n")
        else:
            r = requests.post(url=self.webhook_url, json=json_payload)
            if self.debug is True:
                fh = open('debug.log', 'a')
                fh.write("Payload: {}".format(json.dumps(json_payload)))
                fh.write("Response status Code from MS Teams: {}".format(r.status_code))
                fh.write("Response from MS Teams: {}".format(r.text))
                fh.close()


def dd(data: dict):
    """
    Dump a dict and die.
    :param data:
    :return:
    """
    print(json.dumps(data, indent=4))
    sys.exit(255)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='MS Teams Sender')

    parser.add_argument('--severity', action="store", dest="severity")
    parser.add_argument('--profile', action="store", dest="profile", default="default")
    parser.add_argument('--sender', action="store", dest="sender")
    parser.add_argument('--message', action="store", dest="message", default=None)
    parser.add_argument('--pipe', action="store_true", dest="read_pipe", default=False)
    parser.add_argument('--title', action="store", dest="title", default="nxlog notification")
    parser.add_argument('--config', action="store", dest="config", default=None)
    parser.add_argument('--debug', action='store_true', dest="debug", default=False)

    args = parser.parse_args()
    dispatcher = MstSender(args)
    if args.message is not None:
        dispatcher.dispatch(args.message)
        sys.exit(0)
    sys.argv = []
    #
    # Keep the script running and wait for piped input.
    #
    for message in fileinput.input():
        log = open('/tmp/pipeeater.log', 'a')
        log.write('Eating from the pipe: ' + message)
        log.close()
        dispatcher.dispatch(message)
