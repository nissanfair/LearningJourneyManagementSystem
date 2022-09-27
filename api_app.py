from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS



app = Flask(__name__)

DBpassword = '' #for wamp it is default empty string
DBport = '3306'
DBusername = 'root'
DBhost = 'localhost'
DBname = 'ljms'

app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+mysqlconnector://{DBusername}:{DBpassword}@{DBhost}:{DBport}/{DBname}'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

CORS(app)



class JobRole(db.Model):
    __tablename__ = 'jobrole'
    jobrole_id = db.Column(db.Integer, primary_key=True)
    jobrole_name = db.Column(db.String(255), nullable=False)
    roleskills = db.relationship('RoleSkill', backref='jobrole', lazy=True)

    def __init__(self, jobrole_id, jobrole_name, roleskills = []):
        self.jobrole_id = jobrole_id
        self.jobrole_name = jobrole_name
        self.roleskills = roleskills

    def json(self):
        return {
                "jobrole_id": self.jobrole_id,
                "jobrole_name": self.jobrole_name,
                "roleskills": [roleskill.json() for roleskill in self.roleskills]
            }

class Skill(db.Model):
    __tablename__ = 'skill'
    skill_id = db.Column(db.Integer, primary_key=True)
    skill_name = db.Column(db.String(255), nullable=False)
    roleskills = db.relationship('RoleSkill', backref='skill', lazy=True)

    def __init__(self, skill_id, skill_name, roleskills = []):
        self.skill_id = skill_id
        self.skill_name = skill_name
        self.roleskills = roleskills

    def json(self):
        return {
                "skill_id": self.skill_id,
                "skill_name": self.skill_name
            }

class RoleSkill(db.Model):
    __tablename__ = 'roleskill'
    rsid = db.Column(db.Integer, primary_key=True)
    skill_id = db.Column(db.Integer, db.ForeignKey('skill.skill_id'), nullable=False)
    jobrole_id = db.Column(db.Integer, db.ForeignKey('jobrole.jobrole_id'), nullable=False)

    def __init__(self, rsid, skill_id, jobrole_id):
        self.rsid = rsid
        self.skill_id = skill_id
        self.jobrole_id = jobrole_id

    def json(self):
        return {
                "rsid": self.rsid,
                "skill_id": self.skill_id,
                "jobrole_id": self.jobrole_id
            }

class Role(db.Model):
    __tablename__ = 'role'

    role_id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(20), nullable=False)
    staffs = db.relationship('Staff', backref='Role', lazy=True)

    def __init__(self,role_id,role_name,staffs = list()):
        self.role_id = role_id
        self.role_name = role_name
        self.staffs = staffs

    def json(self):
        return {
            "role_id": self.role_id,
            "role_name": self.role_name
        }



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

class Course(db.Model):
    course_id = db.Column(db.String(20), primary_key=True)
    course_name = db.Column(db.String(50), nullable=False)
    course_desc = db.Column(db.String(255))
    course_status = db.Column(db.String(15))
    course_type = db.Column(db.String(10))
    course_category = db.Column(db.String(50))
    registrations = db.relationship('Registration', backref='Course', lazy=True)

    def __init__(self,course_id,course_name,course_desc,course_status,course_type,course_category,registrations = list()):
        self.course_id = course_id
        self.course_name = course_name
        self.course_desc = course_desc
        self.course_status = course_status
        self.course_type = course_type
        self.course_category = course_category
        self.registrations = registrations

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

# db.create_all()

def add_values(): #THIS IS EXAMPLE TO ADD VALUES TO DB (CURRENTLY NOT USED AS WE PRIORITISE READ OVER OTHER OPERATIONS)
    role1 = Role(role_id = 1, role_name = 'Admin', staffs=[])


    staff1 = Staff(staff_id = 1,
            staff_fname = 'Apple',
            staff_lname = 'Tan',
            dept = 'HR',
            email = 'apple.tan.hr@spm.com',
            role = 1,
            registrations = [])

    course1 = Course(course_id = 'IS111',
            course_name = 'Introduction to Programming',
            course_desc = 'Introductory Python module',
            course_status = 'Active',
            course_type = 'Internal',
            course_category = 'Technical',
            registrations = [])

    registration1 = Registration(reg_id = 1,
            course_id = 'IS111',
            staff_id = 1,
            reg_status = 'Registered',
            completion_status = 'Completed')

    db.session.add(role1)
    db.session.add(staff1)
    db.session.add(course1)
    db.session.add(registration1)
    db.session.commit()

@app.route('/')
def home():
    return """
    <h1>Hello! this links are to test the backend, expect json files from them.</h1>
    <a href='/getstaff'>get staffs</a>
    <a href='/getrole'>get roles</a>
    <a href='/jobrole'>get jobroles</a>
    <a href='/getskill'>get skills</a>
    <a href='/getroleskill'>get roleskills</a>
    """

@app.route('/getskill')
def getskill():
    skills = Skill.query.all()
    if len(skills):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "skills": [skill.json() for skill in skills]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no skills."
        }
    ), 404

@app.route('/getroleskill')
def getroleskill():
    roleskills = RoleSkill.query.all()
    if len(roleskills):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "roleskills": [roleskill.json() for roleskill in roleskills]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no roleskills."
        }
    ), 404

@app.route('/getstaff')
def getstaff():
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

@app.route('/role')
def getrole():
    roles = Role.query.all()

    if len(roles):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "roles": [role.json() for role in roles]
                }
            }
        )

    return jsonify(
        {
            "code": 404,
            "message": "There are no roles."
        }
    ), 404

@app.route('/jobrole')
def getjobrole():
    jobroles = JobRole.query.all()

    if len(jobroles):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "jobroles": [jobrole.json() for jobrole in jobroles]
                }
            }
        )

    return jsonify(
        {
            "code": 404,
            "message": "There are no jobroles."
        }
    ), 404

@app.route('/jobrole/<int:jobrole_id>')
def getjobrolebyid(jobrole_id):
    jobrole = JobRole.query.filter_by(jobrole_id=jobrole_id).first()

    if jobrole:
        return jsonify(
            {
                "code": 200,
                "data": jobrole.json()
            }
        )

    return jsonify(
        {
            "code": 404,
            "message": "JobRole not found."
        }
    ), 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)