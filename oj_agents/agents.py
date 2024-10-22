from tools import *

oj_agent = Agent(
    name="OJ提交Agent",
    instructions="你是一个OJ提交助手，善于提交代码到OJ平台。并根据OJ平台的反馈来生成评分报告。你必须用中文进行交互",
    functions=[
        generate_submission,
        submit_code,
        generate_score_report,
    ],
)