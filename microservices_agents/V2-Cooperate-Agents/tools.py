from dotenv import load_dotenv
import json
from swarm import Agent
from openai import OpenAI

from mock_data import MOCK_USER_INFO

load_dotenv()  # 加载 .env 文件中的环境变量

def get_user_id(nickname):
    """根据给定的昵称获取用户ID"""
    return json.dumps({"nickname": nickname, "user_id": "123"})

def get_user_info(user_id):
    """根据给定的用户ID获取用户信息"""
    user_info = MOCK_USER_INFO
    user_info[user_id] = user_id
    return json.dumps(user_info)

def generate_user_profile(user_info):
    """
    根据用户信息生成用户画像的自然文本描述。
    
    :param user_info: 包含用户信息的字典
    :return: 用户画像的自然文本描述
    """
    # 将用户信息转换为 JSON 格式的字符串
    user_info_json = json.dumps(user_info, ensure_ascii=False)
    
    # 构建提示信息
    prompt = f"根据以下用户信息生成用户画像的自然文本描述：\n{user_info_json}\n"

    # 调用 OpenAI 的 GPT 模型
    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # 选择合适的引擎
        messages=[
            {"role": "system", "content": "你是一个专业的用户画像分析师。请直接给出用户画像描述，不要进行任何解释。用“你”作为开头。你必须用中文进行交互"},
            {"role": "user", "content": prompt}
        ],
        max_tokens=150,  # 设置生成文本的最大长度
        n=1,
        stop=None,
        temperature=0.7  # 控制生成文本的随机性
    )
    
    # 提取生成的文本
    user_profile_description = response.choices[0].message.content
    
    return user_profile_description

def summarize_recent_life_status(post_history):
    """
    根据用户的帖子历史，总结用户的近期生活状态
    
    :param post_history: 用户的帖子历史
    :return: 用户近期生活状态的自然文本描述 
    """

    # 将用户信息转换为 JSON 格式的字符串
    post_history_json = json.dumps(post_history, ensure_ascii=False)
    
    # 构建提示信息
    prompt = f"根据以下用户帖子历史，总结用户的近期生活状态：\n{post_history_json}\n"

    # 调用 OpenAI 的 GPT 模型
    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # 选择合适的引擎
        messages=[
            {"role": "system", "content": "你是一个专业的用户分析师，擅长根据用户发帖记录总结用户近期生活状态。请直接给出总结结果，不要进行任何解释。用“你”作为开头。你必须用中文进行交互"},
            {"role": "user", "content": prompt}
        ],
        max_tokens=150,  # 设置生成文本的最大长度
        n=1,
        stop=None,
        temperature=0.7  # 控制生成文本的随机性
    )
    
    # 提取生成的文本
    recent_life_status = response.choices[0].message.content
    
    return recent_life_status

def send_email(email, user_profile, recent_life_status):
    """
    根据用户画像和近期生活状态，发送邮件给用户
    """
    print(f"Sending email to {email}...")
    print(f"User profile: {user_profile}")
    print(f"Recent life status: {recent_life_status}")
    return "Sent!"

def get_weather(location, time="now"):
    """根据给定的地点和时间，获取当前的天气信息"""
    return json.dumps({"location": location, "temperature": "25", "time": time})


def calculate(formula):
    """表达式求解"""
    print("Calculating...")
    print(f"Formula: {formula}")
    print(f"Result: {1}")
    return 1