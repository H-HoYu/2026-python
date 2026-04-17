# R14. 物件排序 attrgetter（1.14）

from operator import attrgetter

# 定義一個簡單的使用者類別
class User:
    def __init__(self, user_id):
    # 每個 User 物件都有一個 user_id 屬性
        self.user_id = user_id

# 建立多個 User 物件
users = [User(23), User(3), User(99)]

# 依照物件的 user_id 屬性排序
sorted(users, key=attrgetter('user_id'))
