from __main__ import app, db, Skill, CourseSkill

from flask import jsonify, request



@app.route('/courseskill')
def courseskill():
    courseskills = CourseSkill.query.all()

    if len(courseskills):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "courseskills": [courseskill.json() for courseskill in courseskills]
                }
            }
        )

    return jsonify(
        {
            "code": 404,
            "message": "There are no courseskills."
        }
    ), 404

# put request to courseskill with only skill_id
@app.route('/skill/<int:skill_id>/courseskills', methods=['PUT'])
def update_courseskill_forskill(skill_id):

    try:
        data = request.get_json()
        print(data)
        skill = Skill.query.filter_by(skill_id=skill_id).first()
        courseskill = CourseSkill.query.filter_by(skill_id=skill_id).all()


        # delete all courseskills for skill
        for cs in courseskill:
            db.session.delete(cs)

        unique_course_id = []
        # add new courseskills for skill
        for courseskillobject in data['courseskills']:
            course_id = courseskillobject['course_id']
            if course_id not in unique_course_id:
                unique_course_id.append(course_id)
            else:
                continue

            csid = 1
            try:
                csid = CourseSkill.query.filter(CourseSkill.csid != None).order_by(CourseSkill.csid).all()[-1].csid + 1
            except:
                pass
            
            
            courseskill = CourseSkill(skill_id=skill_id, course_id=course_id, csid = csid)
            db.session.add(courseskill)
        
        db.session.commit()
        
        

        #return updated courseskills
        return jsonify(
            {
                "code": 200,
                "data": [courseskill.json() for courseskill in skill.courseskills]
            }
        )
    except:
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred updating the courseskill."
            }
        ), 500


    


# post request to courseskill
@app.route('/courseskill', methods=['POST'])
def add_courseskill():





    data = request.get_json()
    courseskill = CourseSkill(**data, csid = CourseSkill.query.filter(CourseSkill.csid != None).order_by(CourseSkill.csid).all()[-1].csid + 1)

    #check if courseskill with same skill and course already exists
    if CourseSkill.query.filter_by(skill_id=courseskill.skill_id, course_id=courseskill.course_id).first():
        return jsonify(
            {
                "code": 400,
                "message": "A courseskill with skill_id '{}' and course_id '{}' already exists.".format(courseskill.skill_id, courseskill.course_id)
            }
        ), 400

    try:
        db.session.add(courseskill)
        db.session.commit()
    except:
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred creating the courseskill." #should not happen because checks in place to prevent duplicate csid
            }
        ), 500

    return jsonify(
        {
            "code": 201,
            "data": courseskill.json()
        }
    ), 201

    

# delete request to courseskill
@app.route('/courseskill/<string:course_id>/<int:skill_id>', methods=['DELETE'])
def delete_courseskill(course_id, skill_id):
    courseskill = CourseSkill.query.filter_by(course_id=course_id, skill_id=skill_id).first()
    
    if courseskill:
        db.session.delete(courseskill)
        db.session.commit()
        return jsonify(
            {
                "code": 200,
                "data": courseskill.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "CourseSkill not found."
        }
    ), 404
