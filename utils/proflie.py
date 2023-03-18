def profile(profile):
    # id = profile.user_id
    # pic = profile.picture_url
    #m = profile.status_message

    name = profile.display_name
    if name != "卓子揚":
        return "你叫 " + name 
    else:
        return "你叫 " + name +",是個帥哥!"