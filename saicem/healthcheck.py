import logging
from typing import Tuple
import requests
import random
import json
from saicem.useragent import randAgent


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
        self.__is_leave_chengdu = bool(1 - is_in_school)

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
            "User-Agent": randAgent(),
        }
        resp = requests.post(url=url, headers=headers, json=self.__json_data)
        self.__session_id = json.loads(resp.text)["data"]["sessionId"]
        logging.info(resp.text)

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
            "User-Agent": randAgent(),
        }
        resp = requests.post(url=url, headers=headers, json=self.__json_data)
        logging.info(resp.text)
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
            str(self.__province)
            + str(self.__city)
            + str(self.__county)
            + str(self.__street)
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
            "User-Agent": randAgent(),
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
        logging.info(resp.text)
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
            "User-Agent": randAgent(),
        }
        resp = requests.post(url=url, headers=headers)
        logging.info(resp.text)

    # 健康填报全过程
    def health_check(self) -> Tuple[str, str]:
        self.get_session_id()
        msg_bind = self.__get_bind_user_info()
        json_bind = json.loads(msg_bind)
        # 绑定是否成功
        if json_bind["status"]:
            msg_check = self.__submit_form()
            self.__cancel_bind()
            json_check = json.loads(msg_check)
            if json_check["status"]:
                return "填报成功", json_bind["data"]["user"]
            else:
                # 今日已填报
                return json_check["message"], json_bind["data"]["user"]
        else:
            self.__cancel_bind()
            # 该学号已被其它微信绑定 输入信息不符合
            return json_bind["message"], None