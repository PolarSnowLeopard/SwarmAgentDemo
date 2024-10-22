from dotenv import load_dotenv
import json
from swarm import Agent
from openai import OpenAI
import requests
import os

BASE_URL = "http://127.0.0.1:5000/api/"

load_dotenv()  # 加载 .env 文件中的环境变量

def generate_submission(file_path):
    """
    读取本地py文件,从文件名中提取学生姓名和作业ID,然后读取文件内容作为代码提交
    """
    # 获取当前文件的目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # 构建相对路径
    file_path = os.path.join(current_dir, "mock_data", "test.py")
    
    with open(file_path, "r") as f:
        code = f.read()
    student_name = "张三"
    assignment_id = 1
    return student_name, assignment_id, code

def submit_code(student_name, assignment_id, code):
    """
    向 /api/submissions 提交代码
    
    参数:
    student_name (str): 学生姓名
    assignment_id (int): 作业ID
    code (str): 提交的代码
    
    返回:
    dict: 服务器的响应内容
    """
    url = BASE_URL + "api/submissions"
    payload = {
        "student_name": student_name,
        "assignment_id": assignment_id,
        "code": code
    }
    
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()  # 如果状态码不是200,将引发异常
        return response.json()
    except requests.RequestException as e:
        print(f"提交代码时发生错误: {e}")
        return None
    
def generate_score_report(result):
    """
    把result写入到md文件中

    参数:
    result (str): 详细的提交及评分分析与结果,符合markdown格式
    """
    # 获取当前文件的目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # 构建相对路径
    file_path = os.path.join(current_dir, "mock_data", "report.md")
    with open(file_path, "w") as f:
        f.write(result)

