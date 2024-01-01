import uuid
from datetime import datetime
from flask import Blueprint, request
from flaskPro.common.db import Execute

team = Blueprint("team", __name__, url_prefix="/team")


@team.route("/teamList", methods=["GET"])
def get_team_list():
    data = request.args
    page_size = int(data.get('page_size')) if data.get('page_size') else 10
    page_number = int(data.get('page_number')) if data.get('page_number') else 0
    if page_number:
        page_number = (page_number - 1) * page_size
    team_name = data.get('name') if data.get('name') else None
    if team_name:
        sql = (f"select * from race_team left join race_member rm on race_team.id=rm.team_id "
               f"where name like '%{team_name}%' order by create_at limit {page_size} offset {page_number}")
    else:
        sql = f"select * from race_team order by create_at limit {page_size} offset {page_number}"
    res = Execute().get_data_list(sql)
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


@team.route("/teamDetail/<team_id>", methods=["GET"])
def get_team_detail(team_id):
    sql = f"select * from race_team left join race_member rm on race_team.id=rm.team_id where race_team.id='{team_id}'"
    res = Execute().get_data_list(sql)
    if len(res) > 0:
        member_list = []
        data = {
            "id": res[0][0],
            "name": res[0][1],
            "desc": res[0][2],
            "create_at": res[0][3],
            "update_at": res[0][4],
            "member_list": member_list
        }
        for info in res:
            member_list.append(
                {
                    "id": info[-7],
                    "name": info[-6],
                    "desc": info[-5],
                    "work_code": info[-4],
                    "create_at": info[-3],
                    "update_at": info[-2],
                }
            )
        return {
            "result": "success",
            "data": data
        }
    else:
        return {
            "result": "failed",
            "msg": "该队伍不存在"
        }, 400


@team.route("/teamCreate", methods=["POST"])
def create_team():
    data = request.get_json()
    name = data["name"]
    desc = data["desc"]
    sql = f"select * from race_team where name = '{name}'"
    if len(Execute().get_data_list(sql)) > 0:
        return {"result": "failed", "msg": "该队伍已存在"}, 400
    team_id = uuid.uuid4()
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sql = (f"insert into race_team (id, name, `desc`, create_at, update_at) values"
           f"('{team_id}', '{name}', '{desc}', '{current_time}', '{current_time}')")
    Execute().write_data_info(sql)
    return get_team_detail(team_id)


@team.route('/teamUpdate', methods=['POST'])
def update_team():
    data = request.get_json()
    team_id = data["id"]
    name = data["name"]
    desc = data["desc"]
    sql = f"select * from race_team where id = '{team_id}'"
    if len(Execute().get_data_list(sql)) < 1:
        return {"result": "failed", "msg": "该队伍不存在"}, 400
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sql = f"update race_team set name='{name}', `desc`='{desc}', update_at='{current_time}' where id='{team_id}'"
    Execute().write_data_info(sql)
    return get_team_detail(team_id)


@team.route('/teamDelete/<team_id>', methods=['DELETE'])
def delete_team(team_id):
    sql = f"select * from race_team where id = '{team_id}'"
    if len(Execute().get_data_list(sql)) < 1:
        return {"result": "failed", "msg": "该队伍不存在"}, 400
    sql = f"delete from race_team where id='{team_id}'"
    Execute().write_data_info(sql)
    return {}, 204


@team.route("/team/addMember", methods=['POSTs'])
def team_add_member():
    data = request.get_json()
    team_id = data['team_id']
    member_list = set(data['member_list'])
    sql = (f"select rt.id, race_member.id from race_member left join race_team rt "
           f"on rt.id = race_member.team_id where rt.id='{team_id}'")
    res = Execute().get_data_list(sql)
    if 8 - len(res) > len(set(member_list)):
        return {'status': 'failed', 'msg': '队伍上限为8人'}, 400
    for member_id in member_list:
        sql = f"update race_member set team_id='{team_id}' where member_id='{member_id}'"
        Execute().write_data_info(sql)
    return {'status': 'success', 'msg': '添加成功'}


