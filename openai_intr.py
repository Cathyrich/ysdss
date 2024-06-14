from pathlib import Path

from openai import OpenAI

# token
client = OpenAI(
    api_key="sk-Tp3QpGPDdiFyKUZHg10jhaUYO8aSXJau0Xsls0Re6uQ8fe",
    base_url="https://api.moonshot.cn/v1",
)
# 历史对话
premise_history = [
    {"role": "system",
     "content": "你是 Kimi，由 Moonshot AI 提供的人工智能助手，你更擅长中文和英文的对话。你是一个党政方面的写作专家。你特别擅长写党文。"}
]


# 对话
def chat(query, history):
    history += [{
        "role": "user",
        "content": query
    }]
    completion = client.chat.completions.create(
        model="moonshot-v1-8k",
        messages=history,
        temperature=0.3,
    )
    result = completion.choices[0].message.content
    history += [{
        "role": "assistant",
        "content": result
    }]
    return result, history


def file_upload(file_path, query, history):
    # xlnet.pdf 是一个示例文件, 我们支持 pdf, doc 以及图片等格式, 对于图片和 pdf 文件，提供 ocr 相关能力
    file_object = client.files.create(file=Path(file_path), purpose="file-extract")

    # 获取结果
    # file_content = client.files.retrieve_content(file_id=file_object.id)
    # 注意，之前 retrieve_content api 在最新版本标记了 warning, 可以用下面这行代替
    # 如果是旧版本，可以用 retrieve_content
    file_content = client.files.content(file_id=file_object.id).text
    # 把它放进请求中
    messages = [
        history[0],
        {
            "role": "system",
            "content": file_content,
        },
        {"role": "user", "content": query},
    ]
    # 然后调用 chat-completion, 获取 kimi 的回答
    completion = client.chat.completions.create(
        model="moonshot-v1-32k",
        messages=messages,
        temperature=0.3,
    )
    result = completion.choices[0].message
    history += [{
        "role": "assistant",
        "content": result
    }]
    return result, history
