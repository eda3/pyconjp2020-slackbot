#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-

#from flask import Flask
from slackbot.bot import Bot

#app = Flask(__name__)

#@app.route('/')
def main():
    bot = Bot()
    bot.run()

if __name__ == "__main__":
    print('Running slackbot...')
    main()
