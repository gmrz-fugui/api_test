from BeautifulReport import BeautifulReport
from android_auto_test.zhiya_app.test_case import test_way
import unittest

if __name__ == '__main__':
    cases=[
        test_way.get_teacher_case()
    ]
    suit=unittest.TestSuite()
    for case in cases:
        suit.addTests(case)
    run = BeautifulReport(suit)
    run.report(filename='report', description='UI测试报告',
               report_dir='D:\\App_UI_Auto\\zhiya_app\\report')
