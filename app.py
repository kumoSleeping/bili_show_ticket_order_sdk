from pkg import Order
from pkg.utills.stdlog import stdlog


cookie_ = '' # 你的 cookie， 浏览器进入 https://account.bilibili.com/account/home 按下 F12 找到 cookie 复制过来 详细方法可以百度 bing google

order_1 = Order(73710, cookie_)  # 创建订单实例
order_2 = Order(73710, cookie_)

order_1.order_msg_print()  # 获取订单信息

order_1.build_order_msg(1, 134761, 398585, 12800, [1])  # 生成订单信息
order_2.build_order_msg(1, 134762, 398405, 12800, [1])



import datetime
import time


# 设置目标时间
target_time_str = '2024-07-01 11:59:53'
stdlog.info(f'目标时间: {target_time_str}')


while True:
    # 比较当前时间和目标时间
    if datetime.datetime.now() >= datetime.datetime.strptime(target_time_str, '%Y-%m-%d %H:%M:%S'):
        stdlog.warning('时间到达，开始执行')
        break

    # 等待 1 秒后再次检查
    stdlog.info(f'检查时间: {datetime.datetime.now()}')
    time.sleep(4)


def try_do(order: Order):
    try:
        order.create()
    except Exception as e:
        stdlog.error(e)


import threading

while True:
    threading.Thread(target=try_do, args=(order_1,)).start()
    threading.Thread(target=try_do, args=(order_2,)).start()
    time.sleep(0.7)





