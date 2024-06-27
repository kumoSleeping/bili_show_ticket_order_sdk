# bili_show_ticket_order_sdk

> 一个研究B站会员购购票构思 API 的项目

## ⚠️ 注意

**本项目正处在一个 `开发` 阶段。**   

如果你是想要用一些 `不正当` 手段抢票的用户，这个 SDK 并不适合你。  
本 SDK 仅供学习研究使用。

## 📅 TODO

- [ ] 杂项完善
- [ ] 验证码 ticket 抓取
- [ ] 实体票购买
- [ ] 非实名制购票


## 💻 关于

项目采用 OOP、DI、的设计模式，有一部分类型注解，虽然很多地方称不上规范，但是尽量保证可读。  
必要的地方注释可能有遗漏欢迎补充。


> 项目思路来源 fengx1a0/Bilibili_show_ticket_auto_order

十分感谢原作者的分享，让我认识到 bilibili 会员购购票的 API 构思请求是多么的抽象。  
虽然说原项目的代码规范程度也很难评价，但是还是十分感谢原作者所给我带来的帮助。  


## 📦 依赖

只需要安装 高版本的 Python3 即可，不需要额外的依赖。

## 🚀 使用

```py
from pkg import Order, msg_get

'''
压力环境弹出验证码请无视，约 10000 次尝试后会有强制验证码，目前没写解决方法，建议换 token
'''

cookie_ = '' # 你的 cookie， 浏览器进入 https://account.bilibili.com/account/home 按下 F12 找到 cookie 复制过来 详细方法可以百度 bing google

order_1 = Order(73710, cookie_)
order_2 = Order(73710, cookie_)

msg_get(order_1)  # 先使用 msg_get 获取订单信息

order_1.build_order_msg(1, 134761, 398585, 12800, [1])  # 生成订单信息
order_2.build_order_msg(1, 134762, 398405, 12800, [1])

# 创建订单
# import time
#
# while True:
#     order_1.create()
#     order_2.create()
#     time.sleep(1)

# 并发执行
# import threading
# import time
#
# while True:
#     # 并发执行
#     threading.Thread(target=order_1.create).start()
#     threading.Thread(target=order_2.create).start()
#     time.sleep(1)


# 并发 5 条线程抢购，但不推荐这样做，也许被ban IP
# import threading
# import time
#
# while True:
#     # 并发 5 条线程抢购
#     for i in range(5):
#         threading.Thread(target=order_1.create).start()
#         threading.Thread(target=order_2.create).start()
#     time.sleep(2)


# import datetime
# import time
# from pkg.utills import stdlog

# 
# 
# # 设置目标时间
# target_time_str = '2024-06-27 20:35:00'
# stdlog.info(f'目标时间: {target_time_str}')
# 
# while True:
#     # 比较当前时间和目标时间
#     if datetime.datetime.now() >= datetime.datetime.strptime(target_time_str, '%Y-%m-%d %H:%M:%S'):
#         stdlog.warning('时间到达，开始执行')
#         break
# 
#     # 等待 1 秒后再次检查
#     time.sleep(0.1)
# 
# 
# while True:
#     order_1.create()
#     order_2.create()
#     time.sleep(0.7)




```