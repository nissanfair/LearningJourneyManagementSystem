from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS


DBpassword = ''  # for wamp it is default empty string
DBport = '3306'
DBusername = 'root'
DBhost = 'localhost'
DBname = 'ljms'

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+mysqlconnector://{DBusername}:{DBpassword}@{DBhost}:{DBport}/{DBname}'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

CORS(app)


class Course(db.Model):
    course_id = db.Column(db.String(20), primary_key=True)
    course_name = db.Column(db.String(50), nullable=False)
    course_desc = db.Column(db.String(255))
    course_status = db.Column(db.String(15))
    course_type = db.Column(db.String(10))
    course_category = db.Column(db.String(50))
    registrations = db.relationship(
        'Registration', backref='course', lazy=True)
    courseskills = db.relationship('CourseSkill', backref='course', lazy=True)
    ljcourses = db.relationship(
        'LearningJourneyCourse', backref='course', lazy=True)

    def __init__(self, course_id, course_name, course_desc, course_status, course_type, course_category, registrations=list(), courseskills=list(), ljcourses=list()):
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


class JobRole(db.Model):
    __tablename__ = 'jobrole'
    jobrole_id = db.Column(db.Integer, primary_key=True)
    jobrole_name = db.Column(db.String(255), nullable=False)
    jobrole_desc = db.Column(db.String(255), nullable=False)
    roleskills = db.relationship('RoleSkill', backref='jobrole', lazy=True)
    isDeleted = db.Column(db.Boolean, nullable=False, default=False)
    learningjourneys = db.relationship(
        'LearningJourney', backref='jobrole', lazy=True)

    def __init__(self, jobrole_id, jobrole_name, jobrole_desc, roleskills=[], isDeleted=False, learningjourneys=[]):
        self.jobrole_id = jobrole_id
        self.jobrole_name = jobrole_name
        self.jobrole_desc = jobrole_desc
        self.roleskills = roleskills
        self.isDeleted = isDeleted
        self.learningjourneys = learningjourneys

    def json(self):
        return {
            "jobrole_id": self.jobrole_id,
            "jobrole_name": self.jobrole_name,
            "jobrole_desc": self.jobrole_desc,
            "roleskills": [roleskill.json() for roleskill in self.roleskills],
            "isDeleted": self.isDeleted,
            "learningjourneys": [learningjourney.json() for learningjourney in self.learningjourneys]
        }


class LearningJourney(db.Model):
    __tablename__ = 'learningjourney'
    lj_id = db.Column(db.Integer, primary_key=True)
    lj_name = db.Column(db.String(50), nullable=False)
    jobrole_id = db.Column(db.Integer, db.ForeignKey(
        'jobrole.jobrole_id'), nullable=False)
    staff_id = db.Column(db.Integer, db.ForeignKey(
        'staff.staff_id'), nullable=False)
    ljcourses = db.relationship(
        'LearningJourneyCourse', backref='learningjourney', lazy=True)

    def __init__(self, lj_id, lj_name, jobrole_id, staff_id, ljcourses=list()):
        self.lj_id = lj_id
        self.lj_name = lj_name
        self.jobrole_id = jobrole_id
        self.staff_id = staff_id
        self.ljcourses = ljcourses

    def json(self):
        return {
            "lj_id": self.lj_id,
            "lj_name": self.lj_name,
            "jobrole_id": self.jobrole_id,
            "staff_id": self.staff_id,
            "ljcourses": [ljcourse.json() for ljcourse in self.ljcourses],
        }


class LearningJourneyCourse(db.Model):
    __tablename__ = 'learningjourneycourse'
    ljc_id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.String(20), db.ForeignKey(
        'course.course_id'), nullable=False)
    lj_id = db.Column(db.Integer, db.ForeignKey(
        'learningjourney.lj_id'), nullable=False)

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


class Registration(db.Model):
    reg_id = db.Column(db.Integer, primary_key=True)
    # course_id = db.Column(db.String(20))
    # staff_id = db.Column(db.Integer)
    reg_status = db.Column(db.String(20), nullable=False)
    completion_status = db.Column(db.String(20), nullable=False)
    course_id = db.Column(db.String(20), db.ForeignKey('course.course_id'))
    staff_id = db.Column(db.Integer, db.ForeignKey('staff.staff_id'))

    def __init__(self, reg_id, reg_status, completion_status, course_id, staff_id):
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


