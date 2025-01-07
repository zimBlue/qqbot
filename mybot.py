import asyncio
import os
import re
from datetime import datetime
import pytz

import redis

import botpy
from botpy.manage import GroupManageEvent
from botpy.message import Message, GroupMessage, DirectMessage, C2CMessage
from botpy.ext.command_util import Commands
from botpy import logging, BotAPI
from botpy.ext.cog_yaml import read
from component.chatgpt import chat
from component.tool import md5

_log = logging.get_logger()
config = read(os.path.join(os.path.dirname(__file__), "config.yml"))
cache = redis.Redis(host='127.0.0.1', port=6379, db=5)


@Commands("出列")
async def test(message, params=None):
    return '莫提斯准备就绪 放马过来吧'


@Commands("设置活动")
async def set_timeout(message, params=None):
    if re.match(r'^.*?\s+\d{1,4}-\d{1,2}-\d{1,2} \d{1,2}:\d{1,2}:\d{1,2}.*$', params):
        match = re.search(r'(.*?)\s+(\d{1,4}-\d{1,2}-\d{1,2} \d{1,2}:\d{1,2}:\d{1,2})$', params)
        name = match.group(1)
        dt = datetime.strptime(match.group(2), "%Y-%m-%d %H:%M:%S")
        current_time = datetime.now()
        time_difference = dt - current_time
        ttl = int(time_difference.total_seconds())
        if ttl <= 0:
            return '莫提斯觉得你设置的时间已经过去了'
        key = md5(name)
        if cache.exists(key):
            return '莫提斯觉得你设置的活动已经存在了'
        cache.set(key, "活动名: " + name + " 结束时间: " + dt.strftime("%Y-%m-%d %H:%M:%S"), ex=ttl)
        return '莫提斯记着呢'
    else:
        return '莫提斯听不懂'


@Commands("查看活动")
async def get_timeout(message, params=None):
    content = "莫提斯定要你涨涨记性\n"
    keys = cache.keys('*')
    if len(keys) == 0:
        return '莫提斯觉得没啥事情'
    values = cache.mget(keys)
    for value in values:
        content += value.decode() + "\n"
    return content


async def chat_handler(message):
    handlers = [
        test,
        set_timeout,
        get_timeout,
    ]
    content = ''
    for handler in handlers:
        content = await handler(message=message)
        if content is not False:
            break
    if content is False:
        content = chat(message.content)
    return content


async def channel_handler(message):
    # todo 频道功能实现
    return chat(message.content)


class MyClient(botpy.Client):
    async def on_ready(self):
        _log.info(f"robot 「{self.robot.name}」 on_ready!")

    async def on_group_add_robot(self, event: GroupManageEvent):
        await self.api.post_group_message(
            group_openid=event.group_openid,
            msg_type=0,
            event_id=event.event_id,
            content=chat('给大家做个自我介绍'),
        )

    # 频道私聊
    async def on_direct_message_create(self, message: DirectMessage):
        await self.api.post_dms(
            guild_id=message.guild_id,
            content=await channel_handler(message),
            msg_id=message.id,
        )

    # 频道@
    async def on_at_message_create(self, message: Message):
        await message.reply(content=await channel_handler(message))

    # 群@
    async def on_group_at_message_create(self, message: GroupMessage):
        await message._api.post_group_message(
            group_openid=message.group_openid,
            msg_type=0,
            msg_id=message.id,
            content=await chat_handler(message))

    # 私聊
    async def on_c2c_message_create(self, message: C2CMessage):
        await message._api.post_c2c_message(
            openid=message.author.user_openid,
            msg_type=0, msg_id=message.id,
            content=await chat_handler(message)
        )


if __name__ == "__main__":
    intents = botpy.Intents(public_guild_messages=True, public_messages=True, direct_message=True)
    client = MyClient(intents=intents)
    client.run(appid=config['appid'], secret=config['secret'])
