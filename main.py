from saicem.logger import log
from saicem.electric import EleSpider
from fastapi import FastAPI
from saicem.healthcheck import HealthCheck
import json

app = FastAPI()


@app.get("/")
def test():
    return "ok"


@app.get("/cwsf/")
def cwsf_query(nickname, password, roomno, factorycode, area):
    query = EleSpider()
    res = query.get(nickname, password, roomno, factorycode, area)
    if res[0] != "{":
        log(res, "cwsf")
        return {"ok": False}
    else:
        res_json = json.loads(res)
        return {
            "ok": True,
            "readTime": res_json["roomlist"]["readTime"],
            "remainPower": res_json["roomlist"]["remainPower"],
        }


@app.post("/check/")
def auto_health_check(nickname, sn, id_card, province, city, county, street, is_in_school):
    msg = HealthCheck(nickname, sn, id_card, province, city, county, street, is_in_school).health_check()
    if msg == "填报成功":
        return {"code": 0, "msg": msg}
    else:
        return {"code": -1, "msg": msg}
