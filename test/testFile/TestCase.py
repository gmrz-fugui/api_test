

from parameterized import parameterized,param
import unittest
import requests
import json
import sys

class MyTestLoader(unittest.TestLoader):
    def getTestCaseNames(self, testcase_class):
        # 调用父类的获取“测试方法”函数
        test_names = super().getTestCaseNames(testcase_class)
        # 拿到测试方法list
        testcase_methods = list(testcase_class.__dict__.keys())
        # 根据list的索引对testcase_methods进行排序
        test_names.sort(key=testcase_methods.index)
        # 返回测试方法名称
        return test_names

body = {
        'context':
            {
                'transNo': 'test-66666666666',
                'appID': 1103,
                'authType': [ '00', '20' ]
            }
    }
statusCode = 1200

testcases={} # 获取所有以test_开头的用例

class TestCase(unittest.TestCase):
    testcases[ 'TestCase' ] = [ i for i in sys._getframe().f_code.co_names if 'test_' in i ]
    @classmethod
    def setUpClass(cls) -> None:
        cls.url ='http://192.168.3.203:8080/uaf/device/support'

        cls.headers = {
        "Content-Type": "application/fido+uaf"
        }

    @parameterized.expand([(body,statusCode),(body,1200)])
    def test_a(self,params,result):
        r = requests.post(url=self.url,headers = self.headers,data = json.dumps(params))
        # print(r.json())
        self.assertEqual(r.json()['statusCode'],result)

    @parameterized.expand([ (body, statusCode), (body, 1200) ])
    def test_c(self, params, result):
        r = requests.post(url = self.url, headers = self.headers, data = json.dumps(params))
        # print(r.json())
        self.assertEqual(r.json()[ 'statusCode' ], result)

    @parameterized.expand([ (body, statusCode), (body, 1200) ])
    def test_b(self, params, result):
        r = requests.post(url = self.url, headers = self.headers, data = json.dumps(params))
        # print(r.json())
        self.assertEqual(r.json()[ 'statusCode' ], result)

def get_query_case():
    """
    组装测试用例
    :return:
    """
    list_case = [ ]
    for k, v in testcases.items():
        for j in v:
            list_case.append(eval(k)(j))
    return list_case

if __name__ == '__main__':
    # suit =unittest.TestSuite()
    # loader = MyTestLoader()
    # suit1 =loader.loadTestsFromTestCase(TestCase)
    # suit.addTest(suit1)
    # runner = unittest.TextTestRunner(verbosity = 2)
    # runner.run(suit)
    ###################################################
    suit = unittest.TestSuite()
    for i in get_query_case():
        suit.addTest(i)
    runner = unittest.TextTestRunner()
    runner.run(suit)




