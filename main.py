from saicem.electric import EleSpider
from fastapi import FastAPI
from saicem.healthcheck import HealthCheck
from pydantic import BaseModel
import json
import logging

app = FastAPI()

logging.basicConfig(
    format="%(levelname)s: %(asctime)s - %(filename)s:%(module)s[line:%(lineno)d] - %(message)s",
    level=logging.INFO,
    filename="log.log",
    filemode="a",
    encoding="utf-8",
)


@app.get("/")
def test():
    return "ok"


class ElectricForm(BaseModel):
    sn: str
    id_card: str
    meter_id: str
    factorycode: str


# nickname 学号
# password 身份证后六位
# meter_id 电表ID
# factorycode 楼栋ID
# 查询得到的表单
# {
#   "ok": true,
#   "data": {
#     "remainPower": "13.35",
#     "valve": "电表--在线",
#     "ZVlaue": "10641.5",
#     "meterOverdue": "0",
#     "returncode": "SUCCESS",
#     "returnmsg": "ok"
#   }
# }
@app.post("/cwsf/")
def cwsf_query(form: ElectricForm):
    logging.info(form)
    query = EleSpider()
    res = query.get(form.sn, form.id_card, form.meter_id, form.factorycode)
    if res[0] != "{":
        # 实际还有可能是 系统开放时间早00:10到23:20
        # <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
        #
        # <meta http-equiv="X-UA-Compatible" content="IE=edge" />
        # <meta name="renderer" content="webkit">
        # <script src="/lib/jQuery 1.11.1.js" type="text/javascript"></script>
        # <script type="text/javascript" src="/js/lockscreen.js"></script>
        # <link href="/css/lockscreen.css" rel="stylesheet" type="text/css" />
        #
        # <html xmlns="http://www.w3.org/1999/xhtml">
        # <head>
        #         <title>缴费平台</title>
        #         <meta http-equiv="X-UA-Compatible" content="IE=edge" />
        #         <meta name="renderer" content="webkit">
        #         <style>
        #         /* .bk img{ margin:100px 0px 0px 500px;} */
        #         .if1{ text-align:center; font-size:24px; color:#cf1f1f; width:100%; margin:0 auto; font-weight:bold;}
        #         .if2{ text-align:center; font-size:18px; color:#333333; width:100%; margin:0 auto; padding-top:10px;}
        #         .if2 span{color:#00F; text-decoration:underline;}
        #         </style>
        # </head>
        # <body style="background-color:#eeeeee;">
        # <!-- <div class="bk"> -->
        # <div align="center">
        #     <img src="/images/system_error.png" />
        # </div>
        # <div class="if1">系统正在结账。<br>
        #     系统开放时间早00:10到23:20。</div>
        # <div class="if2"><span></span></div>
        # </body>
        # </html>
        return {"ok": False, "msg": "密码错误"}
    else:
        res_json = json.loads(res)
        try:
            remain_power = res_json["remainPower"]
            return {
                "ok": True,
                "msg": "success",
                "data": remain_power,
            }
        except:
            logging.warning(res_json)
            return {
                "ok": False,
                "msg": "解析电费失败",
            }


class HealthCheckForm(BaseModel):
    nickname: str
    sn: str
    id_card: str
    province: str
    city: str
    county: str
    street: str
    is_in_school: bool


@app.post("/check/")
def auto_health_check(check_form: HealthCheckForm):
    logging.info(check_form)
    msg, data = HealthCheck(
        check_form.nickname,
        check_form.sn,
        check_form.id_card,
        check_form.province,
        check_form.city,
        check_form.county,
        check_form.street,
        check_form.is_in_school,
    ).health_check()
    if msg == "填报成功" or msg == "今日已填报":
        return {"ok": True, "msg": msg, "data": data}
    else:
        return {"ok": False, "msg": msg}
