import os
from pathlib import Path
import environ
env = environ.Env()
BASE_DIR = Path(__file__).resolve().parent.parent

# Take environment variables from .env file
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': env('DATABASE_NAME'),
        'USER': env('DATABASE_USER'),
        'PASSWORD': env('DATABASE_PASSWORD'),
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}

