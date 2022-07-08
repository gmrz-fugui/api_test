from api_auto_test.uaf_api_test.TestCase import *


data = get_data.GetDataByID()  # 创建获取数据对象
check = assert_result.AssertResult() # 结果校验对象
auth_recv_context_list = data.get_data(3)  # 认证发起所有context

logs.getlog() # 调用日志方法

class TestAuthRecv(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        global auth_recv_context_list
        reg_recv_context_list = data.get_data(3, 1)  # 注册发起所有context
        reg_send_context_list = data.get_data(3, 2)  # 注册完成所有context
        updata_context_list = data.get_data(3, 5)  # 更新证书的context
        test_client.new_testclient_obj().jvmStart()  # 启动java虚拟机
        for i in range(len(auth_recv_context_list)):
            r = check.requests(check = False, api = url[ 'reg_receive' ], parame = reg_recv_context_list[ i ])
            logging.info('认证发起接口用例：注册发起：request_{}---{}'.format(i + 1, json.dumps(reg_recv_context_list[ i ])))
            logging.info('认证发起接口用例：注册发起：response_{}---{}'.format(i + 1, json.dumps(r.json())))
            if r.json()[ 'statusCode' ] == 1200:
                reg_uafRequest = r.json()[ 'uafRequest' ]
            else:
                reg_uafRequest = '注册发起响应uafRequest：{}'.format(r.json()[ 'description' ])
            # 调用testclient
            reg_client_response = test_client.new_testclient_obj().cert_testclient(uafRequest = reg_uafRequest)
            logging.info('认证发起接口用例：注册发起后client返回:{}'.format(reg_client_response))
            # 组装send请求报文
            data.send_uafResponse(reg_client_response, reg_send_context_list, i)
            # send请求发起
            r1 = check.requests(check = False, api = url[ 'reg_send' ], parame = reg_send_context_list[ i ])
            logging.info('认证发起接口用例：注册完成：request_{}---{}'.format(i + 1, json.dumps(reg_send_context_list[ i ])))
            logging.info('认证发起接口用例：注册完成：response_{}---{}'.format(i + 1, json.dumps(r1.json())))
            if r1.json()[ 'statusCode' ] == 1200:
                send_uafRequest = r1.json()[ 'uafRequest' ]
                send_client_response = test_client.new_testclient_obj().save_cert_client(
                    uafRequest = send_uafRequest)
                keyid = send_client_response[ 'keyId' ]
            else:
                keyid = ''
            updata_context_list[ i ][ 'context' ].update({'keyID': keyid})
            dic = {
                "uafResponse": "[{%s}]" % keyid
            }
            up_data = data.send_uafResponse(dic, updata_context_list, i)  # 组装后的更新证书接口数据
            r2 = check.requests(check = False, api = url[ 'cert_update' ], parame = up_data[ i ])
            logging.info('认证发起接口用例：更新证书状态：request_{}---{}'.format(i + 1, json.dumps(up_data[ i ])))
            logging.info('认证发起接口用例：更新证书状态：response_{}---{}'.format(i + 1, json.dumps(r2.json())))
        return auth_recv_context_list

    @parameterized.expand(auth_recv_context_list)
    def test_auth_recv(self, parame, expect):
        """认证发起"""
        check.requests(casename = 'test_auth_recv', api = url[ 'auth_receive' ], parame = parame,
                       expect = expect)

if __name__ == '__main__':
    unittest.main()
