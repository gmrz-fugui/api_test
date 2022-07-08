# import sys
# sys.path.append('/usr/local/tomcat/webapps/jenkins/workspace/TestApi') #
# jenkins用到
from api_auto_test.uaf_api_test.TestCase import test_cert, test_query,test_err_code, \
    test_cert_modify,test_reg_recv,test_reg_send,test_auth_recv,test_auth_send,test_delete
from api_auto_test.uaf_api_test.DataBase import database,redis_conn
from api_auto_test.uaf_api_test.TestClient import test_client
from api_auto_test.uaf_api_test.Logs import logs
from uaf_api_test.CheckResult import case_sort
from api_auto_test.uaf_api_test.Config.config import path
from BeautifulReport import BeautifulReport
import time
import unittest
import sys

if __name__ == '__main__':
    redis_con = redis_conn.Rdis()
    test_client.new_testclient_obj().jvmStart()
    sys.stderr.write('准备执行接口自动化测试...    {}    '.format(
        time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))) + '\n' + '\n')
    # 判断数据库连接是否正常
    if isinstance(database.db_uap(), database.pymysql.connections.Connection):
        # 判断redis连接是否正常
        if redis_con.redis_conn()==0 or redis_con.redis_conn() == 1:
            className = [
                # test_cert.TestCert,
                # test_query.TestQuery,
                # test_err_code.TestErrCode,
                # test_cert_modify.TestCertModify,
                test_reg_recv.TestRegReceive,
                test_reg_send.TestRegSend,
                test_auth_recv.TestAuthRecv,
                test_auth_send.TestAuthSend
                # test_delete.TestDelete
                # test_code.TestCode
            ]
            suit = unittest.TestSuite()
            loader = case_sort.MyTestLoader() # 用例顺序重新排序
            for i in className:
                suit.addTest(loader.loadTestsFromTestCase(i))
            run = BeautifulReport(suit)
            run.report(filename='TestReport', description='UAF接口自动化测试报告',
                       report_dir=path['report_dir'])
            # test_cert.test_client.new_testclient_obj().jvmShutdown()
            logs.del_logfile()  # 是否需要删除旧的日志
        else:
            raise ConnectionError(redis_con.redis_conn())
    else:
        raise ConnectionError(database.db_uap())
