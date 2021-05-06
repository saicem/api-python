import time


def log(msg: str, kind: str):
    f = open(
        kind + time.strftime("%y%m%d", time.localtime()) + ".log", "a", encoding="utf8"
    )
    f.write(time.strftime("%H:%M:%S", time.localtime()) + "\n" + str(msg) + "\n")
    f.close()
    print(str(msg))
