from __main__ import app, db
from flask import jsonify


class LearningJourneyCourse(db.Model):
    __tablename__ = 'learningjourneycourse'
    ljc_id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.String(20), db.ForeignKey('course.course_id'), nullable=False)
    lj_id = db.Column(db.Integer, db.ForeignKey('learningjourney.lj_id'), nullable=False)

    def __init__(self, ljc_id, course_id, lj_id):
        self.ljc_id = ljc_id
        self.course_id = course_id
        self.lj_id = lj_id
    
    def json(self):
        return {
                "ljc_id": self.ljc_id,
                "course_id": self.course_id,
                "lj_id": self.lj_id
            }

#get learning journey courses table
@app.route('/learningjourneycourse')
def learningjourneycourse():
    learningjourneycourse = LearningJourneyCourse.query.all()

    if len(learningjourneycourse):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "learningjourneycourse": [learningjourneycourse.json() for learningjourneycourse in learningjourneycourse]
                }
            }
        )

    return jsonify(
        {
            "code": 404,
            "message": "There are no learningjourneycourses."
        }
    ), 404