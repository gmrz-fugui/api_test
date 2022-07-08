from api_auto_test.uaf_api_test.TestCase import *

class TestErrCode(unittest.TestCase):
    """
    调用check_result时需要指定casename、api，body、expect
    """
    @classmethod
    def setUpClass(cls) -> None:
        # 创建CheckResult类对象
        cls.ch = check_result.CheckResult()

    @parameterized.expand(check_result.data.test_data_params('test_black_list', random_num = True))
    def test_black_list(self, params, expect):
        """厂商设备型号黑名单---statusCode:1412"""
        check_result.redis.del_redis_key('uaf.cache.equipment.forbid.1103')  # 删除厂商设备型号黑名单redis对应的key
        check_result.database.db_uap(check_result.sql_list.test_black_list[ 'sql' ])  # 1、添加厂商
        check_result.database.db_uap(check_result.sql_list.test_black_list[ 'sql2' ])  # 2、添加设备型号
        check_result.database.db_uap(check_result.sql_list.test_black_list[ 'sql3' ])  # 3、设备加入黑名单
        self.ch.check_result(casename = 'test_black_list', api = url[ 'reg_receive' ], body = params,
                             expect = expect)
    # @unittest.skip
    @parameterized.expand(check_result.data.test_data_params('test_white_list', random_num = True))
    def test_white_list(self, params, expect):
        """厂商不在白名单---statusCode:1411"""
        """
        场景说明：
        1、先创建一个厂商，并加入白名单，（因为白名单必须有一条数据，如果没数据，会直接返回1200，而不是1411）
        2、请求的deviceType设置为白名单以外的类型
        3、比如厂商VIVO加入白名单，请求deviceType设置为XIAOMI即可
        """
        check_result.redis.del_redis_key('uaf.cache.vendor.allow.1103')  # 删除厂商白名单redis对应的key
        check_result.database.db_uap(check_result.sql_list.test_white_list[ 'sql' ])  # 1、添加厂商
        check_result.database.db_uap(check_result.sql_list.test_white_list[ 'sql2' ])  # 2、厂商添加为白名单
        self.ch.check_result(casename = 'test_white_list', api = url[ 'reg_receive' ], body = params,
                             expect = expect)
    # @unittest.skip
    @parameterized.expand(check_result.data.test_data_params('test_policy_available', random_num = True))
    def test_policy_available(self, params, expect):
        """请求的策略在服务器上不可用---statusCode:1402"""
        """
        1、需要先添加redis厂商白名单key，value为空就可以，否则报1411
        2、有这个key，值为空，代表所有厂商都是白名单
        3、有这个key，值不为空，代表指定的厂商为白名单
        4、无key，代表都不在白名单
        """
        check_result.redis.add_redis_key('uaf.cache.vendor.allow.1103', '')
        self.ch.check_result(casename = 'test_policy_available', api = url[ 'reg_receive' ], body = params,
                             expect = expect)

if __name__ == '__main__':
    unittest.main()
