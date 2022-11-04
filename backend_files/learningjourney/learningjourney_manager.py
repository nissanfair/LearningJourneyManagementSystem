from api_app import Skill, Course, JobRole
from api_app import LearningJourneyCourse, LearningJourney

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


# add learning journey
@app.route('/learningjourney', methods=['POST'])
def add_learningjourney():
    data = request.get_json()

    courses = data["courses"]
    staff_id = data["staff_id"]
    jobrole_id = data["jobrole_id"]
    lj_name = data["lj_name"]

    learningjourney = LearningJourney(lj_name=lj_name,staff_id=staff_id,jobrole_id=jobrole_id, lj_id = LearningJourney.query.filter(LearningJourney.lj_id != None).order_by(LearningJourney.lj_id).all()[-1].lj_id + 1)

    if (LearningJourney.query.filter(func.lower(LearningJourney.lj_name)== lj_name).first()):
            return jsonify(
                {
                    "code": 400,
                    "message": "A Learning Journey with the same name already exists."
                }
            ), 400


    try:
        db.session.add(learningjourney)
        db.session.commit()

        lj_id = learningjourney.lj_id
        for course_id in courses:
            print(course_id)
            ljc_id = LearningJourneyCourse.query.filter(LearningJourneyCourse.ljc_id != None).order_by(LearningJourneyCourse.ljc_id).all()[-1].ljc_id + 1
            lj_course = LearningJourneyCourse(lj_id=lj_id, course_id=course_id, ljc_id=ljc_id)
            db.session.add(lj_course)
            db.session.commit()

    except:
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred creating the learningjourney."
            }
        ), 500

    return jsonify(
        {
            "code": 201,
            "data": learningjourney.json()
        }
    ), 201

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
