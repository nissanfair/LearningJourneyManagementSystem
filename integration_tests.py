import unittest
import flask_testing
import json
from api_app import app, db, Course, JobRole
from api_app import LearningJourney, LearningJourneyCourse
from api_app import Role, CourseSkill, Skill, Staff


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

    course_retrieval
    staff_retrieval
    role_retrieval
    registration_retrieval
    jobrole_manager
    skill_manager
    course_skill_linker
    jobrole_skills_linker
    learningjourney_manager
    learningjourney_course_linker


class TestApp(flask_testing.TestCase):
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite://"
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {}
    app.config['TESTING'] = True
    maxDiff = None

    def create_app(self):
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

# Testing of Course folder


class TestRetrieveCourse(TestApp):
    def test_retrieve_course_empty_database(self):
        response = self.client.get("/course")

        self.assertEqual(response.json, {
            'code': 404,
            'message': 'There are no courses.'

        })
        print("passed course retrieval test with empty database")

    def test_retrieve_course(self):
        c1 = Course(course_id="IS111",
                    course_name='test name',
                    course_desc='test desc',
                    course_status="Active",
                    course_type="Internal",
                    course_category="Technical",
                    )
        db.session.add(c1)
        db.session.commit()

        response = self.client.get("/course")

        self.assertEqual(response.json, {
            'code': 200,
            'data': {
                'courses': [
                    {'course_category': 'Technical',
                         'course_desc': 'test desc',
                         'course_id': 'IS111',
                         'course_name': 'test name',
                         'course_status': 'Active',
                         'course_type': 'Internal',
                         'courseskills': [],
                         'ljcourses': [],
                         'registrations': []}
                ]
            }
        })
        print("passed course retrieval test with populated database")

# Testing of jobrole folder


class TestJobRole(TestApp):
    def test_retrieve_jobrole_empty_database(self):
        response = self.client.get("/jobrole")

        self.assertEqual(response.json, {
            'code': 404,
            'message': 'There are no jobroles.'
        })
        print("passed job role retrieval test with empty database")

    def test_retrieve_jobrole(self):
        j1 = JobRole(jobrole_id=1,
                     jobrole_name='test name',
                     jobrole_desc='test desc'
                     )
        db.session.add(j1)
        db.session.commit()

        response = self.client.get("/jobrole")

        self.assertEqual(response.json, {
            'code': 200,
            'data': {
                'jobroles': [
                    {
                        'isDeleted': False,
                        'jobrole_desc': 'test desc',
                        'jobrole_id': 1,
                        'jobrole_name': 'test name',
                        'learningjourneys': [],
                        'roleskills': []
                    }
                ]
            }
        })
        print("passed job role retrieval test with populated database")

    def test_create_jobrole(self):
        response = self.client.post("/jobrole", json={
            'jobrole_name': 'test name',
            'jobrole_desc': 'test desc'
        })

        self.assertEqual(response.json, {
            'code': 201,
            'data': {
                'isDeleted': False,
                'jobrole_desc': 'test desc',
                'jobrole_id': 1,
                'jobrole_name': 'test name',
                'learningjourneys': [],
                'roleskills': []
            }
        })
        print("passed job role creation test")

    def test_soft_delete_jobrole(self):
        j1 = JobRole(jobrole_id=1,
                     jobrole_name='test name',
                     jobrole_desc='test desc'
                     )
        db.session.add(j1)
        db.session.commit()

        response = self.client.get("/jobrole/1/softdelete")

        self.assertEqual(response.json, {
            'code': 200,
            'data': {
                'isDeleted': True,
                'jobrole_desc': 'test desc',
                'jobrole_id': 1,
                'jobrole_name': 'test name',
                'learningjourneys': [],
                'roleskills': []
            }
        })
        print("passed job role soft delete test")

    def test_update_jobrole(self):
        j1 = JobRole(jobrole_id=1,
                     jobrole_name='test name',
                     jobrole_desc='test desc'
                     )
        db.session.add(j1)
        db.session.commit()

        response = self.client.put("/jobrole/1", json={
            'jobrole_name': 'test name updated',
            'jobrole_desc': 'test desc updated'
        })

        self.assertEqual(response.json, {
            'code': 200,
            'data': {
                'isDeleted': False,
                'jobrole_desc': 'test desc updated',
                'jobrole_id': 1,
                'jobrole_name': 'test name updated',
                'learningjourneys': [],
                'roleskills': []
            }
        })
        print("passed job role update test")

# Testing of learningjourney folder


class TestLearningJourney(TestApp):
    def test_retrieve_learningjourney_empty_database(self):
        response = self.client.get("/learningjourney")

        self.assertEqual(response.json, {
            'code': 404,
            'message': 'There are no learningjourneys.'
        })
        print("passed learning journey retrieval test with empty database")

    def test_retrieve_learningjourney(self):
        jr1 = JobRole(
            jobrole_id=1,
            jobrole_name='test name',
            jobrole_desc='test desc'
        )

        role1 = Role(
            role_id=1,
            role_name='test name'
        )

        staff1 = Staff(
            staff_id=1,
            staff_fname='Apple',
            staff_lname='Tan',
            dept='HR',
            email='apple.tan.hr@spm.com',
            role=1
        )

        c1 = Course(
            course_id="IS111",
            course_name='test name',
            course_desc='test desc',
            course_status="Active",
            course_type="Internal",
            course_category="Technical",
        )

        lj1 = LearningJourney(
            lj_id=1,
            lj_name='test name',
            jobrole_id=1,
            staff_id=1
        )

        ljc1 = LearningJourneyCourse(
            ljc_id=1,
            course_id='IS111',
            lj_id=1
        )

        db.session.add(jr1)
        db.session.add(role1)
        db.session.add(staff1)
        db.session.add(c1)
        db.session.add(lj1)
        db.session.add(ljc1)
        db.session.commit()

        response = self.client.get("/learningjourney")

        self.assertEqual(response.json, {
            'code': 200,
            'data': {
                'learningjourneys': [
                    {
                        'jobrole_id': 1,
                        'lj_id': 1,
                        'lj_name': 'test name',
                        'ljcourses': [
                            {
                                'course_id': 'IS111',
                                'lj_id': 1,
                                'ljc_id': 1
                            }
                        ],
                        'staff_id': 1
                    }
                ]
            }
        })

        print("passed learning journey retrieval test with populated database")

        response = self.client.delete("/learningjourney/1")

        self.assertEqual(response.json, {
            'code': 200,
            'data': {
                'jobrole_id': 1,
                'lj_id': 1,
                'lj_name': 'test name',
                'ljcourses': [
                    {
                        'course_id': 'IS111',
                        'lj_id': 1,
                        'ljc_id': 1
                    }
                ],
                'staff_id': 1
            }
        })

        print("passed deletion of learning journey test")

