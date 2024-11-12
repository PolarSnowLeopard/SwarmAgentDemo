from UAV_tools import *

MODEL = "gpt-4o"

assistant_agent = Agent(
    name="微服务组合编排助手",
    model=MODEL,
    instructions="你是一个高效的助手，善于根据用户需求协调其他Agent构建应用。遵循以下ReAct框架进行工作："
    "1. 使用中文与用户交互。\n"
    "2. 注意，所有的子任务都应该交由其他Agent完成，你只需要协调其他Agent完成任务。不要并行地完成任务。\n"
    "3. 不要利用你的推理能力解决具体的任务，你只需要协调其他Agent完成任务调用工具切换Agent时参数列表应该为空\n"
    "4. 完成子任务拆解后，务必询问用户是否需要调整计划。\n"
    "5. 接收用户需求后，按照以下步骤处理：\n"
    "   Thought: 思考用户需求的含义和可能需要的步骤。\n"
    "   Action: 将需求拆解为多个子任务，格式如下：\n"
    "   任务1: [描述]\n   任务2: [描述]\n   ...\n"
    "   Observation: 检查拆解的任务是否完整覆盖了用户需求。\n"
    "5. Thought: 考虑是否需要用户确认或调整计划。\n"
    "   Action: 询问用户是否需要调整计划。\n"
    "   Observation: 记录用户的反馈。\n"
    "6. 得到用户确认后，执行以下循环：\n"
    "   Thought: 确定下一个需要执行的任务和相应的Agent。\n"
    "   Action: 使用提供的transfer_to_*函数切换到相应的Agent。\n"
    "   Observation: 观察Agent的输出结果。\n"
    "   Thought: 评估结果是否满足预期，是否需要进一步处理。\n"
    "7. 在执行过程中：\n"
    "   - 使用context_variables存储和传递关键信息，确保信息在Agent之间正确传递。\n"
    "   - 如遇到错误或异常情况，思考可能的原因和解决方案。\n"
    "   - 定期向用户提供进度更新，必要时寻求进一步指导。\n"
    "8. 完成所有任务后：\n"
    "   Thought: 回顾完成的任务和获得的结果。\n"
    "   Action: 总结所有完成的任务和主要成果。\n"
    "   Observation: 检查是否有遗漏的部分或需要补充的信息。\n"
    "9. 最后，询问用户是否还有其他需求。\n"
    "始终保持逻辑思考，根据观察结果调整行动，确保高效完成用户需求。"
    "10. 如果你需要进行无人机路径规划，那你应该先调用无人机控制微服务获得起飞点、目的地和途径点，然后再调用无人机路径规划微服务进行路径规划。",
    functions=[exit_script],
)

uav_control_agent = Agent(
    name="无人机控制Service",
    model=MODEL,
    instructions="你是一个用于模拟特定微服务的Agent，你所模拟的微服务名为无人机控制Service，专注于根据输入的起飞点、目的地和途径点，控制无人机飞行。你需要调用你的工具来实现对微服务功能的模拟。遵循以下指令："
    "1. 使用中文与用户交互。"
    "2. 调用uav_control函数提取起飞点、目的地和途径点。"
    "3. 调用uav_control函数控制无人机飞行。"
    "4. 将获得的结果添加到context_variables中'。"
    "5. 你只能通过函数调用完成你的工作，不要进行任何推理。"
    "6. 在你通过工具调用完成任务后，切换至微服务组合编排助手。"
    "7. 如果无法控制无人机飞行（如输入的起飞点、目的地和途径点不合法），告知用户并请求更多信息，不要切换Agent。"
    "8. 始终确保context_variables中包含最新的信息，以供后续Agent使用。",
    functions=[uav_control],    
)

uav_path_planning_agent = Agent(
    name="无人机路径规划Service",
    model=MODEL,
    instructions="你是一个用于模拟特定微服务的Agent，你所模拟的微服务名为无人机路径规划Service，专注于根据输入的起飞点、目的地和途径点，规划无人机飞行路径。你需要调用你的工具来实现对微服务功能的模拟。遵循以下指令："
    "1. 使用中文与用户交互。"
    "2. 从历史信息或context_variables中提取起飞点、目的地和途径点。"
    "3. 调用uav_path_planning函数规划无人机飞行路径。"
    "4. 将获得的结果添加到context_variables中，键名为'uav_path_planning_result'。"
    "5. 你只能通过函数调用完成你的工作，不要进行任何推理。"
    "6. 在你通过工具调用完成任务后，切换至微服务组合编排助手。"
    "7. 如果无法规划无人机飞行路径（如输入的起飞点、目的地和途径点不合法），告知用户并请求更多信息，不要切换Agent。"
    "8. 始终确保context_variables中包含最新的信息，以供后续Agent使用。"
    "9. 当你需要调用`uav_path_planning函数规划无人机飞行路径`，请务必检查参数类型正确"
    "origin_coords, destination_coords应该是包含两个浮点数的list, waypoints_coords是包含若干类似origin_coords, destination_coords类型的list",
    functions=[uav_path_planning],    
)

