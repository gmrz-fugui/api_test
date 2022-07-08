from api_auto_test.uaf_api_test.TestCase import *

num ={"a":[]}

class TestAuth:
    
    @staticmethod
    def redy():
        global num
        num.update({"b": 1})
        print(num)
        return num

class TestCode(unittest.TestCase):

    @classmethod
    def setUp(cls):
        pass



    def test_code(self):
        TestAuth.redy()

if __name__ == '__main__':
    unittest.main()