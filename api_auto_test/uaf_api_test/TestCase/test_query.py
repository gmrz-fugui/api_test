from api_auto_test.uaf_api_test.TestCase import *

class TestQuery(unittest.TestCase):
    """
    调用check_result时需要指定casename、api，body、expect
    """
    @classmethod
    def setUpClass(cls) -> None:
        # 创建CheckResult对象
        cls.ch = check_result.CheckResult()

    @parameterized.expand(check_result.data.test_data_params('test_device_list', random_num = True))
    def test_device_list(self, params, expect):
        """设备查询"""
        self.ch.check_result(casename = 'test_device_list', api = url[ 'device_list' ], body = params,
                             expect = expect)
    # @unittest.skip
    @parameterized.expand(check_result.data.test_data_params('test_support', random_num = True))
    def test_support(self, params, expect):
        """能力支持查询"""
        self.ch.check_result(casename = 'test_support', api = url[ 'support' ], body = params,
                             expect = expect)
    # @unittest.skip
    @parameterized.expand(check_result.data.test_data_params('test_v2_support', random_num = True))
    def test_v2_support(self, params, expect):
        """能力支持查询_V2"""
        self.ch.check_result(casename = 'test_v2_support', api = url[ 'support_v2' ], body = params,
                             expect = expect)
    # @unittest.skip
    @parameterized.expand(check_result.data.test_data_params('test_reg_status', random_num = True))
    def test_reg_status(self, params, expect):
        """用户开通状态查询"""
        self.ch.check_result(casename = 'test_reg_status', api = url[ 'reg_status' ], body = params,
                             expect = expect)
    # @unittest.skip
    def test_cert_delete(self):
        """证书：注销"""
        self.ch.check_result(casename = 'test_cert_delete', api = url[ 'delete' ])

if __name__ == '__main__':
    unittest.main()
