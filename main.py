from saicem.logger import log
from saicem.elequery import EleQuery
from fastapi import FastAPI
import json

app = FastAPI()


@app.get("/")
def read_root():
    return "ok"


@app.get("/cwsf/")
def read_root(nickName, password, roomno, factorycode, area):
    query = EleQuery()
    res = query.Get(nickName, password, roomno, factorycode, area)
    if res[0] != "{":
        return {"ok": False}
    else:
        resJson = json.loads(res)
        return {
            "ok": True,
            "readTime": resJson["roomlist"]["readTime"],
            "remainPower": resJson["roomlist"]["remainPower"],
        }
