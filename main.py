from saicem.elequery import EleQuery
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class ResOut(BaseModel):
    ok: bool = False
    data: str = "asd"


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/cwsf/", response_model=ResOut)
def read_root(nickName, password, roomno, factorycode, area):
    resOut = ResOut()
    query = EleQuery()
    res = query.Get(nickName, password, roomno, factorycode, area)
    if res == 0:
        return resOut
    else:
        resOut.ok = True
        resOut.data = res
        return resOut
