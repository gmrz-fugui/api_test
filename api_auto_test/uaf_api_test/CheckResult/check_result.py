from api_auto_test.uaf_api_test.DataBase import database, sql_list, redis_conn
from uaf_api_test.HttpRequest import httprequest
from api_auto_test.uaf_api_test.Config.config import url
from api_auto_test.uaf_api_test.TestClient import test_client
from api_auto_test.uaf_api_test.Logs import logs
from uaf_api_test.TestData import test_data

import unittest
import logging
import json

# logs.getlog()
data = test_data.TestData()
redis = redis_conn.Rdis()


class CheckResult(unittest.TestCase):

    def assert_result(self, response, expect):
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()[ 'statusCode' ], expect[ 'expect' ][ 'statusCode' ])
        self.assertEqual(response.json()[ 'description' ], expect[ 'expect' ][ 'description' ])

    def check_result(self, **kwargs):
        """"""
        """
        kwargs:接收不固定长度dict
        casename：用例名称，必传
        api：接口地址，必传
        body、expect：请求参数和预期结果，参数化时需要传递
        1：传递casename和api，校验statusCode和description
        2：传递casename、api、body、expect，参数化校验
        """
        if len(kwargs) == 2:
            logging.info("kwargs---" + str(kwargs))
            body = data.test_data(kwargs[ 'casename' ])
            self.assertTrue(body is not False, '找不到测试数据，请检查参数名或用例名称！--{}'.format(kwargs[ 'casename' ]))
            r = httprequest.http_request('post', api = kwargs[ 'api' ], data = body)
            logging.info(kwargs[ 'casename' ] + "---request：" + json.dumps(body))
            logging.info(kwargs[ 'casename' ] + "---response：" + json.dumps(r.json()))
            print(kwargs[ 'casename' ] + "---request:", body)
            print(kwargs[ 'casename' ] + "---response:", r.json())
            self.assertEqual(r.status_code, 200, "服务器响应状态有误！")
            self.assertEqual(r.json()[ 'statusCode' ], 1200, "接口返回状态有误！{}".format(r.json()))
            self.assertEqual(r.json()[ 'description' ], 'OK', "接口返回状态有误！{}".format(r.json()))
            return [ body, r ]
        if len(kwargs) == 4:
            logging.info("kwargs---" + str(kwargs))
            body = kwargs[ 'body' ]
            logging.info(kwargs[ 'casename' ] + "---request：" + json.dumps(kwargs[ 'body' ]))
            if kwargs[ 'casename' ] == 'test_black_list':
                r = httprequest.http_request('post', kwargs[ 'api' ], data = body)
                logging.info(kwargs[ 'casename' ] + "---request：" + json.dumps(body))
                logging.info(kwargs[ 'casename' ] + "---response：" + json.dumps(r.json()))
                print(kwargs[ 'casename' ] + "---request:", body)
                print(kwargs[ 'casename' ] + "---response:", r.json())
                redis.del_redis_key('uaf.cache.equipment.forbid.1103')  # 删除厂商设备型号黑名单redis对应的key
                database.db_uap(sql_list.test_black_list[ 'sql4' ])  # 删除黑名单设备
                database.db_uap(sql_list.test_black_list[ 'sql5' ])  # 删除设备型号
                database.db_uap(sql_list.test_black_list[ 'sql6' ])  # 删除厂商
                self.assert_result(r, kwargs[ 'expect' ])
                return [ body, r ]
            elif kwargs[ 'casename' ] == 'test_white_list':
                r = httprequest.http_request('post', kwargs[ 'api' ], data = body)
                logging.info(kwargs[ 'casename' ] + "---request：" + json.dumps(body))
                logging.info(kwargs[ 'casename' ] + "---response：" + json.dumps(r.json()))
                print(kwargs[ 'casename' ] + "---request:", body)
                print(kwargs[ 'casename' ] + "---response:", r.json())
                redis.del_redis_key('uaf.cache.vendor.allow.1103')  # 删除厂商白名单redis对应的key
                database.db_uap(sql_list.test_white_list[ 'sql3' ])  # 删除白名单
                database.db_uap(sql_list.test_white_list[ 'sql4' ])  # 删除厂商
                self.assert_result(r, kwargs[ 'expect' ])
                return [ body, r ]
            elif kwargs[ 'casename' ] == 'test_cert_reg_receive1':
                r = httprequest.http_request('post', kwargs[ 'api' ], data = body)
                logging.info(kwargs[ 'casename' ] + "---request：" + json.dumps(body))
                logging.info(kwargs[ 'casename' ] + "---response：" + json.dumps(r.json()))
                print(kwargs[ 'casename' ] + "---request:", body)
                print(kwargs[ 'casename' ] + "---response:", r.json())
                self.assert_result(r, kwargs[ 'expect' ])
                self.assertTrue('uafRequest' in r.json())
                self.assertEqual(json.loads(r.json()[ 'uafRequest' ])[ 0 ][ 'username' ],
                                 kwargs[ 'expect' ][ 'expect' ][ 'username' ])
            elif kwargs[ 'casename' ] == 'test_cert_reg_send2':
                reg_data = data.test_data_modify('test_cert_reg_receive2', ready = True)  # test_cert_reg_receive2数据
                r = httprequest.http_request('post', api = url[ 'reg_receive' ], data = reg_data)
                if r.json()[ 'statusCode' ] == 1200:
                    reg_uafRequest = r.json()[ 'uafRequest' ]
                else:
                    reg_uafRequest = ''
                reg_client_response = test_client.new_testclient_obj().cert_testclient(uafRequest = reg_uafRequest)
                # 组装send接口请求报文
                data.send_uafResponse('test_cert_reg_send2', reg_client_response)
                r1 = httprequest.http_request('post', api = kwargs[ 'api' ], data = body)
                logging.info(kwargs[ 'casename' ] + "---request：" + json.dumps(body))
                logging.info(kwargs[ 'casename' ] + "---response：" + json.dumps(r1.json()))
                print(kwargs[ 'casename' ] + "---request:", body)
                print(kwargs[ 'casename' ] + "---response:", r1.json())
                self.assert_result(r1, kwargs[ 'expect' ])
                # 预期结果
                keyids = json.loads(r1.json()[ 'uafRequest' ])[ 0 ][ 'policy' ][ 'accepted' ][ 0 ][ 0 ][ 'keyIDs' ][ 0 ]
                name = kwargs[ 'expect' ][ 'expect' ][ 'userName' ]
                appid = kwargs[ 'expect' ][ 'expect' ][ 'appID' ]
                deviceid = kwargs[ 'expect' ][ 'expect' ][ 'deviceID' ]
                auth_type = kwargs[ 'expect' ][ 'expect' ][ 'auth_type' ]
                exts = kwargs[ 'expect' ][ 'expect' ][ 'exts' ][ 'id' ]
                sql = "select cust_no,device_id,tenant_id,auth_type from t_authenticators where cust_no ='{}' " \
                      "and status=1".format(name)
                sq1 = "select count(*) from t_certificate where keyid = '{}'".format( keyids)
                result = database.db_uap(sql)
                # 查询数据库，比对userName/appID/deviceID/auth_type和响应参数的exts['id']
                self.assertEqual(name, result[ 0 ][ 0 ])
                self.assertEqual(deviceid, result[ 0 ][ 1 ])
                self.assertEqual(str(appid), result[ 0 ][ 2 ])
                self.assertEqual(str(auth_type), result[ 0 ][ 3 ])
                self.assertTrue('uafRequest' in r.json())
                self.assertTrue(database.db_uap(sq1)[ 0 ][ 0 ])
                self.assertEqual(exts, json.loads(r.json()[ 'uafRequest' ])[ 0 ][ 'header' ][ 'exts' ][ 0 ][ 'id' ])
            elif kwargs[ 'casename' ] == 'test_cert_auth_receive3':
                reg_data = data.test_data_modify('test_cert_reg_receive3', ready = True)  # test_cert_reg_receive3数据
                r = httprequest.http_request('post', api = url[ 'reg_receive' ], data = reg_data)  # 注册发起
                if r.json()[ 'statusCode' ] == 1200:
                    reg_uafRequest = r.json()[ 'uafRequest' ]
                else:
                    reg_uafRequest = ''
                # 注册调用client
                reg_client_response = test_client.new_testclient_obj().cert_testclient(uafRequest = reg_uafRequest)
                # 组装注册完成报文
                data.send_uafResponse('test_cert_reg_send3', reg_client_response)
                send = data.test_data_modify('test_cert_reg_send3', ready = True)
                # 注册完成请求
                r1 = httprequest.http_request('post', api = url[ 'reg_send' ], data = send)
                # send_uafRequest:存储证书调用java方法时传的参数
                if r1.json()[ 'statusCode' ] == 1200:
                    send_uafRequest = r1.json()[ 'uafRequest' ]
                    send_client_response = test_client.new_testclient_obj().save_cert_client(
                        uafRequest = send_uafRequest)
                    keyid = send_client_response[ 'keyId' ]
                else:
                    keyid = ''
                    # print("注册完成失败：",r1.json())
                # 获取更新证书状态为已安装的数据
                data_save_cert = data.test_data_modify('test_update_cert_status3', ready = True)
                data_save_cert[ 'context' ][ 'keyID' ] = keyid  # 替换keid
                dic = {
                    "uafResponse": "[{%s}]" % keyid
                }
                # 组装更新证书接口的数据
                data.send_uafResponse('test_update_cert_status3', dic)
                update = data.test_data_modify('test_update_cert_status3', ready = True)
                httprequest.http_request('post', api = url[ 'cert_update' ], data = update)
                # 认证发起请求
                r3 = httprequest.http_request('post', api = kwargs[ 'api' ], data = body)
                print(r3.json())
                logging.info(kwargs[ 'casename' ] + "---request：" + json.dumps(body))
                logging.info(kwargs[ 'casename' ] + "---response：" + json.dumps(r3.json()))
                self.assert_result(r3, kwargs[ 'expect' ])
                self.assertTrue('uafRequest' in r3.json())
                self.assertEqual(kwargs[ 'expect' ][ 'expect' ][ 'op' ],
                                 json.loads(r3.json()[ 'uafRequest' ])[ 0 ][ 'header' ][ 'op' ])
            elif kwargs[ 'casename' ] == 'test_cert_auth_send4':
                reg_data = data.test_data_modify('test_cert_reg_receive4', ready = True)  # test_cert_reg_receive4数据
                r = httprequest.http_request('post', api = url[ 'reg_receive' ], data = reg_data)  # 注册发起
                if r.json()[ 'statusCode' ] == 1200:
                    reg_uafRequest = r.json()[ 'uafRequest' ]
                else:
                    reg_uafRequest = ''
                # 注册调用client
                print("注册发起请求：", reg_data)
                print("注册发起响应：", r.json())
                reg_client_response = test_client.new_testclient_obj().cert_testclient(uafRequest = reg_uafRequest)
                # 组装注册完成报文
                data.send_uafResponse('test_cert_reg_send4', reg_client_response)
                send = data.test_data_modify('test_cert_reg_send4', ready = True)
                # 注册完成请求
                r1 = httprequest.http_request('post', api = url[ 'reg_send' ], data = send)
                print("注册完成请求：", send)
                print("注册完成响应：", r1.json())
                # send_uafRequest:存储证书调用java方法时传的参数
                if r1.json()[ 'statusCode' ] == 1200:
                    send_uafRequest = r1.json()[ 'uafRequest' ]
                    send_client_response = test_client.new_testclient_obj().save_cert_client(
                        uafRequest = send_uafRequest)
                    keyid = send_client_response[ 'keyId' ]
                else:
                    keyid = ''
                # 获取更新证书状态为已安装的数据
                data_save_cert = data.test_data_modify('test_update_cert_status4', ready = True)
                data_save_cert[ 'context' ][ 'keyID' ] = keyid  # 替换keid
                dic = {
                    "uafResponse": "[{%s}]" % keyid
                }
                # 组装更新证书接口的数据
                data.send_uafResponse('test_update_cert_status4', dic)
                update = data.test_data_modify('test_update_cert_status4', ready = True)
                print("更新证书请：", update)
                print("update响应:", httprequest.http_request('post', api = url[ 'cert_update' ], data = update).json())
                # 认证发起请求
                reg_data1 = data.test_data_modify('test_cert_auth_receive4', ready = True)
                r3 = httprequest.http_request('post', api = url[ 'auth_receive' ], data = reg_data1)
                print("认证发起请求：", reg_data1)
                print("认证发起响应：", r3.json())
                auth_uafRequest = r3.json()[ 'uafRequest' ]
                # cert_testclient请求需要的uafRequest
                __auth_client_response = test_client.new_testclient_obj().cert_auth_client(uafRequest = auth_uafRequest)
                print("client:", __auth_client_response)
                data.send_uafResponse('test_cert_auth_send4', __auth_client_response)
                r4 = httprequest.http_request('post', api = kwargs[ 'api' ], data = body)
                logging.info(kwargs[ 'casename' ] + "---request：" + json.dumps(body))
                logging.info(kwargs[ 'casename' ] + "---response：" + json.dumps(r4.json()))
                print("认证完成请求：", body)
                print("认证完成响应：", r4.json())
                self.assert_result(r4, kwargs[ 'expect' ])
                name = kwargs[ 'expect' ][ 'expect' ][ 'userName' ]
                appid = kwargs[ 'expect' ][ 'expect' ][ 'appID' ]
                deviceid = kwargs[ 'expect' ][ 'expect' ][ 'deviceID' ]
                auth_type = kwargs[ 'expect' ][ 'expect' ][ 'auth_type' ]
                sign_counter = kwargs[ 'expect' ][ 'expect' ][ 'sign_counter' ]
                p7data = kwargs[ 'expect' ][ 'expect' ][ 'exts' ]
                sql = "select cust_no,device_id,tenant_id,auth_type,sign_counter from t_authenticators " \
                      "where cust_no ='{}' and   status =1".format(name)
                result = (database.db_uap(sql))
                print("result", str(result))
                # print(result[0][0])
                # print('result[0][0]',result[0][0])
                # self.assertTrue(p7data in r4.json()[ 'exts' ])
                # self.assertEqual(name, result[ 0 ][ 0 ])
                # self.assertEqual(deviceid, result[ 0 ][ 1 ])
                # self.assertEqual(str(appid), result[ 0 ][ 2 ])
                # self.assertEqual(str(auth_type), result[ 0 ][ 3 ])
                # self.assertEqual(sign_counter, result[ 0 ][ 4 ])
            else:
                r = httprequest.http_request('post', kwargs[ 'api' ], data = body)
                logging.info(kwargs[ 'casename' ] + "---request：" + json.dumps(body))
                logging.info(kwargs[ 'casename' ] + "---response：" + json.dumps(r.json()))
                print(kwargs[ 'casename' ] + "---request:", body)
                print(kwargs[ 'casename' ] + "---response:", r.json())
                self.assert_result(r, kwargs[ 'expect' ])
                return [ body, r ]
