import redis
import time
def execute_redis(mobile):
    """
    :return:返回缓存连接对象
    """
    host = '192.168.6.132'
    port = 5399
    try:
        conn = redis.StrictRedis(host=host, port=port,db=8,decode_responses=True)
    except Exception as e:
        print('redis connection error：{}'.format(e))
        return 0
    key = '{}'.format(mobile) # 拼接手机号对应的key
    n=0 # 查询次数
    while True:
        # 每0.5秒查询redis是否有手机验证码，最长等待20秒
        n += 1
        mobile_code = conn.get(key) # 根据key获取手机验证码
        if mobile_code:
            return mobile_code.replace('"',"")
        if n==40:
            print('redis没有收到这个手机号的验证码：{}'.format(mobile))
            return -1
        time.sleep(0.5)
