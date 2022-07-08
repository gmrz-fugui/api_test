from uaf_api_test.HttpRequest import httprequest
from api_auto_test.uaf_api_test.DataBase import database
from api_auto_test.uaf_api_test.Logs import logs
import unittest
import logging
import json

logs.getlog()

class AssertResult(unittest.TestCase):

    @staticmethod
    def search(parame):
        # 根据userName查询t_authenticators表,校验库里参数
        userName = parame['context']['userName']
        sql = "select cust_no,device_id,auth_type,tenant_id from t_authenticators WHERE " \
              "status=1 and cust_no='{}'".format(userName)
        return database.db_uap(sql)[0]

    def assert_result(self, response, expect,parame = None):
        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(response.json()[ 'statusCode' ]), expect[ 'expect' ][ 'statusCode' ])
        self.assertEqual(response.json()[ 'description' ], expect[ 'expect' ][ 'description' ])
        if parame is not None:
            db_data = self.search(parame)
            self.assertEqual(db_data[0] , expect[ 'expect' ]['ex_userName'])
            self.assertEqual(db_data[ 1 ], expect[ 'expect' ][ 'ex_deviceID' ])
            self.assertEqual(db_data[ 2 ], expect[ 'expect' ][ 'ex_authType' ])
            self.assertEqual(db_data[ 3 ], expect[ 'expect' ][ 'ex_appID' ])

    def requests(self,check = True, db = False,**kwargs):
        # 发送http请求并调用结果验证
        # check：默认校验结果
        # db：默认不校验数据库
        # 四个位置参数：casename、api、parame、expect
        api = kwargs[ 'api' ]
        parame = kwargs[ 'parame' ]
        r = httprequest.http_request('post', api = api, data = parame)
        if check:
            if db:
                logging.info(kwargs[ 'casename' ] + "--- request:{}".format(json.dumps(parame)))
                logging.info(kwargs[ 'casename' ] + "--- response:{}".format(r.json()))
                print(kwargs[ 'casename' ] + "--- request:", parame)
                print(kwargs[ 'casename' ] + "--- response:",r.json())
                expect = kwargs[ 'expect' ]
                self.assert_result(r, expect,parame)
            else:
                logging.info(kwargs[ 'casename' ] + "--- request:{}".format(json.dumps(parame)))
                logging.info(kwargs[ 'casename' ] + "--- response:{}".format(r.json()))
                print(kwargs[ 'casename' ] + "--- request:", parame)
                print(kwargs[ 'casename' ] + "--- response:", r.json())
                expect = kwargs[ 'expect' ]
                self.assert_result(r, expect)
        else:
            return r
