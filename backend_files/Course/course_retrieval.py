from __main__ import app, db, Course

from flask import jsonify


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
