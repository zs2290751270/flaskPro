import uuid
from datetime import datetime
from flask import Blueprint, request
from flaskPro.common.db import Execute

member = Blueprint('member', __name__, url_prefix='/member')


@member.route('/memberCreate', methods=['POST'])
def create_member():
    data = request.get_json()
    name = data['name']
    desc = data['desc']
    work_code = data['work_code']
    team_id = data['team_id']
    sql = f"select * from race_member where name = '{name}'"
    if len(Execute().get_data_list(sql)) > 0:
        return {'status': 'failed', 'msg': '该选手已存在'}, 400
    member_id = uuid.uuid4()
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if data['team_id']:
        sql = (f"insert into race_member (id, name, `desc`, work_code, create_at, update_at, team_id) values "
               f"('{member_id}','{name}','{desc}','{work_code}','{current_time}','{current_time}','{team_id}')")
    else:
        sql = (f"insert into race_member (id, name, `desc`, work_code, create_at, update_at) values "
               f"('{member_id}','{name}','{desc}','{work_code}','{current_time}','{current_time}')")
    print(sql)
    Execute().write_data_info(sql)
    return get_member_detail(member_id)


@member.route('/memberList', methods=['GET'])
def get_member_list():
    data = request.args
    page_number = int(data.get('page_number')) if data.get('page_number') else 0
    page_size = int(data.get('page_size')) if data.get('page_size') else 10
    if page_number:
        page_number = (page_number - 1) * page_size
    member_name = data.get('name') if data.get('name') else None
    if member_name:
        sql = (f"select race_member.id, race_member.name, race_member.`desc`, race_member.work_code, "
               f"race_member.create_at, race_member.update_at, rt.name from race_member "
               f"left join race.race_team rt on race_member.team_id = rt.id "
               f"where name like '%{member_name}%' order by create_at limit {page_size} offset {page_number}")
    else:
        sql = (f"select race_member.id, race_member.name, race_member.`desc`, race_member.work_code, "
               f"race_member.create_at, race_member.update_at, rt.name from race_member "
               f"left join race.race_team rt on race_member.team_id = rt.id "
               f" order by create_at limit {page_size} offset {page_number}")
    res = Execute().get_data_list(sql)
    data = []
    for info in res:
        data.append(
            {
                "id": info[0],
                "name": info[1],
                "desc": info[2],
                "work_code": info[3],
                "create_at": info[4],
                "update_at": info[5],
                "team_name": info[6] if len(info) > 6 else ""
            }
        )
    return {
        "result": "success",
        "data": data
    }


@member.route('/memberDetail/<member_id>', methods=['GET'])
def get_member_detail(member_id):
    sql = (f"select race_member.id, race_member.name, race_member.`desc`, race_member.work_code, "
           f"race_member.create_at, race_member.update_at, rt.name from race_member "
           f"left join race.race_team rt on race_member.team_id = rt.id "
           f"where race_member.id = '{member_id}'")
    res = Execute().get_data_one(sql)
    if len(res) > 0:
        return {
            "result": "success",
            "data": {
                "id": res[0],
                "name": res[1],
                "desc": res[2],
                "work_code": res[3],
                "create_at": res[4],
                "update_at": res[5],
                "team_name": res[6] if len(res) > 6 else ""
            }
        }
    else:
        return {
            "result": "failed",
            "msg": "该选手不存在"
        }, 400


@member.route('/memberUpdate', methods=['POST'])
def update_member():
    data = request.get_json()
    member_id = data["id"]
    name = data["name"]
    desc = data["desc"]
    work_code = data["work_code"]
    sql = f"select * from race_member where id = '{member_id}'"
    if len(Execute().get_data_list(sql)) < 1:
        return {"result": "failed", "msg": "该选手不存在"}, 400
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sql = (f"update race_member set name='{name}', `desc`='{desc}', work_code='{work_code}', update_at='{current_time}' "
           f"where id='{member_id}'")
    Execute().write_data_info(sql)
    return get_member_detail(member_id)


@member.route('/memberDelete/<member_id>', methods=['DELETE'])
def delete_member(member_id):
    sql = f"select * from race_member where id = '{member_id}'"
    if len(Execute().get_data_list(sql)) < 1:
        return {"result": "failed", "msg": "该选手不存在"}, 400
    sql = f"delete from race_member where id='{member_id}'"
    Execute().write_data_info(sql)
    return {}, 204
