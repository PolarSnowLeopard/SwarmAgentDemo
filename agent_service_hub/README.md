# LLM Agent模拟微服务组合-Service Hub

## 介绍
LLM Agent模拟已注册的微服务，根据用户需求进行微服务组合，构建app.

**场景介绍**：根据用户需求，自动从已注册的微服务中选择合适的微服务组合，以实现微服务组合仿真验证。该案例包含13个微服务，涉及学生信息、天气查询、无人机控制、视频分析等用途。

**实现方式**：使用LLM Agent模拟微服务组合。
1. Cooperate Agents: 每个Agent负责一个微服务，多个Agent在一个中枢Agent的协调下协作完成任务

## 运行

1. 使用`Gradio` 可视化运行
```bash
python app.py
```