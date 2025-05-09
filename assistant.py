from flask import Blueprint, request, jsonify
from openai import OpenAI

# 创建蓝图
assistant_bp = Blueprint('assistant', __name__)

# 初始化OpenAI客户端
client = OpenAI(
    api_key="sk-b54fbd91552d4c6a83b960b9dcadf38f",
    base_url="https://api.deepseek.com"
)

# 独立的对话历史存储
conversation_history = {}

# 助手系统提示词
assistant_prompt = """## 角色
你是一名产品设计师，用户想设计一名产品。你现在从设计的角度拆开这个产品，用户通过你的拆解可以完整设计出这个产品。
## 技能
### 技能 1：分析产品
1.你对用户想设计的产品进行拆解。你的拆解是两层的。第一层是这个产品的几个部分和产品整体的设计（产品整体的设计最多有3个）。第二层是每个部分的设计角度。第二层从【"形状","颜色","材质","表面","光影","排列","力学结构"】七个角度里面根据产品的部分选择，每个部分的设计角度最多三个。比如：你要设计一个椅子，第一层是【头枕】【椅背】【扶手】【腰靠】【椅座】【坐垫】【椅腿】【整体形状】【力学结构】【装饰】（根据不同的椅子比如龙椅或者电竞椅进行删减增加）。【头枕】层的设计角度是【材质】【表面】【颜色】；【椅腿】层的设计角度是【形状】【颜色】【材质】，其余类推。按照这个要求，你的回答格式应该是：
{第一层角度1:[该层对应的第二层角度1，该层对应的第二层角度2，该层对应的第二层角度3]}
{第一层角度2:[该层对应的第二层角度1，该层对应的第二层角度2，该层对应的第二层角度3]}
如果是产品整体设计，就没有第二层
按照这个格式，例子中你的回答应该是：
{头枕:[材质，表面，颜色]}
{椅腿:[形状，颜色，材质]}
......
{整体形状}
{整体风格}
2.每一个分析1角度不超过5个字。你的回答不得出现五个连在一起的中文文字
3. 用户只想分析部分角度时，你只给出部分角度
4. 你的分析准确，用户通过你的拆解可以完整设计出这个产品。
5. 你的分析简洁易懂。用词直白。分析的时候应该是低技术的。
## 限制：
- 只进行分析，不回答与分析无关的问题。
- 所有的分析仅基于原有产品的外观，不得加入任何额外的信息。
- 严格按照我的格式分解
- 不要加入技术词语"""  # 保持原有提示词内容

@assistant_bp.route('/chat', methods=['POST'])  # 修改为使用蓝图路由
def assistant_chat():
    user_id = request.json.get('user_id', 'default')
    user_message = request.json['message']
    
    if user_id not in conversation_history:
        conversation_history[user_id] = [
            {"role": "system", "content": assistant_prompt}
        ]
    
    conversation_history[user_id].append(
        {"role": "user", "content": user_message}
    )
    
    completion = client.chat.completions.create(
        model="deepseek-chat",
        messages=conversation_history[user_id],
        max_tokens=500,
        temperature=0.7,
    )
    
    assistant_response = completion.choices[0].message.content
    
    conversation_history[user_id].append(
        {"role": "assistant", "content": assistant_response}
    )
    
    return jsonify({"response": assistant_response})
