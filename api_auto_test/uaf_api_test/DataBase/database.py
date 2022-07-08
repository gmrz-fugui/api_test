from api_auto_test.uaf_api_test.Config import config
import pymysql

def db_uap(sql= ""):
    """
    连接业务库
    项目运行时不传sql，判断是否连接成功
    :param sql:传入需要执行的sql语句
    :return:
    """
    try:
        db = pymysql.connect(**config.conf['mysql'])
        if sql:
            cur = db.cursor()
            cur.execute(sql)
            db.commit()
            cur.close()
            db.close()
            return cur.fetchall()
        return db
    except Exception as e:
        return 'database connection error：\t{}'.format(e)

def db_case(sql):
    """
    连接测试用例库
    :param sql:传入需要执行的sql语句
    :return:
    """
    try:
        db = pymysql.connect(**config.conf['case_mysql'])
        if sql:
            cur = db.cursor()
            cur.execute(sql)
            db.commit()
            cur.close()
            db.close()
            return cur.fetchall()
        return db
    except Exception as e:
        return 'database connection error：\t{}'.format(e)

if __name__ == '__main__':

    print(db_uap())