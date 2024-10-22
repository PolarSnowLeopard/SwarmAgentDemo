from tools import *

print("-------------------------------")
print("get_user_id()")
print(get_user_id("瀚海雪豹"))

print("-------------------------------")
print("get_user_info()")
print(get_user_info("12345"))

print("-------------------------------")
print("generate_user_profile()")
user_base_info = MOCK_USER_INFO.copy()
user_base_info.pop("post_history")
user_profile = generate_user_profile(user_base_info)
print(user_profile)

print("-------------------------------")
print("summarize_recent_life_status()")
user_post_history = MOCK_USER_INFO['post_history']
life_status = summarize_recent_life_status(user_post_history)
print(life_status)

print("-------------------------------")
print("send_email()")
email = MOCK_USER_INFO['email']
print(send_email(email, user_profile, life_status))