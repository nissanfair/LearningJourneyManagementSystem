from __main__ import app, LearningJourneyCourse
from flask import jsonify


# get learning journey courses table
@app.route('/learningjourneycourse')
def learningjourneycourse():
    learningjourneycourse = LearningJourneyCourse.query.all()

    if len(learningjourneycourse):
        return jsonify({"code": 200, "data": {"learningjourneycourse": [
            learningjourneycourse.json() for learningjourneycourse in learningjourneycourse]}})

    return jsonify(
        {
            "code": 404,
            "message": "There are no learningjourneycourses."
        }
    ), 404
