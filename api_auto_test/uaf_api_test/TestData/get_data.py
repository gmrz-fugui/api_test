from api_auto_test.uaf_api_test.DataBase import database
import copy
import json
import random

rd = random.randint(10000, 99999999)

class GetDataByID:
    """根据接口id获取所有数据"""

    def __init__(self):
        sql_parames = "select * from testcase"
        self.list_parames = list(database.db_case(sql_parames))  # 先获取所有接口用例的参数

    @staticmethod
    def send_uafResponse(uafResponse, context, num):
        # 拼装context和uafResponse
        if isinstance(uafResponse, str):
            dic = {
                "uafResponse": '[{}]'.format(uafResponse)
            }
            if type(context[num]) is tuple:
                context[ num ][ 0 ].update(**dic)
            else:
                context[ num ].update(**dic)
        else:
            context[ num ].update(**uafResponse)
        return context

    def group_params(self, api_id):
        # 根据传递的接口id，获取对应接口的用例参数
        lst = [ ]
        for i in self.list_parames:
            if i[ 1 ] == api_id:
                lst.append(i)
        return lst

    def get_data(self, api_id_master, api_id_slave = None):
        """
        数据组装
        1、获取主接口请求参数
        2、循环组装从接口请求参数
        """
        sql_context = "select context from api where api_id = {}".format(api_id_master)
        master_context = json.loads(database.db_case(sql_context)[ 0 ][ 0 ])  # 根据主接口id获取context请求数据,json格式
        master_parames = self.group_params(api_id_master)  # 获取主接口的所有请求参数，列表存放
        group_data = [ ]  # 存放参数替换后的context，单接口的包含expect
        for param in range(len(master_parames)):
            # 按用例名称获取每一组的请求参数和预期结果，按统一格式存入列表
            caseID = master_parames[ param ][ 0 ]
            userName = master_parames[ param ][ 2 ]+str(rd)
            deviceID = master_parames[ param ][ 3 ]+str(rd)
            appID = master_parames[ param ][ 4 ]
            authType = master_parames[ param ][ 5 ]
            statusCode = master_parames[ param ][ 6 ]
            description = master_parames[ param ][ 7 ]
            ex_userName = master_parames[ param ][ 8 ]
            ex_deviceID = master_parames[ param ][ 9 ]
            ex_appID = master_parames[ param ][ 10 ]
            ex_authType = master_parames[ param ][ 11 ]
            if api_id_slave is not None:
                sql_context1 = "select context from api where api_id = {}".format(api_id_slave)
                slave_context = json.loads(database.db_case(sql_context1)[ 0 ][ 0 ])
                slave_context[ 'context' ][ 'appID' ] = appID
                if 'userName' in slave_context[ 'context' ]:
                    slave_context[ 'context' ][ 'userName' ] = userName
                if 'deviceID' in slave_context[ 'context' ]:
                    slave_context[ 'context' ][ 'deviceID' ] = deviceID
                if 'devices' in slave_context[ 'context' ]:
                    slave_context[ 'context' ][ 'devices' ][ 'deviceID' ] = deviceID
                if 'authType' in slave_context[ 'context' ]:
                    if type(slave_context[ 'context' ][ 'authType' ]) is list:
                        slave_context[ 'context' ][ 'authType' ].clear()
                        slave_context[ 'context' ][ 'authType' ].append(authType)
                    else:
                        slave_context[ 'context' ][ 'authType' ] = authType
                cont = copy.deepcopy(slave_context)
                group_data.append(cont)
            else:
                master_context[ 'context' ][ 'appID' ] = appID
                if 'userName' in master_context[ 'context' ]:
                    master_context[ 'context' ][ 'userName' ] = userName
                if 'deviceID' in master_context[ 'context' ]:
                    master_context[ 'context' ][ 'deviceID' ] = deviceID
                if 'devices' in master_context[ 'context' ]:
                    master_context[ 'context' ][ 'devices' ][ 'deviceID' ] = deviceID
                if 'authType' in master_context[ 'context' ]:
                    if type(master_context[ 'context' ][ 'authType' ]) is list:
                        master_context[ 'context' ][ 'authType' ].clear()
                        master_context[ 'context' ][ 'authType' ].append(authType)
                    else:
                        master_context[ 'context' ][ 'authType' ] = authType
                expect = {
                    "statusCode": statusCode,
                    "description": description,
                    "ex_userName": ex_userName+str(rd),
                    "ex_deviceID": ex_deviceID+str(rd),
                    "ex_appID": ex_appID,
                    "ex_authType": ex_authType,
                    "caseID": caseID
                }
                cont = copy.deepcopy(master_context)
                group_data.append((cont, {"expect": expect}))
        return group_data