class Role(db.Model):
    __tablename__ = 'role'

    role_id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(20), nullable=False)
    staffs = db.relationship('Staff', backref='Role', lazy=True)

    def __init__(self, role_id, role_name, staffs=list()):
        self.role_id = role_id
        self.role_name = role_name
        self.staffs = staffs

    def json(self):
        return {
            "role_id": self.role_id,
            "role_name": self.role_name
        }


class CourseSkill(db.Model):
    __tablename__ = 'courseskill'
    csid = db.Column(db.Integer, primary_key=True)
    skill_id = db.Column(db.Integer, db.ForeignKey(
        'skill.skill_id'), nullable=False)
    course_id = db.Column(db.String(20), db.ForeignKey(
        'course.course_id'), nullable=False)

    def __init__(self, csid, skill_id, course_id):
        self.csid = csid
        self.skill_id = skill_id
        self.course_id = course_id

    def json(self):
        return {
            "csid": self.csid,
            "skill_id": self.skill_id,
            "course_id": self.course_id
        }


class RoleSkill(db.Model):
    __tablename__ = 'roleskill'
    rsid = db.Column(db.Integer, primary_key=True)
    skill_id = db.Column(db.Integer, db.ForeignKey(
        'skill.skill_id'), nullable=False)
    jobrole_id = db.Column(db.Integer, db.ForeignKey(
        'jobrole.jobrole_id'), nullable=False)

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


class Skill(db.Model):
    __tablename__ = 'skill'
    skill_id = db.Column(db.Integer, primary_key=True)
    skill_name = db.Column(db.String(255), nullable=False)
    skill_desc = db.Column(db.String(255))
    roleskills = db.relationship('RoleSkill', backref='skill', lazy=True)
    courseskills = db.relationship('CourseSkill', backref='skill', lazy=True)
    isDeleted = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, skill_id, skill_name, skill_desc, roleskills=[], courseskills=[], isDeleted=False):
        self.skill_id = skill_id
        self.skill_name = skill_name
        self.skill_desc = skill_desc
        self.roleskills = roleskills
        self.courseskills = courseskills
        self.isDeleted = isDeleted

    def json(self):
        return {
            "skill_id": self.skill_id,
            "skill_name": self.skill_name,
            "skill_desc": self.skill_desc,
            "roleskills": [roleskill.json() for roleskill in self.roleskills],
            "courseskills": [courseskill.json() for courseskill in self.courseskills],
            "isDeleted": self.isDeleted
        }


class Staff(db.Model):
    staff_id = db.Column(db.Integer, primary_key=True)
    staff_fname = db.Column(db.String(50), nullable=False)
    staff_lname = db.Column(db.String(50), nullable=False)
    dept = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    role = db.Column(db.Integer, db.ForeignKey('role.role_id'))
    registrations = db.relationship('Registration', backref='Staff', lazy=True)

    def __init__(self, staff_id, staff_fname, staff_lname, dept, email, role, registrations=list()):
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


if __name__ == '__main__':
    from backend_files.Course import course_retrieval
    from backend_files.staff import staff_retrieval
    from backend_files.role import role_retrieval
    from backend_files.registration import registration_retrieval

    from backend_files.jobrole import jobrole_manager
    from backend_files.skill import skill_manager
    from backend_files.skill import course_skill_linker
    from backend_files.skill import jobrole_skills_linker
    from backend_files.learningjourney import learningjourney_manager
    from backend_files.learningjourney import learningjourney_course_linker


@app.route('/')
def home():
    return """
    <h1>Hello! this links are to test the backend, expect json files from them.</h1>
    <a href='/course'>get courses</a>
    <a href='/staff'>get staffs</a>
    <a href='/role'>get roles</a>
    <a href='/jobrole'>get jobroles</a>
    <a href='/skill'>get skills</a>
    <a href='/roleskill'>get roleskills</a>
    <a href='/courseskill'>get courseskills</a>
    <a href='/registration'>get registrations</a>
    <a href='/learningjourney'>get learningjourneys</a>
    <a href='/learningjourneycourse'>get learningjourneycourse</a>
    """


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
