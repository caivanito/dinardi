import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

from ballot.environs import DB_CONFIG_ENVS

SQLITE = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db_.sqlite3'),
    }
}


POSTGRESQL = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': DB_CONFIG_ENVS.get('name'),
        'USER': DB_CONFIG_ENVS.get('user'),
        'PASSWORD': DB_CONFIG_ENVS.get('password'),
        'HOST': DB_CONFIG_ENVS.get('host'), # set in docker-compose.yml
        'PORT': DB_CONFIG_ENVS.get('port'), # default postgres port

    }
}
