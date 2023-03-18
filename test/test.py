import json
def test():
    return "hello world"
def profile(profile):
    name = profile.display_name
    # id = profile.user_id
    # pic = profile.picture_url
    #m = profile.status_message
        #     'profile_name': profile.display_name,
        # 'profile_id': profile.user_id,
    return name 
def group(profile):
    id = profile.group_id  # 群組 ID
    name = profile.group_name  # 群組名稱
    pic = profile.picture_url # 群組照片 URL
    return name 
