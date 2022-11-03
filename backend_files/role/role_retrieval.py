from __main__ import app, db
from api_app import Role


from flask import jsonify, request
from sqlalchemy import func


# add role
@app.route('/role', methods=['POST'])
def add_role():
    data = request.get_json()
    role = Role(**data)
    role_name = data['role_name'].lower()
    if (Role.query.filter(func.lower(Role.role_name) == role_name).first()):
        return jsonify(
            {
                "code": 400,
                "message": "role already exists."
            }
        ), 400
    try:
        db.session.add(role)
        db.session.commit()
    except BaseException:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "role_id": data['role_id']
                },
                "message": "An error occurred while creating the role."
            }
        ), 500

    return jsonify(
        {
            "code": 201,
            "data": role.json()
        }
    ), 201


@app.route('/role')
def role():
    roles = Role.query.all()

    if len(roles):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "roles": [role.json() for role in roles]
                }
            }
        )

    return jsonify(
        {
            "code": 404,
            "message": "There are no roles."
        }
    ), 404


@app.route('/role/<int:role_id>')
def find_role(role_id):
    role = Role.query.filter_by(role_id=role_id).first()
    if role:
        return jsonify(
            {
                "code": 200,
                "data": role.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Role not found."
        }
    ), 404
