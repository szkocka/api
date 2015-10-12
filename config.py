import os

env = os.getenv('SERVER_SOFTWARE')
if env and env.startswith('Google App Engine/'):
    SQLALCHEMY_DATABASE_URI = 'mysql://root@/db?unix_socket=/cloudsql/szkocka-1080:db'
else:
    SQLALCHEMY_DATABASE_URI = 'mysql://root:toor@173.194.227.105/db'
