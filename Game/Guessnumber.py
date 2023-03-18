# 猜數字的函數
def Guessnumber(user_input,range_min,range_max,answer):

    try:
        user_number = int(user_input)

        if user_number < range_min or user_number > range_max:
            gamemode = False
            return "請輸入範圍內的數字！"
        
        if user_number == answer:
            return "恭喜你，猜中了！" 
        
        elif user_number < answer:
            return "太小了，再猜一次！" 
        
        else:
            return "太大了，再猜一次！" 
        
    except ValueError:
        return "請輸入一個數字！"

