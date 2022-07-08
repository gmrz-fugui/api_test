from BeautifulReport import BeautifulReport
from web_auto_test.le_login.TestCase import LoginCase, InstallPlug
from web_auto_test.le_login.TestCase import IndexCase
from web_auto_test.le_login.Common.common import report_path
import unittest


if __name__ == '__main__':
    suit = unittest.TestSuite()
    for case in InstallPlug.get_install_case() + \
                LoginCase.get_login_case() + \
                IndexCase.get_index_case():
        suit.addTest(case)
    run = BeautifulReport(suit)
    run.report(filename='TestReport', description='乐登录web自动化测试',
               report_dir=report_path)

