from pathlib import Path
import environ

BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env()
env.read_env(env.str('ENV_PATH', '.env'))

ENV_NAME = env.str('ENV_NAME')

SECRET_KEY = env('SECRET_KEY')

DEBUG = env.bool('DEBUG')
TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = ["*"]

CORS_ALLOWED_ORIGINS = env.list('CORS_ALLOWED_ORIGINS')
CORS_ALLOW_CREDENTIALS = True

FRONTEND_URL = env.str('FRONTEND_URL', default='http://localhost:4200')


INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    'django.contrib.sites',
    
    "django_extensions",
    "corsheaders",
    
    'drf_yasg',
    'rest_framework',
    'rest_framework_api_key',
    'rest_framework.authtoken',
    'dj_rest_auth',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'dj_rest_auth.registration',
    
    'django_filters',
    "taggit",
     
    'org',
    'core',
    'client',
    
]

SITE_ID = 1

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    'djangorestframework_camel_case.middleware.CamelCaseMiddleWare',
]

ROOT_URLCONF = "mrc.urls"

LOCALE_PATHS = (
    BASE_DIR / 'locale',
)

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "mrc.wsgi.application"

DATABASES = {
    'default': env.db_url('DATABASE_URL')
}


AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

REST_FRAMEWORK = {
    'JSON_UNDERSCOREIZE': {
        'no_underscore_before_number': True,
    },
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    "DEFAULT_PERMISSION_CLASSES": [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_RENDERER_CLASSES': (
        'djangorestframework_camel_case.render.CamelCaseJSONRenderer',
        'djangorestframework_camel_case.render.CamelCaseBrowsableAPIRenderer',
    ),
    'DEFAULT_PARSER_CLASSES': (
        'djangorestframework_camel_case.parser.CamelCaseFormParser',
        'djangorestframework_camel_case.parser.CamelCaseMultiPartParser',
        'djangorestframework_camel_case.parser.CamelCaseJSONParser',
    ),
    
}

REST_AUTH = {
    'USE_JWT': True,
    'JWT_AUTH_HTTPONLY' : False,
    'LOGIN_SERIALIZER' : 'org.serializers.LoginSerializer',
    'REGISTER_SERIALIZER': 'org.serializers.RegisterSerializer',
    'PASSWORD_RESET_SERIALIZER': 'org.serializers.PasswordResetSerializer',
    'USER_DETAILS_SERIALIZER': 'org.serializers.UserSerializer',
    'PASSWORD_RESET_USE_SITES_DOMAIN': False,
}

ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = env.str('ACCOUNT_EMAIL_VERIFICATION', default='mandatory') 

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


LANGUAGE_CODE = "fr"
TIME_ZONE = "Europe/Paris"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "static"
MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_USER_MODEL = 'org.User'

CLIENT_MODE = env.bool('CLIENT_MODE', default=False)

MQTT_BROKER = env.str('MQTT_BROKER', default=None)