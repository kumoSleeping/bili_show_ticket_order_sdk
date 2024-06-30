import json
import time
import ssl

from urllib import request
from urllib.request import Request
from urllib.parse import urlencode
from typing import Optional, List, Dict

from pkg.utills.stdlog import stdlog


class Order:
    ssl._create_default_https_context = ssl._create_unverified_context

    def __init__(self, project_id, cookie: str):
        '''
        虽然 self 很多类型都是 int，但 bili-api 的接口很多都是 str，这就是史
        '''
        self.cookie: str = cookie
        self.project_id: int = project_id  # 买的哪一场
        self.auth_type: Optional[int] = None  # 身份验证类型 1 一单一人 2 一单多人 0 无需验证

        self.screen_id: Optional[int] = None  # 买的哪个场次
        self.sku_id: Optional[int] = None  # 买的哪个票
        self.pay_money: Optional[int] = None  # 买的票价（单位：分）

        # self.buyer_info_raw = None  # 购票人信息（原始）
        self.buyer_info: Optional[List[Dict[str, str]]] = None  # 加入了'isBuyerInfoVerified': 'true', 'isBuyerValid': 'true'的购票人信息
        self.count: Optional[int] = None  # 购票数量（需对应购票人数量）

        self.token: Optional[str] = None  # 开票前获取的token

        # self.buyer_name = None  # 购票人姓名（无需验证时使用）
        # self.tel = None  # 购票人电话（无需验证时使用）

        self.order_type = 1  # 买票
        self.timestamp = int(round(time.time() * 1000))

        self.headers = {
            # "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0",
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_5 like Mac OS X) AppleWebKit/618.1.15.10.15 (KHTML, like Gecko) Mobile/21F90 BiliApp/77900100 os/ios model/iPhone 15 mobi_app/iphone build/77900100 osVer/17.5.1 network/2 channel/AppStore c_locale/zh-Hans_CN s_locale/zh-Hans_CH disable_rcmd/0",
            "Referer": "https://show.bilibili.com/",
            "Cache-Control": "max-age=0",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-User": "?1",
            "Sec-Fetch-Dest": "document",
            "Cookie": self.cookie,
            "Accept": "*/*",
            "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
            "Accept-Encoding": "",
            "Connection": "keep-alive"
        }

        self.finished = False

    def get_token(self):
        '''
        在 full_init 前运行用于获取 token
        '''
        url = f"https://show.bilibili.com/api/ticket/order/prepare?project_id={self.project_id}"

        # 构建请求payload
        payload = {
            "project_id": str(self.project_id),
            "count": str(self.count),
            "order_type": "1",
            "screen_id": str(self.screen_id),
            "sku_id": str(self.sku_id),
            "token": ""
        }

        json_payload = urlencode(payload).replace("%27true%27", "true").replace("%27", "%22").encode()
        res = request.urlopen(Request(url, headers=self.headers, method="POST", data=json_payload), timeout=120)
        data = json.loads(res.read().decode())

        if not data["data"]:
            stdlog.error("失败信息: " + data["msg"])
            return False
        print(data)
        self.token = data["data"]["token"]
        print(self.token)
        return True

    def full_init(self, auth_type: int, screen_id: int, sku_id: int, pay_money: int, buyer_info: List[dict], count: int):
        '''
        正式购票前的初始化信息
        '''
        self.auth_type = auth_type
        self.screen_id = screen_id
        self.sku_id = sku_id
        self.pay_money = pay_money
        self.buyer_info = buyer_info
        self.count = count

    def build_order_msg(self,auth_type: int, screen_id: int, sku_id: int, pay_money: int,
                        buyer_index_list: List[int]):
        '''
        构建购票信息
        project_id: 项目ID
        auth_type: 身份验证类型 1 一单一人 2 一单多人 0 无需验证（暂不支持）
        screen_id: 场次ID
        sku_id: 票ID
        pay_money: 价格（单位：分！）单价！一张的价格！
        buyer_index: 购票人索引，但是是从1开始的，例如 [1, 2] ，需要先在 msg_get 中获取，需要 cookie 的购买人是相同的
        '''

        def bulid_buyer_msg() -> List[Dict[str, str]]:
            '''
            构建购票人信息
            '''
            if auth_type == 0:
                raise Exception("暂不支持")
            elif auth_type == 1 or auth_type == 2:
                try:
                    res = request.urlopen(Request(f"https://show.bilibili.com/api/ticket/buyer/list?is_default", headers=self.headers), timeout=120)
                    data = json.loads(res.read().decode())
                    data_con = data['data']
                except:
                    raise Exception("获取购票人信息失败")

                buyer_info_list = []
                for i in buyer_index_list:
                    index = i - 1
                    buyer_info_raw: dict = data_con["list"][index]
                    # 使用 update 方法更新 buyer_info_raw 字典
                    buyer_info_raw.update({'isBuyerInfoVerified': 'true', 'isBuyerValid': 'true'})  # bili-api 要加的构思
                    # 将更新后的字典赋值给 buyer_info_dict
                    buyer_info_dict = buyer_info_raw
                    # 将 buyer_info_dict 放入列表中
                    buyer_info_list.append(buyer_info_dict)
                return buyer_info_list
            else:
                raise Exception("auth_type 错误")

        buyer_info = bulid_buyer_msg()
        count = len(buyer_info)
        self.full_init(auth_type, screen_id, sku_id, pay_money, buyer_info, count)

    def create(self):
        if self.finished:
            stdlog.warning("订单已完成，无需重复下单")
            return

        def auth_type_0():
            # 此演出无需身份电话信息
            ...

        def auth_type_1_and_2():
            # 一单一证（只能选择一个购票人）
            # 一人一证（可以选择多个购票人）

            payload = {
                "buyer_info": self.buyer_info,
                "count": str(self.count),
                "order_type": 1,
                "pay_money": self.pay_money * self.count,
                "project_id": str(self.project_id),
                "screen_id": self.screen_id,
                "sku_id": self.sku_id,
                "timestamp": int(round(time.time() * 1000)),
                "token": self.token,
                "deviceId": "",
            }

            json_payload = urlencode(payload).replace("%27true%27", "true").replace("%27", "%22").encode()
            url = f"https://show.bilibili.com/api/ticket/order/createV2?project_id={self.project_id}"
            res = request.urlopen(Request(url, headers=self.headers, method="POST", data=json_payload),timeout=120)

            try:
                data = json.loads(res.read().decode())
                if data["errno"] == 0:
                    stdlog.success("下单成功！")
                    stdlog.warning("为防止误判，将继续检查票务状态")
                elif data["errno"] == 100079 or data["errno"] == 100048:
                    stdlog.success(f'次订单已存在，无需重复下单！{data}')
                    self.finished = True
                    return
                elif data["errno"] == 100051 or data["errno"] == 100041:
                    self.token = self.get_token()
                    stdlog.warning("token 过期，已重新获取")
                elif data["errno"] == 3:
                    stdlog.warning("慢一点（强制5秒）")
                    time.sleep(2.8)

                elif data["errno"] == 100001:
                    stdlog.warning("👋📱👋")
                elif data["errno"] == 100016:
                    stdlog.error("项目不可售")
                elif data["errno"] == 219:
                    stdlog.info("库存不足")
                elif data["errno"] == 100009:
                    stdlog.warning("无票")
                elif data["errno"] == 100017:
                    stdlog.warning("票种不可售")
                else:
                    stdlog.error(f'下单失败！{data}')

            except json.JSONDecodeError as e:
                stdlog.error(f'JSON解析错误: {e}')
                stdlog.error(f'响应内容: {res.read().decode()}')

        if self.auth_type == 0:
            auth_type_0()
        else:
            auth_type_1_and_2()












