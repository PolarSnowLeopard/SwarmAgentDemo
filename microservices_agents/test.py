from tools import *

print("-------------------------------")
print("get_user_id()")
print(get_user_id("瀚海雪豹"))

print("-------------------------------")
print("get_user_info()")
print(get_user_info("12345"))

print("-------------------------------")
print("generate_education_description()")

education_description = generate_education_description("复旦大学", "计算机科学与技术")
print(education_description)

print("-------------------------------")
print("summarize_recent_life_status()")
user_post_history = [
            {"time": "2024-05-01", "title": "五一假期，开始肝毕设论文！"},
            {"time": "2024-05-03", "title": "快死了，腰酸背痛"},
            {"time": "2024-05-07", "title": "通宵一星期，终于搞定初稿了"},
            {"time": "2024-05-12", "title": "开始做答辩PPT，虽然但是，五分钟怎么讲的完啊"},
            {"time": "2024-05-19", "title": "怎么论文还要改啊，想死"},
            {"time": "2024-06-01", "title": "明天答辩，躺床上睡不着怎么办"},
            {"time": "2024-06-02", "title": "昨天晚上睡不着，通宵了，马上轮到我答辩，已经快飞升了"},
            {"time": "2024-06-02", "title": "答辩结束！先睡他三天！"},
        ]
life_status = summarize_recent_life_status(user_post_history)
print(life_status)

print("-------------------------------")
print("send_email()")
email = "test@test.com"
print(send_email(email, education_description, life_status))