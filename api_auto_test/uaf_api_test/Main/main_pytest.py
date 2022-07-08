from api_auto_test.uaf_api_test.TestClient import test_client
import os
import pytest

if __name__ == '__main__':

    test_client.new_testclient_obj().jvmStart()
    casefile= '../TestCase'
    pytest.main (['--alluredir', '../report/result',casefile])
    os.system('allure generate ../report/result -o ../report/html --clean ')
    test_client.new_testclient_obj().jvmShutdown()







