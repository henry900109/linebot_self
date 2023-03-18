def test():
    return "hello world"
def profile(profile):
    name = profile.display_name
    id = profile.user_id
    pic = profile.picture_url
    m = profile.status_message
    return name +"\n"+ id +"\n" + pic +"\n" + m