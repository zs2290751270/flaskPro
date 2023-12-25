import uuid
from datetime import datetime
from flask import Blueprint, request
from flaskPro.common.db import Execute

member = Blueprint('/member', __name__, url_prefix='/member')


@member.route('/memberCreate', methods=['POST'])
def create_member():
    pass


@member.route('/memberList', methods=['GET'])
def get_member_list():
    pass


@member.route('/memberDetail', methods=['GET'])
def create_member():
    pass


@member.route('/memberUpdate', methods=['POST'])
def create_member():
    pass
