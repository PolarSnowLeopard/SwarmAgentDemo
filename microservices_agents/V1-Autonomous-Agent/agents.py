from tools import *

microservices_agent = Agent(
    name="微服务组合Agent",
    instructions="你是一个微服务组合助手，善于根据给定需求选择微服务进行组合以构建应用。你必须用中文进行交互",
    functions=[
        get_user_id,
        get_user_info,
        generate_user_profile,
        summarize_recent_life_status,
        send_email,
        get_weather,
        calculate,
    ],
)