import uuid
from datetime import datetime
from flask import Blueprint, request
from flaskPro.common.db import Execute

team = Blueprint("team", __name__, url_prefix="/team")


def get_db_list(sql):
    return Execute().get_data_list(sql)


def get_db_info(sql):
    return Execute().get_data_one(sql)


@team.route("/teamList", methods=["GET"])
def get_team_list():
    data = request.args
    page_size = int(data.get('page_size')) if data.get('page_size') else 10
    page_number = int(data.get('page_number')) if data.get('page_number') else 0
    if page_number:
        page_number = (page_number - 1) * page_size
    team_name = data.get('name') if data.get('name') else None
    if team_name:
        sql = (f"select * from race_team where name like '%{team_name}%' "
               f"order by create_at limit {page_size} offset {page_number}")
    else:
        sql = f"select * from race_team order by create_at limit {page_size} offset {page_number}"
    print(sql)
    res = get_db_list(sql)
    data = []
    for info in res:
        data.append(
            {
                "id": info[0],
                "name": info[1],
                "desc": info[2],
                "create_at": info[3],
                "update_at": info[4],
            }
        )
    return {
        "result": "success",
        "data": data
    }


@team.route("/teamDetail/<name>", methods=["GET"])
def get_team_detail(name):
    sql = f"select * from race_team where name='{name}'"
    res = get_db_info(sql)
    if len(res) > 0:
        return {
            "result": "success",
            "data": {
                "id": res[0],
                "name": res[1],
                "desc": res[2],
                "create_at": res[3],
                "update_at": res[4],
            }
        }
    else:
        return {
            "result": "failed",
            "msg": "该队伍不存在"
        }


@team.route("/teamCreate", methods=["POST"])
def create_team():
    data = request.get_json()
    name = data["name"]
    desc = data["desc"]
    sql = f"select * from race_team where name = '{name}'"
    if len(get_db_list(sql)) > 0:
        return {"result": "failed", "msg": "该队伍已存在"}, 400
    team_id = uuid.uuid4()
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sql = (f"insert into race_team (id, name, `desc`, create_at, update_at) values"
           f"('{team_id}', '{name}', '{desc}', '{current_time}', '{current_time}')")
    Execute().write_data_info(sql)
    return {
        "result": "success",
        "data": {
            "id": team_id,
            "name": name,
            "desc": desc,
            "create_at": current_time,
            "update_at": current_time,
        }
    }
