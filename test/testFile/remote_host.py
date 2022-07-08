from fabric import Connection

def host_command():
    user = 'root'
    host = '192.168.3.211'
    password = '123456'

    c = Connection(host = f'{user}@{host}',
                   connect_kwargs = dict(
                       password = password
                   ))
    return c

