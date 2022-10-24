from __main__ import app, db

from flask import jsonify


class Staff(db.Model):
    staff_id = db.Column(db.Integer, primary_key=True)
    staff_fname = db.Column(db.String(50), nullable=False)
    staff_lname = db.Column(db.String(50), nullable=False)
    dept = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    role = db.Column(db.Integer, db.ForeignKey('role.role_id'))
    registrations = db.relationship('Registration', backref='Staff', lazy=True)
    
    def __init__(self,staff_id,staff_fname,staff_lname,dept,email,role,registrations = list()):
        self.staff_id = staff_id
        self.staff_fname = staff_fname
        self.staff_lname = staff_lname
        self.dept = dept
        self.email = email
        self.role = role
        self.registrations = registrations

    def json(self):
        return {
            "staff_id": self.staff_id,
            "staff_fname": self.staff_fname,
            "staff_lname": self.staff_lname,
            "dept": self.dept,
            "email": self.email,
            "role": self.role
        }

@app.route('/staff')
def staff():
    staffs = Staff.query.all()

    if len(staffs):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "staffs": [staff.json() for staff in staffs]
                }
            }
        )

    return jsonify(
        {
            "code": 404,
            "message": "There are no staffs."
        }
    ), 404

@app.route('/staff/<int:staff_id>')
def find_staff(staff_id):
    staff = Staff.query.filter_by(staff_id=staff_id).first()
    if staff:
        return jsonify(
            {
                "code": 200,
                "data": staff.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Staff not found."
        }
    ), 404