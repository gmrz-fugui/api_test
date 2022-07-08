import unittest


class MyTestLoader(unittest.TestLoader):
    def getTestCaseNames(self, testcase_class):
        # 调用父类的获取“测试方法”函数
        test_names = super().getTestCaseNames(testcase_class)
        # 拿到测试方法list
        testcase_methods = list(testcase_class.__dict__.keys())
        # 根据list的索引对testcase_methods进行排序
        test_names.sort(key = testcase_methods.index)
        # 返回测试方法名称
        return test_names

# if __name__ == '__main__':
#     from api_auto_test.uaf_api_test.TestCase import test_cert,test_query,test_err_code
#     name = test_cert.TestCert
#     loadre = MyTestLoader()
#     print(loadre.getTestCaseNames(name))
#     lst = list(name.__dict__.keys())
#     print([i for i in lst if 'test' in i])
