import os
import django
from django.conf import settings


DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),'data')

DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': '{}/db.athletics'.format(DATA_DIR),
        }
    }


# HAS TO RUN FIRST
settings.configure(DATABASES=DATABASES)
django.setup()
