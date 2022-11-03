from __main__ import app, db, JobRole, RoleSkill
from flask import jsonify, request


@app.route('/roleskill')
def roleskill():
    roleskills = RoleSkill.query.all()
    if len(roleskills):
        return jsonify({"code": 200, "data": {"roleskills": [
            roleskill.json() for roleskill in roleskills]}})
    return jsonify(
        {
            "code": 404,
            "message": "There are no roleskills."
        }
    ), 404


@app.route('/roleskill/<int:roleskill_id>')
def find_roleskill(roleskill_id):
    roleskill = RoleSkill.query.filter_by(roleskill_id=roleskill_id).first()
    if roleskill:
        return jsonify(
            {
                "code": 200,
                "data": roleskill.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Roleskill not found."
        }
    ), 404


@app.route('/jobrole/<int:jobrole_id>/roleskills', methods=['PUT'])
def update_roleskill_forrole(jobrole_id):
    try:
        data = request.get_json()
        print(data)
        jobrole = JobRole.query.filter_by(jobrole_id=jobrole_id).first()
        roleskill = RoleSkill.query.filter_by(jobrole_id=jobrole_id).all()

        # delete all roleskills for skill
        for rs in roleskill:
            db.session.delete(rs)

        unique_jobrole_id = []
        # add new roleskills for skill
        for roleskillobject in data['roleskills']:
            skill_id = roleskillobject['skill_id']
            if skill_id not in unique_jobrole_id:
                unique_jobrole_id.append(skill_id)
            else:
                continue

            rsid = 1
            try:
                rsid = RoleSkill.query.filter(RoleSkill.rsid is not None).order_by(
                    RoleSkill.rsid).all()[-1].rsid + 1
            except BaseException:
                pass

            roleskill = RoleSkill(
                skill_id=skill_id, jobrole_id=jobrole_id, rsid=rsid)
            db.session.add(roleskill)
        db.session.commit()

        # return updated roleskills
        return jsonify(
            {
                "code": 200,
                "data": [roleskill.json() for roleskill in jobrole.roleskills]
            }
        )
    except BaseException:
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred updating the roleskill."
            }
        ), 500
