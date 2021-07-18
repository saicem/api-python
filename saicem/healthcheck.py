import requests
import random
import json
from saicem.logger import log

useragent_list = [
    "Mozilla/5.0 (Linux; U; Android 7.1.2; zh-cn; MI 6 Build/NXTHUAWEI) AppleWebKit/537.36 (KHTML, like Gecko)Version/4.0 MQQBrowser/9.9 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 9_3_5 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Mobile/13G36 baiduboxapp/0_01.5.2.8_enohpi_6311_046/5.3.9_1C2%8enohPi/1099a/7D4BD508A31C4692ACC31489A6AA6FAA3D5694CC7OCARCEMSHG/1",
    "Mozilla/5.0 (Linux; U; Android 4.4.4; en-us; vivo X5Max Build/KTU84P) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 UCBrowser/1.0.0.100 U3/0.8.0 Mobile Safari/534.30 AliApp(TB/6.5.0) WindVane/8.0.0 1080X1920 GCanvas/1.4.2.21",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 10_2 like Mac OS X) AppleWebKit/602.3.12 (KHTML, like Gecko) Mobile/14C92 baiduboxapp/0_01.5.2.8_enohpi_8022_2421/2.01_2C2%8enohPi/1099a/05D5623EBB692D46C9C9659B23D68FBD5C7FEB228ORMNJBQOHM/1",
    "Mozilla/5.0 (Linux; Android 8.0.0; BKL-AL00 Build/HUAWEIBKL-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/76.0.3809.89 Mobile Safari/537.36 T7/11.19 SP-engine/2.15.0 baiduboxapp/11.19.5.10 (Baidu; P1 8.0.0)",
    "Mozilla/5.0 (Linux; Android 8.1.0; vivo X20 Build/OPM1.171019.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/76.0.3809.89 Mobile Safari/537.36 T7/11.19 SP-engine/2.15.0 baiduboxapp/11.19.5.10 (Baidu; P1 8.1.0)",
    "Mozilla/5.0 (Linux; Android 9; DUK-AL20 Build/HUAWEIDUK-AL20; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/76.0.3809.89 Mobile Safari/537.36 T7/11.19 SP-engine/2.15.0 baiduboxapp/11.19.5.10 (Baidu; P1 9)",
]


def request_session_id(json_data):
    url = "https://zhxg.whut.edu.cn/yqtjwx/api/login/checkBind"

    headers = {"Accept-Encoding": "gzip, deflate, br", "content-type": "application/json",
               "Referer": "https://servicewechat.com/wxa0738e54aae84423/9/page-frame.html", "X-Tag": "flyio",
               "Content-Length": "100", "Accept-Language": "zh-cn", "Connection": "keep - alive",
               "Host": "zhxg.whut.edu.cn", "User-Agent": random.choice(useragent_list)}
    resp = requests.post(url=url, headers=headers, json=json_data)
    log(resp.text, "healthCheck")
    return resp.text


def request_bind_user_info(session_id, json_data):
    url = "https://zhxg.whut.edu.cn/yqtjwx/api/login/bindUserInfo"
    headers = {"Accept-Encoding": "gzip, deflate, br", "content-type": "application/json",
               "Referer": "https://servicewechat.com/wxa0738e54aae84423/5/page-frame.html",
               "Cookie": "JSESSIONID=%s" % session_id, "Accept": "*/*", "X-Tag": "flyio", "Content-Length": "2",
               "Accept-Language": "zh-cn", "Connection": "keep - alive", "Host": "zhxg.whut.edu.cn",
               "User-Agent": random.choice(useragent_list)}
    resp = requests.post(url=url, headers=headers, json=json_data)
    log(resp.text, "healthCheck")
    return resp.text


def request_monitor_register(name, session_id, province, city, county, street):
    current_address = str(province) + str(city) + str(county) + str(street)
    url = "https://zhxg.whut.edu.cn/yqtjwx/./monitorRegister"
    headers = {"Accept-Encoding": "gzip, deflate, br", "content-type": "application/json",
               "Referer": "https://servicewechat.com/wxa0738e54aae84423/5/page-frame.html",
               "Cookie": "JSESSIONID=%s" % session_id, "Accept": "*/*", "X-Tag": "flyio", "Content-Length": "203",
               "Accept-Language": "zh-cn", "Connection": "keep - alive", "Host": "zhxg.whut.edu.cn",
               "User-Agent": random.choice(useragent_list)}
    json_data = {
        "diagnosisName": "",
        "relationWithOwn": "",
        "currentAddress": current_address,
        "remark": "无",
        "healthInfo": "正常",
        "isDiagnosis": 0,
        "isFever": 0,
        "isInSchool": "1",
        "isLeaveChengdu": 0,
        "isSymptom": "0",
        "temperature": "36.5°C~36.9°C",
        "province": province,
        "city": city,
        "county": county,
    }
    resp = requests.post(url=url, headers=headers, json=json_data)
    log(resp.text, "healthCheck")
    return resp.text


def cancel_bind(session_id):
    url = "https://zhxg.whut.edu.cn/yqtjwx/api/login/cancelBind"
    headers = {"Accept-Encoding": "gzip, deflate, br", "content-type": "application/json",
               "Referer": "https://servicewechat.com/wxa0738e54aae84423/5/page-frame.html",
               "Cookie": "JSESSIONID=%s" % session_id, "Connection": "keep - alive", "Host": "zhxg.whut.edu.cn",
               "User-Agent": random.choice(useragent_list)}
    resp = requests.post(url=url, headers=headers)
    log(resp.text, "healthCheck")
    return resp.text


def health_check(_nickname, _sn, _id_card):
    nickname = _nickname  # "微信昵称"
    sn = _sn  # "学号"
    id_card = _id_card  # "身份证后六位"
    province = "湖北省"
    city = "武汉市"
    county = "洪山区"
    street = "广场东二路"
    json_data = {"sn": sn, "idCard": id_card, "nickname": nickname}
    msg_session = request_session_id(json_data)
    session_id = json.loads(msg_session)["data"]["sessionId"]
    msg_bind = request_bind_user_info(session_id, json_data)
    json_bind = json.loads(msg_bind)
    if json_bind["status"]:
        msg_check = request_monitor_register(
            nickname, session_id, province, city, county, street
        )
        msg_cancel = cancel_bind(session_id)
        json_check = json.loads(msg_check)
        if json_check["status"]:
            append_info = "填报成功"
        else:
            append_info = json_check["message"]
        return True, "{}\n{}\n{}\n{}\n{}\n".format(
            append_info, msg_session, msg_bind, msg_check, msg_cancel
        )
    else:
        msg_cancel = cancel_bind(session_id)
        return False, "{}\n{}\n{}\n".format(msg_session, msg_bind, msg_cancel)
