#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-

from slackbot.bot import Bot

def main():
    bot = Bot()
    bot.run()

app = main()

if __name__ == "__main__":
    print('Running slackbot...')
    main()