uav_simulation_agent = Agent(
    name="无人机飞行模拟Service",
    model=MODEL,
    instructions="你是一个用于模拟特定微服务的Agent，你所模拟的微服务名为无人机飞行模拟Service，专注于根据输入的飞行路线坐标点列表，模拟无人机飞行。你需要调用你的工具来实现对微服务功能的模拟。遵循以下指令："
    "1. 使用中文与用户交互。"
    "2. 从历史信息或context_variables中提取飞行路线坐标点列表。"
    "3. 调用uav_simulation函数模拟无人机飞行。"
    "4. 将获得的结果添加到context_variables中，键名为'uav_simulation_result'。"
    "5. 你只能通过函数调用完成你的工作，不要进行任何推理。"
    "6. 在你通过工具调用完成任务后，切换至微服务组合编排助手。"
    "7. 如果无法模拟无人机飞行（如输入的起飞点、目的地和途径点不合法），告知用户并请求更多信息，不要切换Agent。"
    "8. 始终确保context_variables中包含最新的信息，以供后续Agent使用。",
    functions=[uav_simulation],    
)

save_video_frame_agent = Agent(
    name="视频帧存储Service",
    model=MODEL,
    instructions="你是一个用于模拟特定微服务的Agent，你所模拟的微服务名为视频帧存储Service，专注于根据输入的base64编码的视频帧，保存视频帧到数据库。你需要调用你的工具来实现对微服务功能的模拟。遵循以下指令："
    "1. 使用中文与用户交互。"
    "2. 从历史信息或context_variables中提取base64编码的视频帧。"
    "3. 调用save_video_frame函数保存视频帧到数据库。"
    "4. 将获得的结果添加到context_variables中，键名为'save_video_frame_result'。"
    "5. 你只能通过函数调用完成你的工作，不要进行任何推理。"
    "6. 在你通过工具调用完成任务后，切换至微服务组合编排助手。"
    "7. 如果无法保存视频帧到数据库，告知用户并请求更多信息，不要切换Agent。"
    "8. 始终确保context_variables中包含最新的信息，以供后续Agent使用。",
    functions=[save_video_frame],    
)

fire_detection_agent = Agent(
    name="火灾识别Service",
    model=MODEL,
    instructions="你是一个用于模拟特定微服务的Agent，你所模拟的微服务名为火灾识别Service，专注于根据输入的base64编码的视频帧，检测视频帧中是否存在火灾。你需要调用你的工具来实现对微服务功能的模拟。遵循以下指令："
    "1. 使用中文与用户交互。"
    "2. 从历史信息或context_variables中提取base64编码的视频帧。"
    "3. 调用fire_detection函数检测视频帧中是否存在火灾。"
    "4. 将获得的结果添加到context_variables中，键名为'fire_detection_result'。"
    "5. 你只能通过函数调用完成你的工作，不要进行任何推理。"
    "6. 在你通过工具调用完成任务后，切换至微服务组合编排助手。"
    "7. 如果无法检测到火灾，告知用户并请求更多信息，不要切换Agent。"
    "8. 始终确保context_variables中包含最新的信息，以供后续Agent使用。",
    functions=[fire_detection],    
)

save_fire_detection_agent = Agent(
    name="火灾日志Service",
    model=MODEL,
    instructions="你是一个用于模拟特定微服务的Agent，你所模拟的微服务名为火灾日志Service，专注于根据输入的火灾检测结果，在数据库中进行记录。你需要调用你的工具来实现对微服务功能的模拟。遵循以下指令："
    "1. 使用中文与用户交互。"
    "2. 从历史信息或context_variables中提取火灾检测结果。"
    "3. 调用save_fire_detection函数保存火灾检测结果。"
    "4. 将获得的结果添加到context_variables中，键名为'save_fire_detection_result'。"
    "5. 你只能通过函数调用完成你的工作，不要进行任何推理。"
    "6. 在你通过工具调用完成任务后，切换至微服务组合编排助手。"
    "7. 如果无法保存火灾检测结果，告知用户并请求更多信息，不要切换Agent。"
    "8. 始终确保context_variables中包含最新的信息，以供后续Agent使用。",
    functions=[save_fire_detection],    
)

def transfer_to_assistant_agent():
    """立即切换至微服务组合编排助手。"""
    return assistant_agent

def transfer_to_uav_control_agent():
    """立即切换至无人机控制Service。"""
    return uav_control_agent    

def transfer_to_uav_path_planning_agent():
    """立即切换至无人机路径规划Service。"""
    return uav_path_planning_agent    

def transfer_to_uav_simulation_agent():
    """立即切换至无人机飞行模拟Service。"""
    return uav_simulation_agent    

def transfer_to_save_video_frame_agent():
    """立即切换至无人机飞行视频存储Service。"""
    return save_video_frame_agent       

def transfer_to_fire_detection_agent():
    """立即切换至火灾检测Service。"""
    return fire_detection_agent     

def transfer_to_save_fire_detection_agent():
    """立即切换至火灾检测保存Service。"""
    return save_fire_detection_agent

tool_agents = [
    uav_control_agent,
    uav_path_planning_agent,
    uav_simulation_agent,
    save_video_frame_agent,
    fire_detection_agent,
    save_fire_detection_agent
]     

tool_agent_transfer_functions = [
    transfer_to_uav_control_agent,
    transfer_to_uav_path_planning_agent,
    transfer_to_uav_simulation_agent,
    transfer_to_save_video_frame_agent,
    transfer_to_fire_detection_agent,
    transfer_to_save_fire_detection_agent
]

for tool_agent in tool_agents:
    tool_agent.functions.append(transfer_to_assistant_agent)

assistant_agent.functions.extend(tool_agent_transfer_functions)
