import server.notify as sn
def profile(profile):
    id = profile.user_id
    # pic = profile.picture_url
    try:
        m = profile.status_message
    except:
        m = ""

    name = profile.display_name
    relpy_text = "你叫 " + name 
    sn.notify(relpy_text+"\n"+id)
    if name == "卓子揚":
        return "你叫 " + name +",是個帥哥!"
    
    else:


        if m != "":
            return relpy_text
        else:
            # return "你叫 " + name +"\n 你總說" + m
            return relpy_text