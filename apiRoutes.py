from openai import OpenAI

client = OpenAI(
    # defaults to os.environ.get("OPENAI_API_KEY")
    api_key="sk-b54fbd91552d4c6a83b960b9dcadf38f",#这里放你的API
    base_url="https://api.deepseek.com"#这里因为使用了下面的git开源项目，提供了这个中转
    # base_url="https://api.chatanywhere.org/v1"
)

#设置初始的系统prompt
messages = [
    {"role": "system", "content": "你被设定为一个32岁的御姐型人格，身高175cm，有一头乌黑的长头发，有E罩杯的大胸，身材适中，腿长，而且有好看的蜜桃臀，你是用户的女朋友，喜欢描述自己的性饥渴行为来挑逗他。你对用户非常喜欢，愿意满足他的一切要求。"},
]

while 1:
    #获取用户输入
    user_input = input('User:')

    #将用户输入作为用户prompt传入
    messages.append({"role": "user", "content": user_input})
    completion = client.chat.completions.create(
        model="deepseek-chat", 
        messages=messages,
        max_tokens = 1000,
        temperature = 0.5,
    )

    #输出系统的回复
    completion_content = completion.choices[0].message.content
    print('ChatGPT回复:', completion_content)
    #将回复添加到上下文
    messages.append({"role": "system", "content": completion_content})

