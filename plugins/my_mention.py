#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-

from slackbot.bot import respond_to
from slackbot.bot import listen_to
import re
import tempfile

import google.auth
from google.cloud import secretmanager
from google.cloud import storage
import pandas as pd

credentials, project = google.auth.default()

storage_client = storage.Client()
bucket = storage_client.get_bucket(project)
blob = bucket.get_blob('table_cleansed.csv')
with tempfile.NamedTemporaryFile(delete=True) as t:
    blob.download_to_file(t)
    with open(t.name, 'r') as f:
        data = pd.read_csv(f)

@respond_to('hi', re.IGNORECASE)
def hi(message):
    message.reply('I can understand hi or HI!')
    # react with thumb up emoji
    message.react('+1')

@respond_to('こんにちは')
def hi(message):
    message.reply('こんにちは！')
    # react with thumb up emoji
    message.react('+1')

@respond_to('I love you')
def love(message):
    message.reply('I love you too!')

@respond_to('かわいい|愛している')
def love(message):
    message.reply('愛情を感じるにゃん')

@listen_to('Can someone help me?')
def help(message):
    # Message is replied to the sender (prefixed with @user)
    message.reply('Yes, I can!')

    # Message is sent on the channel
    message.send('I can help everybody!')

    # Start a thread on the original message
    message.reply("Here's a threaded reply", in_thread=True)

@listen_to('ヘルプ')
def help(message):
    # Message is replied to the sender (prefixed with @user)
    message.reply('お任せあれ！')

    # Message is sent on the channel
    message.send('みんなの味方！')

    # Start a thread on the original message
    message.reply("こんなお返事もできるにゃー", in_thread=True)
