import time


def log(msg: str):
    f = open("info.log", "a", encoding="utf8")
    f.write(
        time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        + "\n"
        + msg.replace("\t", "").replace(" ", "").replace("\n", "")
        + "\n"
    )
    f.close()
