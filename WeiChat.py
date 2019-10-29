import itchat
import time
hotReload = True  ##保留登录登录状态，段时间内不会自动登录

itchat.auto_login()

time.sleep(3)


itchat.logout()
# while True:
#     itchat.send('hello',toUserName='filehelper')  ##对手机助手发送消息
#     # itchat.send_file('/etc/passwd', toUserName='filehelper')  ##对手机助手发送文件
#     time.sleep(3)  ##每3秒发送一次