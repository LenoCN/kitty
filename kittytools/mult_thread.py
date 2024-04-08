from threading import Thread
import datetime

# 创建 Thread 的子类
class mult_thread(Thread):
    def __init__(self, func, args):
        '''
        :param func: 可调用的对象
        :param args: 可调用对象的参数
        '''
        Thread.__init__(self)   # 不要忘记调用Thread的初始化方法
        self.func = func
        self.args = args
        self.result = None
        self.status = False

    def run(self):
        self.result = self.func(*self.args)

    def get_result(self):
        return self.result
    
class thread_with_date(mult_thread):
    def __init__(self, func, args, date=None):
        '''
        :param func: 可调用的对象
        :param args: 可调用对象的参数
        :param date: 日期参数，默认为None
        '''
        super().__init__(func, args)  # 调用父类的初始化方法
        # 如果未提供日期，则使用当前日期
        self.date = date if date is not None else datetime.datetime.now()
        
    def get_date(self):
        return self.date
    