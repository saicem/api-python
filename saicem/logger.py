import time


def log(msg: str, kind: str):
    file_name = kind + time.strftime("%Y%m%d", time.localtime()) + ".log"
    f = open(file_name, "a", encoding="utf8")
    f.write(time.strftime("%H:%M:%S", time.localtime()) + "\n" + str(msg) + "\n")
    f.close()
    print(str(msg))
