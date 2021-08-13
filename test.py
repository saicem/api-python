from saicem.healthcheck import HealthCheck


class HealthCheckForm:
    nickname = "Kjlhappy"
    sn = "01219039302"
    id_card = "id_card"
    province = "江西省"
    city = "吉安市"
    county = "遂川县"
    street = "幸福路"
    is_in_school = False


def auto_health_check(check_form: HealthCheckForm):
    msg, data = HealthCheck(
        check_form.nickname,
        check_form.sn,
        check_form.id_card,
        check_form.province,
        check_form.city,
        check_form.county,
        check_form.street,
        check_form.is_in_school,
    ).health_check()
    if msg == "填报成功" or msg == "今日已填报":
        return {"ok": True, "msg": msg, "data": data}
    else:
        return {"ok": False, "msg": msg}


auto_health_check(HealthCheckForm())
