# bili_show_ticket_order_sdk

> 一个研究B站会员购购票构思 API 的项目

## ⚠️ 注意

**本项目正处在一个 `开发` 阶段。**   

如果你是想要用一些 `不正当` 手段抢票的用户，这个 SDK 并不适合你。  
本 SDK 仅供学习研究使用。


## 🤔 项目原理

1. B站的验证码只是摆设，不用管
2. B站不让电脑只是使用AU区分，不堵API

## 🚁 战绩

- 2021-06-29 BW 5 个订单中 抢到一个（

> bw人太多啦！完全是抽奖啊😭

## 📅 计划

- TODO
  - [ ] 错误处理完善
  - [ ] 实体票购买
- 不TODO
  - [ ] 非实名制购票
  - [ ] 验证码 ticket 抓取

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

```