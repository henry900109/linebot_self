import hashlib
import random
import string
from datetime import datetime

def generate_monthly_password(seed: str) -> str:
    """
    根據指定的種子和當前日期產生一個每月固定的密碼。

    :param seed: 用於生成密碼的固定種子，確保密碼可重現。
    :return: 10 位的安全密碼，包含大小寫字母、數字和特殊符號。
    """
    # 獲取當前年份和月份
    now = datetime.now()
    year = now.year
    month = now.month

    # 使用種子、年份和月份產生唯一的哈希值
    hash_input = f"{seed}-{year}-{month}"
    hash_value = hashlib.sha256(hash_input.encode()).hexdigest()

    # 隨機種子
    random.seed(hash_value)

    # 定義密碼的字符集
    letters = string.ascii_letters  # 包含大小寫字母
    digits = string.digits  # 包含數字
    symbols = "!@#?%"  # 限定的特殊符號

    # 隨機選取字符
    password = (
        random.choice(letters.upper()) +  # 至少一個大寫字母
        random.choice(letters.lower()) +  # 至少一個小寫字母
        random.choice(digits) +           # 至少一個數字
        random.choice(symbols)            # 至少一個特殊符號
    )

    # 填充剩餘的字符，直到密碼長度為 10
    all_characters = letters + digits + symbols
    password += ''.join(random.choices(all_characters, k=10 - len(password)))

    # 打亂密碼的順序
    password = ''.join(random.sample(password, len(password)))

    return password

# 測試函數
if __name__ == "__main__":
    seed = profile.user_id
    password = generate_monthly_password(seed)
    print(f"本月的密碼是: {password}")
