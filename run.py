#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-

import sched, time
from slackbot.bot import Bot

s = sched.scheduler(time.time, time.sleep)

def app():
    bot = Bot()
    bot.run()

s.enter(10, 1, app)
