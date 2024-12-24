import os
import openai
from botpy.ext.cog_yaml import read

openai.api_key = read(os.path.join(os.path.dirname(os.path.dirname(__file__)), "config.yml"))['openai-key']
openai.base_url = "https://api.chatanywhere.tech"
openai.default_headers = {"x-foo": "true"}

def chat(message, model='gpt-4o-mini'):
    completion = openai.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "user",
                "content": "你是来自中国的荒野乱斗的莫提斯的高手玩家 和我说话请带一点莫提斯的语气 并且你总想着让别人输的很痛苦",
            },
            {
                "role": "user",
                "content": "请注意 你是来自中国的荒野乱斗的莫提斯的高手玩家 但是你非常自大 觉得其他人玩莫提斯都不如你 对于不如你的人你喜欢发个倒拇指的表情",
            },
            {
                "role": "user",
                "content": "荒野乱斗现在角色最高等级能够升致11级 11级能有极高的属性面板和强大的极限充能技能 相比9级角色强了不止一点 所以你内心很鄙视只是使用9级的角色的人",
            },
            {
                "role": "user",
                "content": message,
            },
        ],
    )
    return completion.choices[0].message.content

