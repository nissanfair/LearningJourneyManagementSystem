import unittest
import flask_testing
import json
from api_app import app, db, Course, JobRole, LearningJourney, LearningJourneyCourse, Registration, Role, CourseSkill, RoleSkill, Skill, Staff



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



class TestApp(flask_testing.TestCase):
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite://"
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {}
    app.config['TESTING'] = True

    def create_app(self):
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()


class TestCreateSkill(TestApp):
    def test_create_skill(self):

        request_body = {
            'skill_name' : 'test name',
            'skill_desc' : 'test desc'
        }

        response = self.client.post("/skill",
                                    data=json.dumps(request_body),
                                    content_type='application/json')

        self.assertEqual(response.json["data"], {
            'skill_id' : 1,
            'skill_name' : 'test name',
            'skill_desc' : 'test desc',
            'courseskills' : [],
            'roleskills' : [],
            'isDeleted' : False
        })
        print("Passed creation of skill!")

    def test_create_skill_invalid_name(self):
        s1 = Skill(skill_id = 1, skill_name='test name', skill_desc='test desc')
        db.session.add(s1)
        db.session.commit()

        request_body = {
            'skill_name' : 'test name',
            'skill_desc' : 'test desc 2'
        }

        response = self.client.post("/skill",
                                    data=json.dumps(request_body),
                                    content_type='application/json')


        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {
            'code' : 400,
            'message': 'skill already exists.'
        })
        print("Passed creation of skill with duplicate!")

class TestAssignSkillToCourse(TestApp):

    def test_assign_skill_to_course(self):
        s1 = Skill(skill_id = 1, skill_name='test name', skill_desc='test desc')
        c1 = Course(course_id="IS111",
                    course_name='test name',
                    course_desc='test desc',
                    course_status = "Active",
                    course_type = "Internal",
                    course_category="Technical",
                    )
        db.session.add(s1)
        db.session.add(c1)
        db.session.commit()

        request_body = {
            'course_id' : 'IS111',
            'skill_id' : 1
        }


        response = self.client.post("/courseskill",
                                    data=json.dumps(request_body),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json, {
            "code": 201,
            "data": {
                "course_id": "IS111",
                "csid": 1,
                "skill_id": 1
            }
        })
        print("Passed assign skill to course!")

    def test_assign_skill_to_course_already_exists(self):
        s1 = Skill(skill_id = 1, skill_name='test name', skill_desc='test desc')
        c1 = Course(course_id="IS111",
                    course_name='test name',
                    course_desc='test desc',
                    course_status = "Active",
                    course_type = "Internal",
                    course_category="Technical",
                    )
        cs1 = CourseSkill(csid=1, course_id="IS111", skill_id=1)
        db.session.add(s1)
        db.session.add(c1)
        db.session.add(cs1)
        db.session.commit()

        request_body = {
            'course_id' : 'IS111',
            'skill_id' : 1
        }


        response = self.client.post("/courseskill",
                                    data=json.dumps(request_body),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {
            "code": 400,
            "message": "A courseskill with skill_id '1' and course_id 'IS111' already exists."
        })
        print("Passed assign skill to course that already exists!")




if __name__ == '__main__':
    unittest.main()
