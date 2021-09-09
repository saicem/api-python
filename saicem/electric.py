import requests
import cv2
import numpy as np
from saicem.img_distinguish import char_distinguish
import logging


class EleSpider:
    __uriCode = "http://cwsf.whut.edu.cn/authImage"
    __uriLogin = "http://cwsf.whut.edu.cn/innerUserLogin?logintype=PLATFORM&nickName={}&password={}&checkCode={}"
    __uriEleFee = "http://cwsf.whut.edu.cn/queryReserve"
    __cookie = ""
    __logger = logging.getLogger("electric")

    # def __init__(self) -> None:
    #     self.__logger.info()

    def __get_code(self):
        resp = requests.get(self.__uriCode)
        self.__cookie = "=".join(resp.cookies.items()[0])
        code_img = cv2.imdecode(np.frombuffer(resp.content, np.uint8), 1)
        return code_img

    def __login(self, nick_name, password, check_code):
        uri = self.__uriLogin.format(nick_name, password, check_code)
        requests.get(uri, headers={"Cookie": self.__cookie})

    def __captcha_distinguish(self, code_img) -> str:
        im_gray = cv2.cvtColor(code_img, cv2.COLOR_BGR2GRAY)
        ret, im_inv = cv2.threshold(im_gray, 127, 255, cv2.THRESH_BINARY_INV)
        cut_image = []
        num = []
        cut_image.append(im_inv[3:15, 8:17])
        cut_image.append(im_inv[3:15, 23:32])
        cut_image.append(im_inv[3:15, 38:47])
        cut_image.append(im_inv[3:15, 53:62])
        num.append(char_distinguish(cut_image[0]))
        num.append(char_distinguish(cut_image[1]))
        num.append(char_distinguish(cut_image[2]))
        num.append(char_distinguish(cut_image[3]))
        if num.count(-1) > 0:
            check_code = -1
        else:
            check_code = "".join(num)
        return check_code

    def __get_ele_fee(self, meter_id, factorycode) -> str:
        uri = self.__uriEleFee
        resp = requests.post(uri, headers={"Cookie": self.__cookie}, data={
            "meterId": meter_id,
            "factorycode": factorycode,
        })
        return resp.text

    def get(self, nick_name, password, meter_id, factorycode):
        # self.__logger.info(nick_name, password, meter_id, factorycode)
        # 识别验证码 最多识别10次
        for i in range(10):
            code_img = self.__get_code()
            check_code = self.__captcha_distinguish(code_img)
            if check_code != -1:
                break
        # 如果识别验证码不成功 则返回
        if check_code == -1:
            return 0
        # 登录获取cookie
        self.__login(nick_name, password, check_code)
        return self.__get_ele_fee(meter_id, factorycode)

# {
#     "roomlist": {
#         "resultInfo": {
#             "result": "1",
#             "timeStamp": "2021-05-03T16:14:35.9129277+08:00",
#             "msg": "成功",
#         },
#         "remainPower": "161.55",
#         "remainName": "电量",
#         "ZVlaue": "9976.06",
#         "readTime": "2021/5/3 16:04:20",
#     },
#     "returncode": "SUCCESS",
#     "returnmsg": "ok",
# }
