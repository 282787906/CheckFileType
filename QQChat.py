# -*- coding: utf-8 -*-

# onQQMessage ：必须的注册函数的函数名称
# bot         ：QQBot 对象，提供 List/SendTo/Stop/Restart 等接口
# contact     ：QContact 对象，消息的发送者，具有 ctype/qq/uin/nick/mark/card/name 等属性
# member      ：QContact 对象，仅当本消息为 群消息或讨论组消息 时有效，代表实际发消息的成员
# content     ：str 对象，消息内容
from qqbot import RunBot


def onQQMessage(bot, contact, member, content):
    if content == "-hello":
        bot.SendTo(contact, "你好，我是小罗机器人")
    elif content == '-stop':
        bot.SendTo(contact, "小罗机器人已关闭")
        bot.Stop()
RunBot()
