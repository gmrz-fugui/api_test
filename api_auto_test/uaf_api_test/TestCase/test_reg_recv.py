from api_auto_test.uaf_api_test.TestCase import *

data = get_data.GetDataByID()

class TestRegReceive(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.check = assert_result.AssertResult()  # 结果校验对象


    @parameterized.expand(data.get_data(1)) # 根据api_id获取参数化需要的数据
    def test_reg_receive(self, parame, expect):
        """注册发起"""
        self.check.requests(casename = 'test_reg_receive', api = url[ 'reg_receive' ], parame = parame,
                             expect = expect)


if __name__ == '__main__':
    unittest.main()
