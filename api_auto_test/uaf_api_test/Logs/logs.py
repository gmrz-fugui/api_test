from api_auto_test.uaf_api_test.Config import config
import logging
import time
import os

# 日志级别设置
level=logging.DEBUG

def getlog(logger = None):
    """
     指定保存日志的文件路径，日志级别，以及调用文件
     将日志存入到指定的文件中
    """
    # 创建一个logger
    logger = logging.getLogger(logger)
    logger.setLevel(level)
    if not logger.handlers:
        log_path = config.path[ 'log_path' ]
        log_time = time.strftime("%Y_%m_%d")
        # log文件名不能改
        log_name =log_path + "/"  + log_time + '.log'
        fh = logging.FileHandler(log_name, encoding = 'utf-8')
        fh.setLevel(level)
        ch = logging.StreamHandler()
        ch.setLevel(level)
        # 定义handler的输出格式
        formatter = logging.Formatter(
            '[%(asctime)s] %(filename)s->%(funcName)s line:%(lineno)d [%(levelname)s]%(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        # 给logger添加handler
        logger.addHandler(fh)
        logger.addHandler(ch)
        fh.close()
        ch.close()
        return logger

def del_logfile():
    """保留7个log，删除最近7天以外的log"""
    """"""
    log_dir = config.path[ 'log_path' ]
    index = []
    file = os.listdir(log_dir)
    if len(file)>7:
        lst = [ int(i.replace('_', '').replace('.log', '')) for i in file ]
        while True:
            value = min(lst)
            idx = lst.index(value)
            index.append(idx)
            lst[ idx ] = 2022222222
            if len(lst) - len(index) == 7:
                break
        return [ os.remove(str(log_dir + file[ j ])) for j in index ]