import sys
from saicem.elequery import EleQuery

file, nickName, password, roomno, factorycode, area = sys.argv

query = EleQuery()
res = query.Get(nickName, password, roomno, factorycode, area)
if res == 0:
    print("wrong")
else:
    print(res)

# 0121904950722 021539 7796 E023 9001