from api_auto_test.uaf_api_test.Config.config import path
import yaml
import random

# 测试启动后，随机生成username和deviceid，保持不变，直到测试结束
username = 'test123-gmrz{}'.format(random.randint(111111111, 9999999999))
deviceid = 'HW512Dqw5zr5QWERTYUIOPA9D6GHJKLZXtcs{}'.format(random.randint(111111111, 9999999999))


class TestData:
    def __init__(self):
        try:
            # 打开test_data用例
            with open(str(path[ 'case_yalm' ]), encoding = 'utf-8') as f:
                # 用例源文件
                self.data = yaml.load(f, Loader = yaml.FullLoader)
        except Exception as e:
            raise Exception('数据格式有误：' + str(e))
        try:
            # 打开test_data1用例
            with open(str(path[ 'cert_modify_yalm' ]), encoding = 'utf-8') as f:
                # 用例源文件
                self.data1 = yaml.load(f, Loader = yaml.FullLoader)
        except Exception as e:
            raise Exception('数据格式有误：' + str(e))

    def test_data(self, case_name, random_num = False):
        # 不需要参数化的用例
        """
        :param random_num: 如果为True，重新生成userName和deviceID
        :param case_name: 根据用例名称动态填充数据，-1代表要测试空值
        :return:
        """
        if random_num:
            userName = 'test-fg{}'.format(random.randint(111111111, 9999999999))
            deviceID = 'HW5Dqw5zr5QWERTYUIOPA9D6GHJXtcsfg{}'.format(random.randint(111111111, 9999999999))
        else:
            userName = username
            deviceID = deviceid
        try:
            all_data = self.data[ case_name ]
        except:
            return False
        case_data = all_data
        if 'userName' in case_data[ 'context' ]:
            if len(case_data[ 'context' ][ 'userName' ]) == 0:
                case_data[ 'context' ][ 'userName' ] = userName
            if case_data[ 'context' ][ 'userName' ] == '-1':
                case_data[ 'context' ][ 'userName' ] = ''
        if 'devices' in case_data[ 'context' ]:
            if len(case_data[ 'context' ][ 'devices' ][ 'deviceID' ]) == 0:
                case_data[ 'context' ][ 'devices' ][ 'deviceID' ] = deviceID
            if all_data[ 'context' ][ 'devices' ][ 'deviceID' ] == '-1':
                case_data[ 'context' ][ 'devices' ][ 'deviceID' ] = ''
        if "deviceID" in case_data[ 'context' ]:
            if len(case_data[ 'context' ][ 'deviceID' ]) == 0:
                case_data[ 'context' ][ 'deviceID' ] = deviceID
            if case_data[ 'context' ][ 'deviceID' ] == '-1':
                case_data[ 'context' ][ 'deviceID' ] = ''
        return case_data

    def test_data_params(self, case_name, random_num = False):
        # 需要参数化的用例，根据用例名称，按参数化格式循环组装
        list_data = [ ]
        userName = username
        deviceID = deviceid
        try:
            all_data = self.data[ case_name ]
        except:
            return False
        case_data = all_data
        for i in range(len(case_data)):
            if random_num:
                userName = 'test-fg{}'.format(random.randint(111111111, 9999999999))
                deviceID = 'HW5Dqw5zr5QWERTYUIOPA9D6GHJXtcsfg{}'.format(random.randint(111111111, 9999999999))
            context = case_data[ i ][ 0 ][ 'context' ]
            if 'userName' in context:
                if len(context[ 'userName' ]) == 0:
                    context[ 'userName' ] = userName
            if 'devices' in context:
                if len(context[ 'devices' ][ 'deviceID' ]) == 0:
                    context[ 'devices' ][ 'deviceID' ] = deviceID
            if "deviceID" in context:
                if len(context[ 'deviceID' ]) == 0:
                    context[ 'deviceID' ] = deviceID
            list_data.append((case_data[ i ][ 0 ], case_data[ i ][ 1 ]))
        return list_data

    def test_data_modify(self, case_name , ready=False):
        # 用例给啥就传啥，啥都不改
        # ready:代表直接返回这条用单条数据，比如test_cert_reg_receive2，否则循环生成参数化数据
        if ready:
            try:
                all_data = self.data1[ case_name ]
                return all_data
            except:
                return False
        list_data = [ ]
        try:
            all_data = self.data1[ case_name ]
        except:
            return False
        case_data = all_data
        for i in range(len(case_data)):
            list_data.append((case_data[ i ][ 0 ], case_data[ i ][ 1 ]))
        return list_data

    def send_uafResponse(self, case_name, uafResponse ):
        """
        处理testclient返回的数据uafResponse，组装send请求报文
        :param case_name:用例名称
        :param uafResponse:testclient返回的uafResponse
        :return:
        """
        all_data = self.data
        if case_name in all_data:
            if uafResponse is not None:
                if isinstance(uafResponse, str):
                    dic = {
                        "uafResponse": '[{}]'.format(uafResponse)
                    }
                    all_data[ case_name ].update(**dic)
                else:
                    all_data[ case_name ].update(**uafResponse)
            else:
                pass
            return all_data
        send_datas = self.data1[ case_name ]
        if isinstance(send_datas, list):
            if uafResponse is not None:
                for i in range(len(send_datas)):
                    if isinstance(uafResponse, str):
                        dic = {
                            "uafResponse": '[{}]'.format(uafResponse)
                        }
                        send_datas[i][0].update(**dic)
                    else:
                        send_datas[i][0].update(**uafResponse)
        else:
            if uafResponse is not None:
                if isinstance(uafResponse, str):
                    dic = {
                        "uafResponse": '[{}]'.format(uafResponse)
                    }
                    send_datas.update(**dic)
                else:
                    send_datas.update(**uafResponse)
            else:
                pass
