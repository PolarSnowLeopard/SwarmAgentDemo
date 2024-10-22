from dotenv import load_dotenv
import json
from swarm import Agent
from openai import OpenAI

from mock_data import (
    MOCK_USER_INFO,
    MOCK_USER_ID
)

load_dotenv()  # 加载 .env 文件中的环境变量

def get_user_id(nickname):
    """获取给定昵称的用户ID。

    参数:
        nickname (str): 用户的昵称。

    返回:
        str: 用户ID的JSON格式。
    """
    return json.dumps(MOCK_USER_ID.get(nickname,{}), ensure_ascii=False)

def get_user_info(user_id):
    """获取给定用户ID的用户信息。

    参数:
        user_id (str): 用户的ID。

    返回:
        str: 用户信息的JSON格式。
    """
    return json.dumps(MOCK_USER_INFO.get(user_id, {}), ensure_ascii=False)

def generate_education_description(college, major):
    """生成院校与专业的介绍。

    参数:
        college (str): 学校名称。
        major (str): 专业名称。

    返回:
        str: 学校与专业的自然语言描述。
    """
    # 构建提示信息
    prompt = f"根据给定的学校名称与专业名称生成对该院校与专业的介绍：\n{college} {major}\n"

    # 调用 OpenAI 的 GPT 模型
    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # 选择合适的引擎
        messages=[
            {"role": "system", "content": "你是一个专业的院校与专业介绍分析师。"
             "请撰写一段邮件内容，介绍给定的院校与专业。你的回答只需要包含一段话，"
             "不要包含称谓、落款、日期等任何信息，不要进行任何解释。你必须用中文进行交互"},
            {"role": "user", "content": prompt}
        ],
        max_tokens=512,  # 设置生成文本的最大长度
        n=1,
        stop=None,
        temperature=0.7  # 控制生成文本的随机性
    )
    
    # 提取生成的文本
    user_profile_description = response.choices[0].message.content
    
    return user_profile_description

def summarize_recent_life_status(post_history):
    """根据用户的帖子历史总结用户的近期生活状态。

    参数:
        post_history (str): 用户的帖子历史。

    返回:
        str: 用户近期生活状态的自然语言描述。
    """
    
    # 构建提示信息
    prompt = f"根据以下用户帖子历史，总结用户的近期生活状态：\n{post_history}\n"

    # 调用 OpenAI 的 GPT 模型
    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # 选择合适的引擎
        messages=[
            {"role": "system", "content": "你是一个专业的用户分析师，擅长根据用户发帖记录总结用户近期生活状态，"
             "并撰写一段邮件内容。你的回答只需要包含一段话，"
             "不要包含称谓、落款、日期等任何信息，不要进行任何解释。用“你”作为开头。你必须用中文进行交互"},
            {"role": "user", "content": prompt}
        ],
        max_tokens=512,  # 设置生成文本的最大长度
        n=1,
        stop=None,
        temperature=0.7  # 控制生成文本的随机性
    )
    
    # 提取生成的文本
    recent_life_status = response.choices[0].message.content
    
    return recent_life_status

def send_email(email, education_description, recent_life_status):
    """合并用户本科院校与专业介绍、近期生活状态发送邮件给用户。

    参数:
        email (str): 用户的电子邮件地址。
        education_description (str): 用户的本科院校与专业介绍。
        recent_life_status (str): 用户的近期生活状态。

    返回:
        str: 确认邮件已发送的消息。
    """
    print(f"Sending email to {email}...")
    print(f"Education description: {education_description}")
    print(f"Recent life status: {recent_life_status}")
    return "Sent!"

def get_weather(location, time="now"):
    """获取给定地点和时间的当前天气信息。

    参数:
        location (str): 获取天气的地点。
        time (str, optional): 获取天气的时间。默认为"now"。

    返回:
        str: 天气信息的JSON格式。
    """
    return json.dumps({"location": location, "temperature": "25", "time": time})

def calculate(formula):
    """求解数学表达式。

    参数:
        formula (str): 要求解的数学表达式。

    返回:
        int: 计算结果。
    """
    print("Calculating...")
    print(f"Formula: {formula}")
    print(f"Result: {1}")
    return 1

def exit_script():
    """结束与用户的交互。"""
    print("Exiting script...")
    exit()
