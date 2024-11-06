from dotenv import load_dotenv
import json
from swarm import Agent
from openai import OpenAI
from itertools import permutations
import base64

def uav_control():
    """获取起飞点、目的地和途径点，控制无人机飞行。

    返回:
        str: JSON格式返回的起飞点、目的地和途径点坐标。
    """
    origin_coords = (31.3385, 121.5020)
    destination_coords = (31.3389, 121.5025)
    waypoints_coords = [(31.3384, 121.5019), (31.3387, 121.5018), (31.3384, 121.5023)]
    return json.dumps({"origin_coords": origin_coords, "destination_coords": destination_coords, "waypoints_coords": waypoints_coords})

def uav_path_planning(origin_coords, destination_coords, waypoints_coords):
    """规划无人机飞行路径。找到从起点到终点经过所有途经点的最短路径。

    参数:
        origin_coords (list): 起飞点坐标。
        destination_coords (list): 目的地坐标。
        waypoints_coords (list): 途径点坐标。

    返回:
        str: JSON格式返回的最短路径（坐标列表）和最短距离。
    """

    origin_coords = (31.3385, 121.5020)
    destination_coords = (31.3389, 121.5025)
    waypoints_coords = [(31.3384, 121.5019), (31.3387, 121.5018), (31.3384, 121.5023)]

    def calculate_distance(point1, point2):
        """计算两个点之间的欧几里得距离"""
        return ((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2) ** 0.5
    
    all_points = [origin_coords] + waypoints_coords + [destination_coords]
    waypoints_permutations = permutations(waypoints_coords)
    shortest_path = None
    shortest_distance = float('inf')
    
    for perm in waypoints_permutations:
        current_path = [origin_coords] + list(perm) + [destination_coords]
        current_distance = sum(calculate_distance(current_path[i], current_path[i+1]) for i in range(len(current_path) - 1))
        
        if current_distance < shortest_distance:
            shortest_distance = current_distance
            shortest_path = current_path
    
    return json.dumps({"shortest_path": shortest_path, "shortest_distance": shortest_distance})

def uav_simulation(path_points):
    """模拟无人机飞行。

    参数:
        path_points (list): 飞行路线坐标点列表。
    返回:
        返回JSON格式返回的当前飞行点坐标和视频帧。
    """
    path_points = [[31.3385, 121.502], [31.3387, 121.5018], [31.3384, 121.5019], [31.3384, 121.5023], [31.3389, 121.5025]]
    
    for i in range(len(path_points) - 1):
        print(f"从第{i+1}个点飞往第{i+2}个点")
        current_point = [round((x+y)/2, 4) for x,y in zip(path_points[i], path_points[i+1])]
        return json.dumps({"current_point": current_point,"video_frame": "mock视频帧"})

def save_video_frame(video_frame: str):
    """保存base64编码的视频帧到数据库。

    参数:
        video_frame (str): 视频帧。

    返回:
        str: 保存成功返回视频帧，保存失败返回"fail"。
    """

    return json.dumps({"status": "success", "video_frame": video_frame})

def fire_detection(video_frame: str):
    """检测视频帧中的火灾。

    参数:
        video_frame (str): base64编码的视频帧。

    返回:
        str: 检测到火灾返回"true"，未检测到火灾返回"false"。
    """

    return json.dumps({"fire_detected": False})

def save_fire_detection(fire_detected: bool):
    """保存火灾检测结果到数据库。

    参数:
        fire_detected (bool): 检测到火灾返回"true"，未检测到火灾返回"false"。
    """

    return json.dumps({"fire_detected": fire_detected})

def exit_script():
    """结束与用户的交互。"""
    print("Exiting script...")
    # exit()


if __name__ == "__main__":
    origin_coords = (31.3385, 121.5020)
    destination_coords = (31.3389, 121.5025)
    waypoints_coords = [(31.3384, 121.5019), (31.3387, 121.5018), (31.3384, 121.5023)]
    result = uav_path_planning(origin_coords, destination_coords, waypoints_coords)
    print(result)

    i = 1
    # for result in uav_simulation(json.loads(result)["shortest_path"]):
    #     print(f"第{i}次飞行")
    #     point = json.loads(result)["current_point"]
    #     video_frame = json.loads(result)["video_frame"]
    #     print(point)
    #     print(video_frame)
    #     i += 1
