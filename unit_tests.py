import unittest
from api_app import Skill, Course, JobRole, LearningJourney, Staff, Role


class TestSkill(unittest.TestCase):
    def test_skill(self):
        s1 = Skill(skill_id=1, skill_name='test name', skill_desc='test desc')
        self.assertEqual(s1.json(), {
            'skill_id' : 1,
            'skill_name' : 'test name',
            'skill_desc' : 'test desc',
            'courseskills' : [],
            'roleskills' : [],
            'isDeleted' : False
        })
        print("Passed testing of skill unit!")

class TestCourse(unittest.TestCase):
    def test_course(self):
        c1 = Course(course_id=1,
         course_name='test name',
        course_desc='test desc',
         course_status = "Active",
          course_type = "Internal",
          course_category="Technical",
           )
        self.assertEqual(c1.json(), {
            'course_id' : 1,
            'course_name' : 'test name',
            'course_desc' : 'test desc',
            'course_status' : 'Active',
            'course_type' : 'Internal',
            'course_category' : 'Technical',
            'courseskills' : [],
            'ljcourses' : [],
            'registrations' : []
        })
        print("Passed testing of course unit!")

class TestJobrole(unittest.TestCase):
    def test_jobrole(self):
        j1 = JobRole(jobrole_id=1,
         jobrole_name='test name',
         jobrole_desc='test desc'
        )
        self.assertEqual(j1.json(), {
            'jobrole_id' : 1,
            'jobrole_name' : 'test name',
            'jobrole_desc' : 'test desc',
            'isDeleted' : False,
            'learningjourneys' : [],
            'roleskills' : []
        })
        print("Passed testing of jobrole unit!")

class TestLearningJourney(unittest.TestCase):
    def test_learningjourney(self):
        r1 = Role(role_id=1,
         role_name='test name'
         )

        s1 = Staff(staff_id=1,
        staff_fname='Piplup',
        staff_lname='Pikachu',
        dept='Human Resource',
        email='piplup@pikachu.com',
        role=1)

        j1 = JobRole(jobrole_id=1,
         jobrole_name='test name',
         jobrole_desc='test desc'
        )


        lj1 = LearningJourney(lj_id=1,
            lj_name='test name',
            jobrole_id=1,
            staff_id=1
        )

        self.assertEqual(lj1.json(), {
            'lj_id' : 1,
            'lj_name' : 'test name',
            'jobrole_id' : 1,
            'staff_id' : 1,
            'ljcourses' : []
        })
        print("Passed testing of learningjourney unit!")




        

if __name__ == "__main__":
    unittest.main()
