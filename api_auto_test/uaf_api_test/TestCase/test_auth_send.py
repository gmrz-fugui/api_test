from api_auto_test.uaf_api_test.TestCase import *

data = get_data.GetDataByID()  # 创建获取数据对象
check = assert_result.AssertResult()  # 结果校验对象
auth_send_context_list = data.get_data(4)  # 认证完成所有context
logs.getlog() # 调用日志方法

class TestAuthSend(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        global auth_send_context_list
        reg_recv_context_list = data.get_data(4, 1)  # 注册发起所有context
        reg_send_context_list = data.get_data(4, 2)  # 注册完成所有context
        updata_context_list = data.get_data(4, 5)  # 更新证书的context
        auth_recv_context_list = data.get_data(4, 3)  # 认证发起所有context
        test_client.new_testclient_obj().jvmStart()  # 启动java虚拟机
        for i in range(len(auth_recv_context_list)):
            # 注册发起
            r = check.requests(check = False, api = url[ 'reg_receive' ],parame = reg_recv_context_list[ i ])
            logging.info('认证完成接口用例：注册发起：request_{}---{}'.format(i + 1,json.dumps(reg_recv_context_list[ i ])))
            logging.info('认证完成接口用例：注册发起：response_{}---{}'.format(i + 1,json.dumps(r.json())))
            if r.json()[ 'statusCode' ] == 1200:
                reg_uafRequest = r.json()[ 'uafRequest' ]
            else:
                reg_uafRequest = '注册发起响应uafRequest：{}'.format(r.json()[ 'description' ])
            # 调用testclient
            reg_client_response = test_client.new_testclient_obj().cert_testclient(uafRequest = reg_uafRequest)
            logging.info('认证完成接口用例： 注册发起后client返回：{}'.format(reg_client_response))
            # 组装send请求报文
            data.send_uafResponse(reg_client_response, reg_send_context_list, i)
            # 注册send请求发起
            r1 = check.requests(check = False,api = url[ 'reg_send' ],parame = reg_send_context_list[ i ])
            logging.info('认证完成接口用例：注册完成：request_{}---{}'.format(i + 1, json.dumps(reg_send_context_list[ i ])))
            logging.info('认证完成接口用例：注册完成：response_{}---{}'.format(i + 1, json.dumps(r1.json())))
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
            # 更新证书状态发起请求
            r2 = check.requests(check = False,api = url[ 'cert_update' ], parame = up_data[ i ])
            logging.info('认证完成接口用例：更新证书状态：request_{}---{}'.format(i + 1, json.dumps(up_data[ i ])))
            logging.info('认证完成接口用例：更新证书状态：response_{}---{}'.format(i + 1, json.dumps(r2.json())))
            # 认证发起请求
            r3 = check.requests(check = False,api = url[ 'auth_receive' ],parame = auth_recv_context_list[ i ])
            logging.info('认证完成接口用例：认证发起：request_{}---{}'.format(i + 1, json.dumps(auth_recv_context_list[ i ])))
            logging.info('认证完成接口用例：认证发起：response_{}---{}'.format(i + 1, json.dumps(r3.json())))
            if r3.json()[ 'statusCode' ] == 1200:
                auth_uafRequest = r3.json()[ 'uafRequest' ]
            else:
                auth_uafRequest = "认证完成响应：{}".format(r3.json()[ 'description' ])
            __auth_client_response = test_client.new_testclient_obj().cert_auth_client(uafRequest = auth_uafRequest)
            data.send_uafResponse(__auth_client_response, auth_send_context_list, i)  # 组装认证完成报文
        return auth_send_context_list

    @parameterized.expand(auth_send_context_list)
    def test_auth_send(self, parame, expect):
        """认证完成"""
        check.requests(casename = 'test_auth_send', api = url[ 'auth_send' ], parame = parame,
                       expect = expect)

if __name__ == '__main__':
    unittest.main()
