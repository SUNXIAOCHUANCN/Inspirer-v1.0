from openai import OpenAI

client = OpenAI(
    # defaults to os.environ.get("OPENAI_API_KEY")
    api_key="sk-b54fbd91552d4c6a83b960b9dcadf38f",#这里放你的API
    base_url="https://api.deepseek.com"#这里因为使用了下面的git开源项目，提供了这个中转
    # base_url="https://api.chatanywhere.org/v1"
)

completion = client.chat.completions.create(
    # 调用模型，这里写的调用了ChatGPT-3.5，可以按照需求更改，前提是API支持这个模型
    model="deepseek-chat",
    # messages 是对话列表
    messages=[
        {"role": "system", "content": "You are a helpful assistant."}, #系统prompt
        {"role": "user", "content": "Hello!"} #用户prompt
    ],
    max_tokens = 1000,
    temperature = 0.5,
)

#调用该 API 会返回一个 ChatCompletion 对象，其中包括了回答文本、创建时间、id 等属性。
#我们一般需要的是回答文本，也就是回答对象中的 content 信息
completion_content = completion.choices[0].message.content

# 打印生成的回复
print("ChatGPT回复：", completion_content)