import asyncio
import os

import botpy
from botpy.message import Message, GroupMessage
from botpy.ext.command_util import Commands
from botpy import logging, BotAPI
from botpy.ext.cog_yaml import read

_log = logging.get_logger()
config = read(os.path.join(os.path.dirname(__file__), "config.yml"))

class MyClient(botpy.Client):
    async def on_ready(self):
        _log.info(f"robot 「{self.robot.name}」 on_ready!")

    async def on_at_message_create(self, message: Message):
        _log.info(message.author.avatar)
        if "sleep" in message.content:
            await asyncio.sleep(10)
        _log.info(message.author.username)
        await message.reply(content=f"机器人{self.robot.name}收到你的@消息了: {message.content}")

    async def on_group_at_message_create(self, message: GroupMessage):
        messageResult = await message._api.post_group_message(
            group_openid=message.group_openid,
              msg_type=0,
              msg_id=message.id,
              content=f"收到了消息：{message.content}")
        _log.info(messageResult)


@Commands("test")
async def test(api: BotAPI, message: Message, params=None):
    await message.reply(content=params)
    await api.post_message(channel_id=message.channel_id, content=params, msg_id=message.id)
    return True


if __name__ == "__main__":
    intents = botpy.Intents(public_guild_messages=True)
    client = MyClient(intents=intents)
    client.run(appid=config['appid'], secret=config['secret'])