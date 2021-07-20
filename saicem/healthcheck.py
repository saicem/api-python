import requests
import random
import json

from saicem import logger
from saicem.logger import log


class HealthCheck:
    __nickname: str
    __sn: str
    __id_card: str
    __province: str
    __city: str
    __county: str
    __street: str
    __session_id: str
    __json_data: dict
    __is_in_school: bool
    __is_leave_chengdu: bool
    __current_address: str
    __useragent_list = [
        "Mozilla/5.0 (Linux; U; Android 7.1.2; zh-cn; MI 6 Build/NXTHUAWEI) AppleWebKit/537.36 (KHTML, like Gecko)Version/4.0 MQQBrowser/9.9 Mobile Safari/537.36",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 9_3_5 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Mobile/13G36 baiduboxapp/0_01.5.2.8_enohpi_6311_046/5.3.9_1C2%8enohPi/1099a/7D4BD508A31C4692ACC31489A6AA6FAA3D5694CC7OCARCEMSHG/1",
        "Mozilla/5.0 (Linux; U; Android 4.4.4; en-us; vivo X5Max Build/KTU84P) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 UCBrowser/1.0.0.100 U3/0.8.0 Mobile Safari/534.30 AliApp(TB/6.5.0) WindVane/8.0.0 1080X1920 GCanvas/1.4.2.21",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 10_2 like Mac OS X) AppleWebKit/602.3.12 (KHTML, like Gecko) Mobile/14C92 baiduboxapp/0_01.5.2.8_enohpi_8022_2421/2.01_2C2%8enohPi/1099a/05D5623EBB692D46C9C9659B23D68FBD5C7FEB228ORMNJBQOHM/1",
        "Mozilla/5.0 (Linux; Android 8.0.0; BKL-AL00 Build/HUAWEIBKL-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/76.0.3809.89 Mobile Safari/537.36 T7/11.19 SP-engine/2.15.0 baiduboxapp/11.19.5.10 (Baidu; P1 8.0.0)",
        "Mozilla/5.0 (Linux; Android 8.1.0; vivo X20 Build/OPM1.171019.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/76.0.3809.89 Mobile Safari/537.36 T7/11.19 SP-engine/2.15.0 baiduboxapp/11.19.5.10 (Baidu; P1 8.1.0)",
        "Mozilla/5.0 (Linux; Android 9; DUK-AL20 Build/HUAWEIDUK-AL20; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/76.0.3809.89 Mobile Safari/537.36 T7/11.19 SP-engine/2.15.0 baiduboxapp/11.19.5.10 (Baidu; P1 9)",
    ]
    __temperature_list = ["36°C以下", "36.5°C~36.9°C"]

    def __init__(
            self,
            nickname: str,
            sn: str,
            id_card: str,
            province: str,
            city: str,
            county: str,
            street: str,
            is_in_school: bool,
    ) -> None:
        self.__nickname = nickname
        self.__sn = sn
        self.__id_card = id_card
        self.__province = province
        self.__city = city
        self.__county = county
        self.__street = street
        self.__json_data = {"sn": sn, "idCard": id_card, "nickname": nickname}
        self.__is_in_school = is_in_school
        self.__is_leave_chengdu = 1 - is_in_school
        self.__current_address = (
                str(province) + str(city) + str(county) + str(street)
        )

    # 获取 data 下的 session_id 别的没什么卵用 至于检测绑定 code 参数来历不明
    # 已绑定
    # {
    #     "status": true,
    #     "code": 0,
    #     "message": null,
    #     "data": {
    #         "bind": false,
    #         "sessionId": "9777f75c-aa18-46cf-b607-6f65c939e829"
    #     },
    #     "otherData": {}
    # }
    # 未绑定
    # {
    #     "status": true,
    #     "code": 0,
    #     "message": null,
    #     "data": {
    #         "bind": false,
    #         "sessionId": "9777f75c-aa18-46cf-b607-6f65c939e829"
    #     },
    #     "otherData": {}
    # }
    def get_session_id(self):
        url = "https://zhxg.whut.edu.cn/yqtjwx/api/login/checkBind"
        headers = {
            "Accept-Encoding": "gzip, deflate, br",
            "content-type": "application/json",
            "Referer": "https://servicewechat.com/wxa0738e54aae84423/9/page-frame.html",
            "X-Tag": "flyio",
            "Content-Length": "100",
            "Accept-Language": "zh-cn",
            "Connection": "keep - alive",
            "Host": "zhxg.whut.edu.cn",
            "User-Agent": random.choice(self.__useragent_list),
        }
        resp = requests.post(url=url, headers=headers, json=self.__json_data)
        self.__session_id = json.loads(resp.text)["data"]["sessionId"]
        log(resp.text, "healthCheck")

    # 绑定用户
    # 已被绑定
    # {
    #     "status": false,
    #     "code": 50000,
    #     "message": "该学号已被其它微信绑定",
    #     "data": null,
    #     "otherData": {}
    # }
    # 错误
    # {
    #     "status": false,
    #     "code": 50000,
    #     "message": "输入信息不符合",
    #     "data": null,
    #     "otherData": {}
    # }
    # 未绑定
    # {
    #     "status": true,
    #     "code": 0,
    #     "message": null,
    #     "data": {
    #         "user": {
    #             "id": 1868364,
    #             "openId": "",
    #             "sn": "0121904950722",
    #             "nickName": "青鸟飞跃",
    #             "gender": null,
    #             "language": null,
    #             "city": null,
    #             "province": null,
    #             "country": null,
    #             "avatarUrl": null,
    #             "createDate": "2021-07-19T23:43:25",
    #             "updateDate": "2021-07-20T00:06:37",
    #             "name": "余世杰",
    #             "college": "安全科学与应急管理学院",
    #             "className": "公管1902",
    #             "major": "公共事业管理",
    #             "unionId": null
    #         }
    #     },
    #     "otherData": {}
    # }
    def __get_bind_user_info(self) -> str:
        url = "https://zhxg.whut.edu.cn/yqtjwx/api/login/bindUserInfo"
        headers = {
            "Accept-Encoding": "gzip, deflate, br",
            "content-type": "application/json",
            "Referer": "https://servicewechat.com/wxa0738e54aae84423/5/page-frame.html",
            "Cookie": "JSESSIONID=%s" % self.__session_id,
            "Accept": "*/*",
            "X-Tag": "flyio",
            "Content-Length": "2",
            "Accept-Language": "zh-cn",
            "Connection": "keep - alive",
            "Host": "zhxg.whut.edu.cn",
            "User-Agent": random.choice(self.__useragent_list),
        }
        resp = requests.post(url=url, headers=headers, json=self.__json_data)
        log(resp.text, "healthCheck")
        return resp.text

    # 提交表单
    # {
    #     "status": true,
    #     "code": 0,
    #     "message": null,
    #     "data": true,
    #     "otherData": {}
    # }
    # {
    #     "status": false,
    #     "code": 50000,
    #     "message": "今日已填报",
    #     "data": null,
    #     "otherData": {}
    # }
    def __submit_form(self) -> str:
        current_address = (
                str(self.__province) + str(self.__city) + str(self.__county) + str(self.__street)
        )
        url = "https://zhxg.whut.edu.cn/yqtjwx/./monitorRegister"
        headers = {
            "Accept-Encoding": "gzip, deflate, br",
            "content-type": "application/json",
            "Referer": "https://servicewechat.com/wxa0738e54aae84423/5/page-frame.html",
            "Cookie": "JSESSIONID=%s" % self.__session_id,
            "Accept": "*/*",
            "X-Tag": "flyio",
            "Content-Length": "203",
            "Accept-Language": "zh-cn",
            "Connection": "keep - alive",
            "Host": "zhxg.whut.edu.cn",
            "User-Agent": random.choice(self.__useragent_list),
        }
        json_data = {
            "diagnosisName": "",
            "relationWithOwn": "",
            "currentAddress": current_address,
            "remark": "无",
            "healthInfo": "正常",
            "isDiagnosis": 0,
            "isFever": 0,
            "isInSchool": int(self.__is_in_school),
            "isLeaveChengdu": int(self.__is_leave_chengdu),
            "isSymptom": "0",
            "temperature": random.choice(self.__temperature_list),
            "province": self.__province,
            "city": self.__city,
            "county": self.__county,
        }
        resp = requests.post(url=url, headers=headers, json=json_data)
        log(resp.text, "healthCheck")
        return resp.text

    # 取消绑定
    # {
    #     "status": true,
    #     "code": 0,
    #     "message": null,
    #     "data": "解绑成功",
    #     "otherData": {}
    # }
    # {
    #     "status": false,
    #     "code": 50000,
    #     "message": "解绑用户不存在",
    #     "data": null,
    #     "otherData": {}
    # }
    def __cancel_bind(self):
        url = "https://zhxg.whut.edu.cn/yqtjwx/api/login/cancelBind"
        headers = {
            "Accept-Encoding": "gzip, deflate, br",
            "content-type": "application/json",
            "Referer": "https://servicewechat.com/wxa0738e54aae84423/5/page-frame.html",
            "Cookie": "JSESSIONID=%s" % self.__session_id,
            "Connection": "keep - alive",
            "Host": "zhxg.whut.edu.cn",
            "User-Agent": random.choice(self.__useragent_list),
        }
        resp = requests.post(url=url, headers=headers)
        log(resp.text, "healthCheck")

    # 健康填报全过程
    def health_check(self) -> str:
        logger.log(
            self.__nickname + self.__sn + self.__id_card + self.__province + self.__city + self.__county + self.__street + self.__is_in_school,
            "healthCheck")
        self.get_session_id()
        msg_bind = self.__get_bind_user_info()
        json_bind = json.loads(msg_bind)
        # 绑定是否成功
        try:
            if json_bind["status"]:
                msg_check = self.__submit_form()
                self.__cancel_bind()
                json_check = json.loads(msg_check)
                if json_check["status"]:
                    return "填报成功"
                else:
                    # 今日已填报
                    return json_check["message"]
            else:
                self.__cancel_bind()
                # 该学号已被其它微信绑定 输入信息不符合
                return json_bind["message"]
        finally:
            self.__cancel_bind()
            return "特殊错误"
