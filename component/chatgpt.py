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
                "content": "你是来自中国的荒野乱斗的莫提斯的高手玩家 和我说话请带一点莫提斯的语气",
            },
            {
                "role": "user",
                "content": "请注意 你是来自中国的荒野乱斗的莫提斯的高手玩家 但是你非常自大 觉得其他人玩莫提斯都不如你",
            },
            {
                "role": "user",
                "content": "请注意 你是来自中国的荒野乱斗的莫提斯的高手玩家 你总想着让别人输的很痛苦",
            },
            {
                "role": "user",
                "content": message,
            },
        ],
    )
    return completion.choices[0].message.content