from api_auto_test.uaf_api_test.Config import config
import redis

host = config.conf['redis']['host']
port = config.conf['redis']['port']
passwd = config.conf['redis']['password']

class Rdis:

    def __init__(self):
        if passwd:
            conn = redis.ConnectionPool(
                host = host,
                port = port,
                db = 1,
                password = passwd,
                decode_responses = True
            )
        else:
            conn = redis.ConnectionPool(
                host = host,
                port = port,
                db = 1,
                password = passwd,
                decode_responses = True
            )
        self.res = redis.StrictRedis(connection_pool = conn)

    def redis_conn(self):
        # 判断redis连接是否正常
        try:
            n = self.res.exists("")  # 返回0或1
            return n
        except Exception as e:
            return e

    def del_redis_key(self,key):
        # 删除key
        return  self.res.delete(key)

    def add_redis_key(self,key,value):
        # 添加key
        return self.res.sadd(key,value)

    def query_redis_key(self,key):
        # 查询是否存在key，0 or 1
        return self.res.exists(key)

    def query_num_key(self,key):
        # 返回key的数量
        return len(self.res.keys(key))

    def get_key(self,key):
        return self.res.get(key)

# if __name__ == '__main__':
#     r = Rdis()
#     print(r.query_num_key('u*'))
#     pass