import time


def log(msg: str, kind: str):
    fileName = kind + time.strftime("%Y%m%d", time.localtime()) + ".log"
    f = open(fileName, "a", encoding="utf8")
    f.write(time.strftime("%H:%M:%S", time.localtime()) + "\n" + str(msg) + "\n")
    f.close()
    print(str(msg))
