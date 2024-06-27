import requests

from pkg.order import Order
from pkg.utills.stdlog import stdlog


def msg_get(order: Order):
    '''
    用于获取订单信息。
    project_id: int
    '''

    def get_buyer_info():

        def auth_type_0():
            # 此演出无需身份电话信息
            stdlog.info("此演出无需身份电话信息")
            stdlog.warning("TODO...")
            ...

        def auth_type_1_or_2():
            # 一单一证（只能选择一个购票人）
            # 一人一证（可以选择多个购票人）
            global data_con
            try:
                data = requests.get(
                    url=f"https://show.bilibili.com/api/ticket/buyer/list?is_default",
                    headers=order.headers,
                ).json()
                data_con = data['data']
            except:
                stdlog.error("获取购票人信息失败")
                raise Exception("获取购票人信息失败")

            try:
                stdlog.info("Buyer Index: >>>")
                for i in range(len(data_con["list"])):
                    stdlog.info(
                        f"{i + 1}: 姓名: {data_con['list'][i]['name'][0:1]}** 身份证: {data_con['list'][i]['personal_id'][0:2]}*************{data_con['list'][i]['personal_id'][-1:]}")
            except:
                stdlog.error("获取购票人信息失败")
                stdlog.error(data)
                raise Exception("获取购票人信息失败")

        if order.auth_type == 0:
            # 此演出无需身份电话信息
            auth_type_0()

        elif order.auth_type == 1 or order.auth_type == 2:
            # 一单一证（只能选择一个购票人）
            # 一人一证（可以选择多个购票人）
            auth_type_1_or_2()

    def get_order_info():
        stdlog.info("演出名称: " + data_con["name"] + data_con["sale_flag"] + ">>>")
        for screen in data_con['screen_list']:
            print(f"[{screen['name']}] screen_id: {screen['id']}")
            for ticket in screen['ticket_list']:
                print(
                    f"  [{ticket['desc']}] sku_id: {ticket['id']} price: {ticket['price']} 分（{ticket['price'] // 100} 元）")

    def chick_order_auth_type():
        for _ in data["data"]["performance_desc"]["list"]:
            if _["module"] == "base_info":
                for i in _["details"]:
                    if i["title"] == "实名认证" or i["title"] == "实名登记":
                        if "一单一证" in i["content"]:
                            order.auth_type = 1
                            stdlog.warning("此演出为一单一证演出，只能选择一个购票人")
                            stdlog.info('auth_type: 1')
                            break
                        elif "一人一证" in i["content"]:
                            order.auth_type = 2
                            stdlog.warning("此演出为一人一证演出，可以选择多个购票人")
                            stdlog.info('auth_type: 2')
                            break

    data = requests.get(
        f"https://show.bilibili.com/api/ticket/project/get?version=134&id={order.project_id}&project_id={order.project_id}",
        headers=order.headers).json()
    if not data["data"]:
        return stdlog.error(data)

    data_con = data["data"]
    chick_order_auth_type()
    get_order_info()
    get_buyer_info()



