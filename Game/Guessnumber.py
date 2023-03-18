


# 猜數字的函數
def Guessnumber(user_input,range_min,range_max,answer):



    try:
        user_number = int(user_input)

        if user_number < range_min or user_number > range_max:
            return "請輸入範圍內的數字！" + str(answer)
        
        if user_number == answer:
            return "恭喜你，猜中了！" + str(answer)
        
        elif user_number < answer:
            return "太小了，再猜一次！" + str(answer)
        
        else:
            return "太大了，再猜一次！" + str(answer)
        
    except ValueError:
        return "請輸入一個數字！"

