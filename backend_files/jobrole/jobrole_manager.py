from __main__ import app, db
from api_app import JobRole, Skill

from flask import jsonify, request
from sqlalchemy import func


@app.route('/jobrole/<int:jobrole_id>', methods=['PUT'])
def update_jobrole(jobrole_id):
    jobrole = JobRole.query.filter_by(jobrole_id=jobrole_id).first()
    if jobrole:
        data = request.get_json()
        jobrole_name = data['jobrole_name'].lower()

        original_name = jobrole.jobrole_name

        jobrole.jobrole_name = "temp"
        db.session.commit()

        if (JobRole.query.filter(func.lower(
                JobRole.jobrole_name) == jobrole_name).first()):
            jobrole.jobrole_name = original_name
            db.session.commit()
            return jsonify(
                {
                    "code": 400,
                    "message": "job role already exists."
                }
            ), 400
        try:
            jobrole.jobrole_name = data['jobrole_name']
            jobrole.jobrole_desc = data['jobrole_desc']
            db.session.commit()
        except BaseException:
            return jsonify(
                {
                    "code": 500,
                    "data": {
                        "jobrole_id": jobrole_id
                    },
                    "message": "An error occurred while updating the jobrole."
                }
            ), 500

        return jsonify(
            {
                "code": 200,
                "data": jobrole.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "role not found."
        }
    ), 404


@app.route('/jobrole')
def getjobrole():
    # get all non soft deleted job roles
    jobroles = JobRole.query.filter_by(isDeleted=False).all()

    if len(jobroles):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "jobroles": [jobrole.json() for jobrole in jobroles]
                }
            }
        )

    return jsonify(
        {
            "code": 404,
            "message": "There are no jobroles."
        }
    ), 404


@app.route('/jobrole/<int:jobrole_id>')
def getjobrolebyid(jobrole_id):
    jobrole = JobRole.query.filter_by(jobrole_id=jobrole_id).first()

    if jobrole:
        jobrolejson = jobrole.json()

        linked_skills = []

        # iterate through roleskills in jobrole
        for roleskill in jobrole.roleskills:
            # get skill name from skill id
            skill = Skill.query.filter_by(skill_id=roleskill.skill_id).first()
            # append skill.json to linked_skills
            linked_skills.append(skill.json())

        jobrolejson['linked_skills'] = linked_skills

        return jsonify(
            {
                "code": 200,
                "data": jobrolejson
            }
        )

    return jsonify(
        {
            "code": 404,
            "message": "JobRole not found."
        }
    ), 404


@app.route('/jobrole/<int:jobrole_id>/softdelete')
def soft_delete_jobrole(jobrole_id):
    jobrole = JobRole.query.filter_by(jobrole_id=jobrole_id).first()
    if jobrole:
        if not jobrole.isDeleted:
            jobrole.isDeleted = True
        else:
            jobrole.isDeleted = False

        db.session.commit()
        return jsonify(
            {
                "code": 200,
                "data": jobrole.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "JobRole not found."
        }
    ), 404


@app.route('/jobrole/softdeleted')
def getsoftdeletedjobroles():
    jobroles = JobRole.query.filter_by(isDeleted=True).all()

    if len(jobroles):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "jobroles": [jobrole.json() for jobrole in jobroles]
                }
            }
        )

    return jsonify(
        {
            "code": 404,
            "message": "There are no soft deleted jobroles."
        }
    ), 404

# add job role


@app.route('/jobrole', methods=['POST'])
def add_jobrole():
    data = request.get_json()
    jobrole = JobRole(**data, jobrole_id=JobRole.query.count() + 1)
    # check if jobrole already exists
    if JobRole.query.filter_by(jobrole_name=jobrole.jobrole_name).first():
        return jsonify(
            {
                "code": 400,
                "message": "A jobrole with name '{}' already exists.".format(jobrole.jobrole_name)
            }
        ), 400
    try:
        db.session.add(jobrole)
        db.session.commit()
    except BaseException:
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred creating the jobrole."
            }
        ), 500

    return jsonify(
        {
            "code": 201,
            "data": jobrole.json()
        }
    ), 201
