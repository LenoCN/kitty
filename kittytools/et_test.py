from unittest import expectedFailure
import easytrader

user = easytrader.use('universal_client')
user.connect(path='C:\\同花顺软件\\同花顺\\xiadan.exe')
#user.prepare(user='8069170012', password='123456', comm_password='华泰通讯密码，其他券商不用',exe_path=r"C:\同花顺软件\同花顺\xiadan.exe")
print(user.balance)