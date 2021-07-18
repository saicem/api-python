from saicem.logger import log
from saicem.elespider import EleSpider
from fastapi import FastAPI
from saicem.healthcheck import health_check
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


@app.get("/check/")
def auto_health_check(nickname, sn, id_card):
    isvalid_user, msg = health_check(nickname, sn, id_card)
    return {"ok": isvalid_user, "msg": msg}
