from saicem.logger import log
from saicem.elespider import EleSpider
from fastapi import FastAPI
from saicem.healthcheck import healthCheck
import json

app = FastAPI()


@app.get("/")
def test():
    return "ok"


@app.get("/cwsf/")
def cwsfQuery(nickName, password, roomno, factorycode, area):
    query = EleSpider()
    res = query.Get(nickName, password, roomno, factorycode, area)
    if res[0] != "{":
        log(res, "cwsf")
        return {"ok": False}
    else:
        resJson = json.loads(res)
        return {
            "ok": True,
            "readTime": resJson["roomlist"]["readTime"],
            "remainPower": resJson["roomlist"]["remainPower"],
        }


@app.get("/check/")
def autoHealthCheck(_nickname, _sn, _idCard):
    msg = healthCheck(_nickname, _sn, _idCard)
    return {"ok": True, "msg": msg}
