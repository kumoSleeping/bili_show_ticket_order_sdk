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






