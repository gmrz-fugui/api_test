from api_auto_test.uaf_api_test.TestCase import *

data = get_data.GetDataByID()  # 创建获取数据对象
check = assert_result.AssertResult()  # 结果校验对象
send_context_list = data.get_data(2)  # 获取注册完成所有context

logs.getlog()


class TestRegSend(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        global send_context_list
        reg_context_list = data.get_data(2, 1)  # 根据send接口，获取注册发起所有请求参数
        test_client.new_testclient_obj().jvmStart()  # 启动java虚拟机
        for i in range(len(reg_context_list)):
            r = check.requests(check = False, api = url[ 'reg_receive' ], parame = reg_context_list[ i ])
            logging.info('注册完成接口用例：注册发起：request_{}---{}'.format(i + 1, json.dumps(reg_context_list[ i ])))
            logging.info('注册完成接口用例：注册发起：response_{}---{}'.format(i + 1, json.dumps(r.json())))
            if r.json()[ 'statusCode' ] == 1200:
                reg_uafRequest = r.json()[ 'uafRequest' ]
            else:
                reg_uafRequest = '注册发起响应uafRequest：{}'.format(r.json()[ 'description' ])
            # 调用testclient
            reg_client_response = test_client.new_testclient_obj().cert_testclient(uafRequest = reg_uafRequest)
            # 组装send请求报文
            data.send_uafResponse(reg_client_response, send_context_list, i)
        return send_context_list

    @parameterized.expand(send_context_list)
    def test_reg_send(self, parame, expect):
        """注册完成"""
        check.requests(db = True, casename = 'test_reg_send', api = url[ 'reg_send' ], parame = parame,
                       expect = expect)

if __name__ == '__main__':
    unittest.main()
