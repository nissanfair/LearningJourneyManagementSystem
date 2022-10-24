from __main__ import app, db


from flask import jsonify


class Registration(db.Model):
    reg_id = db.Column(db.Integer, primary_key=True)
    # course_id = db.Column(db.String(20))
    # staff_id = db.Column(db.Integer)
    reg_status = db.Column(db.String(20), nullable=False)
    completion_status = db.Column(db.String(20), nullable=False)
    course_id = db.Column(db.String(20), db.ForeignKey('course.course_id'))
    staff_id = db.Column(db.Integer, db.ForeignKey('staff.staff_id'))

    def __init__(self,reg_id,reg_status,completion_status,course_id,staff_id):
        self.reg_id = reg_id
        self.reg_status = reg_status
        self.completion_status = completion_status
        self.course_id = course_id
        self.staff_id = staff_id

    def json(self):
        return {
            "reg_id": self.reg_id,
            "reg_status": self.reg_status,
            "completion_status": self.completion_status,
            "course_id": self.course_id,
            "staff_id": self.staff_id
        }

#get registrations
@app.route('/registration')
def registration():
    registrations = Registration.query.all()

    if len(registrations):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "registrations": [registration.json() for registration in registrations]
                }
            }
        )

    return jsonify(
        {
            "code": 404,
            "message": "There are no registrations."
        }
    ), 404