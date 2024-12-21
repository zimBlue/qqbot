import asyncio
import os

import botpy
from botpy.message import Message, GroupMessage, DirectMessage
from botpy.ext.command_util import Commands
from botpy import logging, BotAPI
from botpy.ext.cog_yaml import read

_log = logging.get_logger()
config = read(os.path.join(os.path.dirname(__file__), "config.yml"))

@Commands("test")
async def test(api: BotAPI, message: Message, params=None):
    await message.reply(content='测试成功')
    await api.post_message(channel_id=message.channel_id, content='测试成功', msg_id=message.id)
    return True


class MyClient(botpy.Client):
    async def on_ready(self):
        _log.info(f"robot 「{self.robot.name}」 on_ready!")

    async def on_direct_message_create(self, message: DirectMessage):
        await self.api.post_dms(
            guild_id=message.guild_id,
            content=f"机器人{self.robot.name}收到你的私信了: {message.content}",
            msg_id=message.id,
        )

    async def on_at_message_create(self, message: Message):
        # 注册指令handler
        handlers = [
            test,
        ]
        for handler in handlers:
            if await handler(api=self.api, message=message):
                return
        else:
            await message.reply(content=f"机器人{self.robot.name}收到你的@消息了: {message.content}")

    async def on_group_at_message_create(self, message: GroupMessage):
        messageResult = await message._api.post_group_message(
            group_openid=message.group_openid,
              msg_type=0,
              msg_id=message.id,
              content=f"收到了消息：{message.content}")
        _log.info(messageResult)


if __name__ == "__main__":
    intents = botpy.Intents(public_guild_messages=True)
    client = MyClient(intents=intents)
    client.run(appid=config['appid'], secret=config['secret'])