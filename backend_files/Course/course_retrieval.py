from __main__ import app, db

from flask import jsonify


class Course(db.Model):
    course_id = db.Column(db.String(20), primary_key=True)
    course_name = db.Column(db.String(50), nullable=False)
    course_desc = db.Column(db.String(255))
    course_status = db.Column(db.String(15))
    course_type = db.Column(db.String(10))
    course_category = db.Column(db.String(50))
    registrations = db.relationship('Registration', backref='course', lazy=True)
    courseskills = db.relationship('CourseSkill', backref='course', lazy=True)
    ljcourses = db.relationship('LearningJourneyCourse', backref='course', lazy=True)

    def __init__(self,course_id,course_name,course_desc,course_status,course_type,course_category,registrations = list(),courseskills = list(), ljcourses = list()):
        self.course_id = course_id
        self.course_name = course_name
        self.course_desc = course_desc
        self.course_status = course_status
        self.course_type = course_type
        self.course_category = course_category
        self.registrations = registrations
        self.courseskills = courseskills
        self.ljcourses = ljcourses

    def json(self):
        return {
            "course_id": self.course_id,
            "course_name": self.course_name,
            "course_desc": self.course_desc,
            "course_status": self.course_status,
            "course_type": self.course_type,
            "course_category": self.course_category,
            "registrations": [registration.json() for registration in self.registrations],
            "courseskills": [courseskill.json() for courseskill in self.courseskills],
            "ljcourses": [ljcourse.json() for ljcourse in self.ljcourses]
        }

@app.route('/course')
def course():
    courses = Course.query.all()

    if len(courses):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "courses": [course.json() for course in courses]
                }
            }
        )

    return jsonify(
        {
            "code": 404,
            "message": "There are no courses."
        }
    ), 404

@app.route('/course/<string:course_id>')
def find_course(course_id):
    course = Course.query.filter_by(course_id=course_id).first()
    if course:
        return jsonify(
            {
                "code": 200,
                "data": course.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Course not found."
        }
    ), 404
