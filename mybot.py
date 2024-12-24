import asyncio
import os
import re
from datetime import datetime

import redis

import botpy
from botpy.message import Message, GroupMessage, DirectMessage, C2CMessage
from botpy.ext.command_util import Commands
from botpy import logging, BotAPI
from botpy.ext.cog_yaml import read
from component.chatgpt import chat
from component.tool import generate_random_key

_log = logging.get_logger()
config = read(os.path.join(os.path.dirname(__file__), "config.yml"))
cache = redis.Redis(host='127.0.0.1', port=6379, db=2)

@Commands("出列")
async def test(api: BotAPI, message: Message, params=None):
    await message.reply(content='莫提斯准备就绪 放马过来吧')
    return True

@Commands("设置活动")
async def setTimeOut(api: BotAPI, message: Message, params=None):
    if re.match(r'^(.*?)\s+(\d{1,4})-(\d{1,2})-(\d{1,2}) (\d{1,2}):(\d{1,2}):(\d{1,2}).*$', message.content):
        match = re.search(r'.*?设置活动\s+(.*?)\s+(\d{1,4})-(\d{1,2})-(\d{1,2}) (\d{1,2}):(\d{1,2}):(\d{1,2})$', message.content)
        name = match.group(1)
        year = int(match.group(2))
        month = int(match.group(3))
        day = int(match.group(4))
        hour = int(match.group(5))
        minute = int(match.group(6))
        second = int(match.group(7))

        dt = datetime(int(year), int(month), int(day), int(hour), int(minute), int(second))
        current_time = datetime.now()
        time_difference = dt - current_time
        ttl = int(time_difference.total_seconds())
        cache.set(generate_random_key(), "活动名: " + name + " 结束时间: " + dt.strftime("%Y-%m-%d %H:%M:%S"), ex=ttl)
        await api.post_message(channel_id=message.channel_id, content='莫提斯记着呢', msg_id=message.id)
    else:
        await api.post_message(channel_id=message.channel_id, content='莫提斯听不懂', msg_id=message.id)
    return True

@Commands("查看活动")
async def getTimeOut(api: BotAPI, message: Message, params=None):
    content = "莫提斯定要你涨涨记性\n"
    keys = cache.keys('*')
    if len(keys) == 0:
        await api.post_message(channel_id=message.channel_id, content='莫提斯觉得没啥事情', msg_id=message.id)
        return True
    values = cache.mget(keys)
    for value in values:
        content += value.decode() + "\n"
    await api.post_message(channel_id=message.channel_id, content=content, msg_id=message.id)
    return True

class MyClient(botpy.Client):
    async def on_ready(self):
        _log.info(f"robot 「{self.robot.name}」 on_ready!")

    async def on_direct_message_create(self, message: DirectMessage):
        handlers = [
            test,
            setTimeOut,
            getTimeOut,
        ]
        for handler in handlers:
            if await handler(api=message._api, message=Message(message)):
                return
        await self.api.post_dms(
            guild_id=message.guild_id,
            content=chat(message.content),
            msg_id=message.id,
        )

    async def on_at_message_create(self, message: Message):
        handlers = [
            test,
            setTimeOut,
            getTimeOut,
        ]
        for handler in handlers:
            if await handler(api=self.api, message=message):
                return
        else:
            await message.reply(content=chat(message.content))

    async def on_group_at_message_create(self, message: GroupMessage):
        await message._api.post_group_message(
            group_openid=message.group_openid,
            msg_type=0,
            msg_id=message.id,
            content=chat(message.content))

    async def on_c2c_message_create(self, message: C2CMessage):
        await message._api.post_c2c_message(
            openid=message.author.user_openid,
            msg_type=0, msg_id=message.id,
            content=chat(message.content)
        )


if __name__ == "__main__":
    intents = botpy.Intents(public_guild_messages=True, public_messages=True, guild_messages=True, direct_messages=True)
    client = MyClient(intents=intents)
    client.run(appid=config['appid'], secret=config['secret'])