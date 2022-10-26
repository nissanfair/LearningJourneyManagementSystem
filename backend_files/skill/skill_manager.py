from __main__ import app, db, Course, Skill


from flask import jsonify, request
from sqlalchemy import func



@app.route('/skill')
def skill():
    skills = Skill.query.all()
    if len(skills):

        skills_not_softdeleted = [skill.json() for skill in skills if not skill.isDeleted]

        if len(skills_not_softdeleted):
            return jsonify(
                {
                    "code": 200,
                    "data": {
                        "skills": skills_not_softdeleted
                    }
                }
            )
        
        return jsonify(
            {
                "code": 404,
                "message": "No skills found that are non softdeleted."
            }
        )

    return jsonify(
        {
            "code": 404,
            "message": "There are no skills."
        }
    ), 404

@app.route('/skill/softdeleted')
def skill_softdeleted():
    skills = Skill.query.all()
    if len(skills):
        softdeleted_skills = [skill.json() for skill in skills if skill.isDeleted]

        if len(softdeleted_skills):
            return jsonify(
                {
                    "code": 200,
                    "data": {
                        "skills": softdeleted_skills
                    }
                }
            )

        return jsonify(
            {
                "code": 404,
                "message": "No skills found that are softdeleted."
            }
        )
        
    return jsonify(
        {
            "code": 404,
            "message": "There are no skills in the database."
        }
    ), 404

@app.route('/skill/<int:skill_id>')
def find_skill(skill_id):
    skill = Skill.query.filter_by(skill_id=skill_id).first()
    linked_courses = []
    
    if skill:
        courseskillswithname = []
        # iterate through courseskills and get the course name
        for courseskill in skill.courseskills:
            course = Course.query.filter_by(course_id=courseskill.course_id).first()
            linked_courses.append(course.json())

            courseskillswithname.append({
                "csid": courseskill.csid,
                "skill_id": courseskill.skill_id,
                "course_id": courseskill.course_id,
                "course_name": course.course_name
            })

        skilljson = skill.json()
        skilljson["courseskills"] = courseskillswithname
        skilljson["linked_courses"] = linked_courses

        return jsonify(
            {
                "code": 200,
                "data": skilljson,
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Skill not found."
        }
    ), 404

#add skill
@app.route('/skill', methods=['POST'])
def add_skill():
    data = request.get_json()
    skill = Skill(**data, skill_id = Skill.query.count() + 1)
    skill_name = data['skill_name'].lower()
    if (Skill.query.filter(func.lower(Skill.skill_name)== skill_name).first()):
        return jsonify(
            {
                "code": 400,
                "message": "skill already exists."
            }
        ), 400
    try:
        db.session.add(skill)
        db.session.commit()
    except:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "skill_id": data['skill_id']
                },
                "message": "An error occurred while creating the skill."
            }
        ), 500

    return jsonify(
        {
            "code": 201,
            "data": skill.json()
        }
    ), 201

# update skill
@app.route('/skill/<int:skill_id>', methods=['PUT'])
def update_skill(skill_id):
    skill = Skill.query.filter_by(skill_id=skill_id).first()
    if skill:
        data = request.get_json()
        skill_name = data['skill_name'].lower()

        original_name = skill.skill_name

        skill.skill_name = "temp"
        db.session.commit()

        if (Skill.query.filter(func.lower(Skill.skill_name)== skill_name).first()):
            skill.skill_name = original_name
            db.session.commit()
            return jsonify(
                {
                    "code": 400,
                    "message": "skill already exists."
                }
            ), 400
        try:
            skill.skill_name = data['skill_name']
            skill.skill_desc = data['skill_desc']
            db.session.commit()
        except:
            return jsonify(
                {
                    "code": 500,
                    "data": {
                        "skill_id": skill_id
                    },
                    "message": "An error occurred while updating the skill."
                }
            ), 500

        return jsonify(
            {
                "code": 200,
                "data": skill.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Skill not found."
        }
    ), 404

#soft delete skill
@app.route('/skill/<int:skill_id>/softdelete')
def soft_delete_skill(skill_id):
    skill = Skill.query.filter_by(skill_id=skill_id).first()
    if skill:
        if not skill.isDeleted:
            skill.isDeleted = True
        else:
            skill.isDeleted = False
            
        db.session.commit()
        return jsonify(
            {
                "code": 200,
                "data": skill.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Skill not found."
        }
    ), 404