# Testing of role folder


class TestRole(TestApp):
    def test_retrieve_role(self):
        response = self.client.get("/role")

        self.assertEqual(response.json, {
            'code': 404,
            'message': 'There are no roles.'
        })
        print("passed role retrieval test with empty database")

    def test_retrieve_role_populated_database(self):
        r1 = Role(
            role_id=1,
            role_name='test name'
        )

        db.session.add(r1)
        db.session.commit()

        response = self.client.get("/role")

        self.assertEqual(response.json, {
            'code': 200,
            'data': {
                'roles': [
                    {
                        'role_id': 1,
                        'role_name': 'test name'
                    }
                ]
            }
        })
        print("passed role retrieval test with populated database")


# Testing of skill folder

class TestCreateSkill(TestApp):
    def test_create_skill(self):

        request_body = {
            'skill_name': 'test name',
            'skill_desc': 'test desc'
        }

        response = self.client.post("/skill",
                                    data=json.dumps(request_body),
                                    content_type='application/json')

        self.assertEqual(response.json["data"], {
            'skill_id': 1,
            'skill_name': 'test name',
            'skill_desc': 'test desc',
            'courseskills': [],
            'roleskills': [],
            'isDeleted': False
        })
        print("Passed creation of skill!")

    def test_create_skill_invalid_name(self):
        s1 = Skill(skill_id=1, skill_name='test name', skill_desc='test desc')
        db.session.add(s1)
        db.session.commit()

        request_body = {
            'skill_name': 'test name',
            'skill_desc': 'test desc 2'
        }

        response = self.client.post("/skill",
                                    data=json.dumps(request_body),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {
            'code': 400,
            'message': 'skill already exists.'
        })
        print("Passed creation of skill with duplicate!")


class TestAssignSkillToCourse(TestApp):

    def test_assign_skill_to_course(self):
        s1 = Skill(skill_id=1, skill_name='test name', skill_desc='test desc')
        c1 = Course(course_id="IS111",
                    course_name='test name',
                    course_desc='test desc',
                    course_status="Active",
                    course_type="Internal",
                    course_category="Technical",
                    )
        db.session.add(s1)
        db.session.add(c1)
        db.session.commit()

        request_body = {
            'course_id': 'IS111',
            'skill_id': 1
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
        s1 = Skill(skill_id=1, skill_name='test name', skill_desc='test desc')
        c1 = Course(course_id="IS111",
                    course_name='test name',
                    course_desc='test desc',
                    course_status="Active",
                    course_type="Internal",
                    course_category="Technical",
                    )
        cs1 = CourseSkill(csid=1, course_id="IS111", skill_id=1)
        db.session.add(s1)
        db.session.add(c1)
        db.session.add(cs1)
        db.session.commit()

        request_body = {
            'course_id': 'IS111',
            'skill_id': 1
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


class TestAssignSkillToJobRole(TestApp):

    def test_assign_skill_to_jobrole(self):
        s1 = Skill(skill_id=1, skill_name='test name', skill_desc='test desc')
        jr1 = JobRole(jobrole_id=3, jobrole_name='test name',
                      jobrole_desc='test desc')

        db.session.add(s1)
        db.session.add(jr1)
        db.session.commit()

        request_body = {
            'roleskills': [
                {
                    'skill_id': 1
                }
            ]
        }

        jobrole_id = 3

        response = self.client.put(f"/jobrole/{jobrole_id}/roleskills",
                                   data=json.dumps(request_body),
                                   content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {
            "code": 200,
            "data": [{
                "jobrole_id": 3,
                "rsid": 1,
                "skill_id": 1
            }]
        })
        print("Passed assign skill to jobrole!")


# Testing of staff folder
class TestStaff(TestApp):
    def test_retrieve_staff_empty_database(self):
        response = self.client.get("/staff")

        self.assertEqual(response.json, {
            'code': 404,
            'message': 'There are no staffs.'
        })
        print("passed staff retrieval test with empty database")

    def test_retrieve_staff_populated_database(self):
        staff1 = Staff(
            staff_id=1,
            staff_fname='Apple',
            staff_lname='Tan',
            dept='HR',
            email='apple.tan.hr@spm.com',
            role=1
        )

        db.session.add(staff1)
        db.session.commit()

        response = self.client.get("/staff")

        self.assertEqual(response.json, {
            'code': 200,
            'data': {
                'staffs': [
                    {
                        'dept': 'HR',
                        'email': 'apple.tan.hr@spm.com',
                        'role': 1,
                        'staff_fname': 'Apple',
                        'staff_id': 1,
                        'staff_lname': 'Tan'
                    }
                ]
            }
        })


if __name__ == '__main__':
    print("-- Integration Testing --")
    unittest.main()
