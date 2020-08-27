#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-

from slackbot.bot import respond_to
from slackbot.bot import listen_to
from datetime import datetime, date, time, timedelta
import re
import tempfile

import google.auth
from google.cloud import secretmanager
from google.cloud import storage
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
import pandas as pd

credentials, project = google.auth.default()

storage_client = storage.Client()
bucket = storage_client.get_bucket(project)
blob = bucket.get_blob('table_cleansed.csv')
with tempfile.NamedTemporaryFile(delete=True) as t:
    blob.download_to_file(t)
    with open(t.name, 'r') as f:
        data = pd.read_csv(f)

data['start_day'] = pd.to_datetime(data['day']).apply(lambda s: s.date())
data['start_time'] = data['no'].apply(time.fromisoformat)
z = zip(data['start_day'].to_list(), data['start_time'].to_list())
data['start'] = [datetime.combine(d, t) for d, t in z]
data['end'] = data['start'] + pd.to_timedelta(data['length_minutes'], unit='minutes')

#def get_sentiment(message, content):
#    document = types.Document(
#        content=content,
#        type=enums.Document.Type.PLAIN_TEXT
#    )
#    annotations = language.LanguageServiceClient().analyze_sentiment(document=document)
#    message.reply('にゃっ？！')
#    # Refer to: https://cloud.google.com/natural-language/docs/basics#interpreting_sentiment_analysis_values
#    if (annotations.document_sentiment.score > 0.3) and (annotations.document_sentiment.magnitude > 1.5):
#        raise ValueError(f'Clearly positive: {annotations.document_sentiment.score, annotations.document_sentiment.magnitude}')
#    elif (annotations.document_sentiment.score < -0.3) and (annotations.document_sentiment.magnitude > 1.5):
#        raise ValueError(f'Clearly negative: {annotations.document_sentiment.score, annotations.document_sentiment.magnitude}')
#    else:
#        pass
#
@listen_to('who', re.IGNORECASE)
def get_speaker(message):
    t = datetime.utcnow() + timedelta(hours=9)
    on_stage = data[(data['start'] <= t) & (data['end'] >= t)]['name']
    if len(on_stage) == 0:
        message.reply("It's {:%H:%M} now, but, sorry, nobody on stage.".format(t))
    else:
        message.reply("It's {:%H:%M} now!  Who's on stage?\n{}".format(t, '\n'.join(on_stage.to_list())))

@listen_to('what', re.IGNORECASE)
def get_title(message):
    t = datetime.utcnow() + timedelta(hours=9)
    on_air= data[(data['start'] <= t) & (data['end'] >= t)]['title']
    if len(on_air) == 0:
        message.reply("It's {:%H:%M} now, but, sorry, nothing on air.".format(t))
    else:
        message.reply("It's {:%H:%M} now!  What's on air?\n{}".format(t, '\n'.join(on_air.to_list())))

@listen_to('だれ|誰', re.IGNORECASE)
def get_speaker_jp(message):
    t = datetime.utcnow() + timedelta(hours=9)
    on_stage = data[(data['start'] <= t) & (data['end'] >= t)]['name']
    if len(on_stage) == 0:
        message.reply("ただいま {:%H:%M} ですのにゃ。だれも居ない…".format(t))
    else:
        message.reply("ただいま {:%H:%M} ですのにゃ。ステージに居るのは…！\n{}".format(t, '\n'.join(on_stage.to_list())))

@listen_to('なに|何', re.IGNORECASE)
def get_title_jp(message):
    t = datetime.utcnow() + timedelta(hours=9)
    on_air= data[(data['start'] <= t) & (data['end'] >= t)]['title']
    if len(on_air) == 0:
        message.reply("ただいま {:%H:%M} ですのにゃ。なにもやってない…".format(t))
    else:
        message.reply("ただいま {:%H:%M} ですのにゃ。ただいまオンエア…！\n{}".format(t, '\n'.join(on_air.to_list())))

@respond_to('hi|hello', re.IGNORECASE)
def hi(message):
    message.reply('I can understand hi or HI!')
    # react with thumb up emoji
    message.react('+1')

@respond_to('こんにちは|こんち|はろー?|ハロー?')
def hi_jp(message):
    message.reply('こんにちは！')
    # react with thumb up emoji
    message.react('+1')

@respond_to('I love you')
def love(message):
    message.reply('I love you too!')

@respond_to('かわいい?|カワイイ?|愛してい?る|あいしてい?る')
def love_jp(message):
    message.reply('愛情を感じるにゃん')

@listen_to('Can someone help me?')
def help(message):
    # Message is replied to the sender (prefixed with @user)
    message.reply('Yes, I can!')

    # Message is sent on the channel
    message.send('I can help everybody!')

    # Start a thread on the original message
    message.reply("Here's a threaded reply", in_thread=True)

@listen_to('へるぷ|ヘルプ|お?助て?|お?たすけて?')
def help_jp(message):
    # Message is replied to the sender (prefixed with @user)
    message.reply('お任せあれ！')

    # Message is sent on the channel
    message.send('みんなの味方！')

    # Start a thread on the original message
    message.reply("こんなお返事もできるにゃー", in_thread=True)

@respond_to('raise error')
def raise_error(message):
    raise ValueError('Simulating an error for you!')
