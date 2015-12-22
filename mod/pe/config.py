PE_LOGIN_URL = "http://58.192.114.239/student/studentFrame.jsp"
PE_PC_URL = "http://58.192.114.239/student/queryCheckInfo.jsp"

CONNECT_TIME_OUT = 3

API_SERVER_HOST = ''
API_SERVER_PORT = 
API_SERVER_KEY = ''

SECRET_KEY1 = 
SECRET_KEY2 = 
A = hex(SECRET_KEY1^SECRET_KEY2)[2:] + API_SERVER_KEY + hex(SECRET_KEY1)[2:]
daymap = {'Mon':1, 'Tue':2, 'Wed':3, 'Thu':4, 'Fri':5, 'Sat':6, 'Sun':7}
finay_day = '2016-01-08'
final_date = 5