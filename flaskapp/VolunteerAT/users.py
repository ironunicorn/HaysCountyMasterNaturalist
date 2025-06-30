from flask import Blueprint

from VolunteerAT.auth import admin_required
from VolunteerAT.db import get_db


bp = Blueprint('users', __name__)

@bp.route('/api/users')
@admin_required
def list():
    users = []
    with get_db() as cursor:
        cursor.execute(
            """SELECT id, email, admin, project_coordinator FROM master_naturalist"""
        )

        db_users = cursor.fetchall()
        users = [{'id': user[0], 'email': user[1], 'admin': user[2], 'project_coordinator': user[3]} for user in db_users]

    return users