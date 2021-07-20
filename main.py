from saicem.logger import log
from saicem.electric import EleSpider
from fastapi import FastAPI
from saicem.healthcheck import HealthCheck
import json

app = FastAPI()


@app.get("/")
def test():
    return "ok"


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
@app.get("/cwsf/")
def cwsf_query(nickname, password, meter_id, factorycode):
    query = EleSpider()
    res = query.get(nickname, password, meter_id, factorycode)
    if res[0] != "{":
        log(res, "cwsf")
        return {"code": -1}
    else:
        res_json = json.loads(res)
        # todo 为什么不行
        return {
            "code": 0,
            "data": res_json,
        }


@app.post("/check/")
def auto_health_check(nickname, sn, id_card, province, city, county, street, is_in_school):
    msg = HealthCheck(nickname, sn, id_card, province, city, county, street, is_in_school).health_check()
    if msg == "填报成功":
        return {"code": 0, "msg": msg}
    else:
        return {"code": -1, "msg": msg}
