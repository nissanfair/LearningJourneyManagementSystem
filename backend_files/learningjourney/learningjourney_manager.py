from __main__ import app, db, Skill, Course, JobRole, Staff, LearningJourneyCourse, LearningJourney
from flask import jsonify


# get learning journey
@app.route('/learningjourney')
def learningjourney():
    learningjourneys = LearningJourney.query.all()

    if len(learningjourneys):
        return jsonify({"code": 200, "data": {"learningjourneys": [
            learningjourney.json() for learningjourney in learningjourneys]}})

    return jsonify(
        {
            "code": 404,
            "message": "There are no learningjourneys."
        }
    ), 404


@app.route('/staff/learningjourney/<int:staff_id>')
def learningjourneyuser(staff_id):

    # learningjourneys = LearningJourney.query.all()

    # print(LearningJourney['staff_id'])

    listoflj = LearningJourney.query.filter_by(staff_id=staff_id)

    if listoflj:
        learningjourneysjson = []

        # iterate through learningjourneys
        for learningjourneyobject in listoflj:
            learningjourneysjson.append(learningjourneyobject.json())

            linked_jobrole = JobRole.query.filter_by(
                jobrole_id=learningjourneyobject.jobrole_id).first()
            linked_courses = []

            learningjourney = LearningJourney.query.filter_by(
                lj_id=learningjourneyobject.lj_id).first()
            # iterate through ljcourses

            ljcourses = LearningJourneyCourse.query.filter_by(
                lj_id=learningjourney.lj_id)
            for ljcourseobject in ljcourses:
                course = Course.query.filter_by(
                    course_id=ljcourseobject.course_id).first()
                linked_courses.append(course.json())

            linked_skills = []
            for roleskillobject in linked_jobrole.roleskills:
                skill = Skill.query.filter_by(
                    skill_id=roleskillobject.skill_id).first()
                linked_skills.append(skill.json())

            learningjourneysjson[-1]['linked_jobrole'] = linked_jobrole.json()
            learningjourneysjson[-1]['linked_jobrole']['linked_skills'] = linked_skills
            learningjourneysjson[-1]['linked_courses'] = linked_courses

        return jsonify(
            {
                "code": 200,
                "data": {
                    "learningjourneys": learningjourneysjson
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no learningjourneys."
        }
    ), 404
    # print(listoflj)

    # print("hi")

    # if len(learningjourneys):
    #     return jsonify(
    #         {
    #             "code": 200,
    #             "data": {
    #                 "learningjourneys": [learningjourney.json() for learningjourney in learningjourneys]
    #             }
    #         }
    #     )

    # return jsonify(
    #     {
    #         "code": 404,
    #         "message": "There are no learningjourneys."
    #     }
    # ), 404

# delete learning journey


@app.route('/learningjourney/<int:lj_id>', methods=['DELETE'])
def delete_learningjourney(lj_id):
    learningjourney = LearningJourney.query.filter_by(lj_id=lj_id).first()
    if learningjourney:
        try:
            # iterate through learningjourney.ljcourses
            for ljcourseobject in learningjourney.ljcourses:
                db.session.delete(ljcourseobject)

            db.session.delete(learningjourney)
            db.session.commit()
        except BaseException:
            return jsonify(
                {
                    "code": 500,
                    "message": "An error occurred deleting the learningjourney."
                }
            ), 500

        return jsonify(
            {
                "code": 200,
                "data": learningjourney.json()
            }
        )

    return jsonify(
        {
            "code": 404,
            "message": "Learning Journey not found."
        }
    ), 404
