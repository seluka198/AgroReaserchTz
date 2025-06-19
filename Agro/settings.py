import os
from pathlib import Path

# Path ya msingi ya mradi
BASE_DIR = Path(__file__).resolve().parent.parent

# Key ya siri ya Django
SECRET_KEY = 'django-insecure-u1qn=gy=dz*t&@ycth%gi_ayz8#uqm!%izgda^&=pt*mon%+zj'
DEBUG = True
ALLOWED_HOSTS = []

# Seti za mazingira kwa ajili ya GDAL na PROJ
os.environ['PROJ_LIB'] = r"C:\Program Files\GDAL\projlib"
os.environ['GDAL_DATA'] = r"C:\Program Files\GDAL\gdal-data"
GDAL_LIBRARY_PATH = r"C:\Program Files\GDAL\gdal.dll"
GEOS_LIBRARY_PATH = r"C:\Program Files\GDAL\geos_c.dll"

# User custom model
AUTH_USER_MODEL = 'account.Account'
LOGIN_REDIRECT_URL = 'home'



OPENWEATHER_API_KEY = "c2bb6088d5ffe0b56a3e2ac1a16e2bae"


# Shapefile Path - Tangaza shapefile path kabla ya kuitumia
shapefile_path = os.path.join(BASE_DIR, 'exported_shapefiles', 'researchdata.shp')

# Database Configuration na PostGIS
DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'ward',  
        'USER': 'postgres',  
        'PASSWORD': '7131', 
        'HOST': 'localhost', 
        'PORT': '5432', 
    }
}


DB_HOST = 'localhost'  
DB_NAME = 'ward' 
DB_USER = 'postgres' 
DB_PASSWORD = '7131'


STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / "static",  
]
STATIC_ROOT = BASE_DIR / "staticfiles" 
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / "media"  

# Installed Apps
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'agroresearch',  
    'account', 
    'import_export',
]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


ROOT_URLCONF = 'Agro.urls'


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'agroresearch', 'templates')],  
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


WSGI_APPLICATION = 'Agro.wsgi.application'


AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Africa/Dar_es_Salaam'
USE_I18N = True
USE_TZ = True


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
