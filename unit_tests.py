import unittest
from api_app import Skill


class TestSkill(unittest.TestCase):
    def test_to_dict(self):
        s1 = Skill(skill_id=1, skill_name='test name', skill_desc='test desc')
        self.assertEqual(s1.json(), {
            'skill_id' : 1,
            'skill_name' : 'test name',
            'skill_desc' : 'test desc',
            'courseskills' : [],
            'roleskills' : [],
            'isDeleted' : False
        })
        

if __name__ == "__main__":
    unittest.main()
