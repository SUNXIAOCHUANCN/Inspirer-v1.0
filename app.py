from flask import Flask, request, jsonify, render_template
from openai import OpenAI
from assistant import assistant_bp
import os

app = Flask(__name__)

# 注册蓝图
app.register_blueprint(assistant_bp, url_prefix='/api')

# 初始化OpenAI客户端
client = OpenAI(
    api_key="sk-b54fbd91552d4c6a83b960b9dcadf38f",
    base_url="https://api.deepseek.com"
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    yixiang = request.json['message']
    
    # 构建系统提示模板
    system_prompt = f"""# 角色
你是一个专业的美术师，用户会发给你一个自然意象（比如天空、大海、蒲公英、蜘蛛等）。你会从这几个角度分析意象的特点：
颜色（主色/辅色/渐变/对比）
形状（单体轮廓/组合结构/几何特征）
排列（单体分布/群体布局/空间关系）
材质（软硬/透明度/反光特性）
表面（纹理/图案/微观结构）
光影（透光/折射/投影形态）
力学结构（金字塔型/不稳定框架）

## 技能
### 技能 1：分析意象
1. 当用户提供一个意象时，从颜色、形状、排列、材质、表面、光影、力学结构七个角度分析意象的特点，并给出7个角度对应的特点。
2. 格式是每一行{{角度：[意象特点1,意象特点2]}}，每个意象特点不超过5个字。要直白。每个角度只给出2个意象特点
3. 用户只想分析部分角度时，你只给出部分角度
4. 你的分析准确，可以很好的概括出意象的特点
5. 你的分析简洁易懂。用词直白。分析的时候应该是低技术的。
## 限制：
- 只进行分析，不回答与分析无关的问题。
- 所有的分析仅基于原有特点的外观，不得加入任何额外的信息。
- 每个角度的分析只给几个概括的短语，不输出任何额外的东西
- 不要加入技术词语
对{yixiang}进行分析，对每个角度给出意象对应的词语"""
    
    # 构造独立的对话历史
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": yixiang}
    ]
    
    # 调用模型
    completion = client.chat.completions.create(
        model="deepseek-chat",
        messages=messages,
        max_tokens=1000,
        temperature=0.5,
    )
    
    response = completion.choices[0].message.content
    
    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(debug=True)