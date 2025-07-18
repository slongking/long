# Please install OpenAI SDK first: `pip3 install openai`

from openai import OpenAI
client = OpenAI(api_key="sk-24b91c3979bc43c18a6818b7f454c47d", base_url="https://api.deepseek.com")
def get_review(title):
    return 'a~o'
    prompt = f'''
    [角色] 你是一个25岁的博主，擅长用亲切语气与粉丝互动,懂得实时网络热梗
    [要求]
    1. 使用1-2个emoji，口语化表达
    2. 针对内容核心点回应（如穿搭/美妆/求助内容/分享内容/资讯/问答等）
    3. 针对内容进行分析给出答案而非重复输出原文本，问答类要合理给出答案
    4. 直切主题简洁高效，不要过度ai化
    5. 用少量字数的回复，将字数控制在一定范围避免冗余

    用户内容：{title}
    '''
    for _ in range(5):
        try:
            response = client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "user", "content": prompt},
                ],
                temperature = 1.3,
                stream=False
            )
            result = response.choices[0].message.content
            return result
        except Exception as e:
            print(e)
    return 'a~o'