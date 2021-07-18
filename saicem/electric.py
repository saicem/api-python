import requests
import cv2
import numpy as np
from saicem.imgDistinguish import char_distinguish


class EleSpider:
    __uriCode = "http://cwsf.whut.edu.cn/authImage"
    __uriLogin = "http://cwsf.whut.edu.cn/innerUserLogin?logintype=PLATFORM&nickName={}&password={}&checkCode={}"
    __uriEleFee = "http://cwsf.whut.edu.cn/querySydl?roomno={}&factorycode={}&area={}"
    __cookie = ""

    def __get_code(self):
        resp = requests.get(self.__uriCode)
        self.__cookie = "=".join(resp.cookies.items()[0])
        code_img = cv2.imdecode(np.frombuffer(resp.content, np.uint8), 1)
        return code_img

    def __login(self, nick_name, password, check_code):
        uri = self.__uriLogin.format(nick_name, password, check_code)
        requests.get(uri, headers={"Cookie": self.__cookie})

    def __image_distinguish(self, code_img):
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

    def __get_ele_fee(self, roomno, factorycode, area):
        uri = self.__uriEleFee.format(roomno, factorycode, area)
        resp = requests.get(uri, headers={"Cookie": self.__cookie})
        return resp.text

    def get(self, nick_name, password, roomno, factorycode, area):
        # 识别验证码 最多识别10次
        for i in range(10):
            code_img = self.__get_code()
            check_code = self.__image_distinguish(code_img)
            if check_code != -1:
                break
        # 如果识别验证码不成功 则返回
        if check_code == -1:
            return 0
        # 登录获取cookie
        self.__login(nick_name, password, check_code)
        return self.__get_ele_fee(roomno, factorycode, area)


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
