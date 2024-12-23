import os
import openai

# optional; defaults to `os.environ['OPENAI_API_KEY']`
openai.api_key = "sk-E2iChmJK9dS5gl1dD477FcA909504dB39d73De184936A1C5"

# all client options can be configured just like the `OpenAI` instantiation counterpart
openai.base_url = "https://free.v36.cm/v1/"
openai.default_headers = {"x-foo": "true"}

def chat(message, model='gpt-3.5-turbo-0125'):
    completion = openai.chat.completions.create(
        model="gpt-3.5-turbo-1106",
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