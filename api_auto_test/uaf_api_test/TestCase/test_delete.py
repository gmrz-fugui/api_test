from api_auto_test.uaf_api_test.TestCase import *


data = get_data.GetDataByID()  # 创建获取数据对象
check = assert_result.AssertResult() # 结果校验对象
delete_context_list = data.get_data(6)

logs.getlog() # 调用日志方法

class TestDelete(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        global delete_context_list
        reg_recv_context_list = data.get_data(6, 1)  # 注册发起所有context
        reg_send_context_list = data.get_data(6, 2)  # 注册完成所有context
        test_client.new_testclient_obj().jvmStart()  # 启动java虚拟机
        for i in range(len(delete_context_list)):
            r = check.requests(check = False, api = url[ 'reg_receive' ], parame = reg_recv_context_list[ i ])
            logging.info('注销接口用例：注册发起：request_{}---{}'.format(i + 1, json.dumps(reg_recv_context_list[ i ])))
            logging.info('注销接口用例：注册发起：response_{}---{}'.format(i + 1, json.dumps(r.json())))
            if r.json()[ 'statusCode' ] == 1200:
                reg_uafRequest = r.json()[ 'uafRequest' ]
            else:
                reg_uafRequest = '注册发起响应uafRequest：{}'.format(r.json()[ 'description' ])
            # 调用testclient
            reg_client_response = test_client.new_testclient_obj().cert_testclient(uafRequest = reg_uafRequest)
            logging.info('注销接口用例：注册发起后client返回:{}'.format(reg_client_response))
            # 组装send请求报文
            data.send_uafResponse(reg_client_response, reg_send_context_list, i)
            # send请求发起
            r1 = check.requests(check = False, api = url[ 'reg_send' ], parame = reg_send_context_list[ i ])
            logging.info('注销接口用例：注册完成：request_{}---{}'.format(i + 1, json.dumps(reg_send_context_list[ i ])))
            logging.info('注销接口用例：注册完成：response_{}---{}'.format(i + 1, json.dumps(r1.json())))
        return delete_context_list

    @parameterized.expand(delete_context_list)
    def test_delete(self,parame,expect):
        """注销"""
        check.requests(casename = 'test_delete', api = url[ 'delete' ], parame = parame,
                       expect = expect)

if __name__ == '__main__':
    unittest.main()