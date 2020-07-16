# @Time : 2020/7/16 10:13 上午
# @Author : HansomeBo
# @File : work.py
# @Software: PyCharm
class Work:

    def __init__(self, work, date):
        self.work = work
        self.date = date

    def __str__(self):
        return self.date + ":" + self.work
