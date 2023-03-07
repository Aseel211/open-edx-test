# -*- coding: utf-8 -*-
import os
from cms.envs.devstack import *

LMS_BASE = "local.overhang.io:8000"
LMS_ROOT_URL = "http://" + LMS_BASE

# Authentication
SOCIAL_AUTH_EDX_OAUTH2_KEY = "cms-sso-dev"
SOCIAL_AUTH_EDX_OAUTH2_PUBLIC_URL_ROOT = LMS_ROOT_URL

FEATURES["PREVIEW_LMS_BASE"] = "preview.local.overhang.io:8000"

####### Settings common to LMS and CMS
import json
import os

from xmodule.modulestore.modulestore_settings import update_module_store_settings

# Mongodb connection parameters: simply modify `mongodb_parameters` to affect all connections to MongoDb.
mongodb_parameters = {
    "db": "openedx",
    "host": "mongodb",
    "port": 27017,
    "user": None,
    "password": None,
    # Connection/Authentication
    "ssl": False,
    "authSource": "admin",
    "replicaSet": None,
    
}
DOC_STORE_CONFIG = mongodb_parameters
CONTENTSTORE = {
    "ENGINE": "xmodule.contentstore.mongo.MongoContentStore",
    "ADDITIONAL_OPTIONS": {},
    "DOC_STORE_CONFIG": DOC_STORE_CONFIG
}
# Load module store settings from config files
update_module_store_settings(MODULESTORE, doc_store_settings=DOC_STORE_CONFIG)
DATA_DIR = "/openedx/data/modulestore"

for store in MODULESTORE["default"]["OPTIONS"]["stores"]:
   store["OPTIONS"]["fs_root"] = DATA_DIR

# Behave like memcache when it comes to connection errors
DJANGO_REDIS_IGNORE_EXCEPTIONS = True

# Elasticsearch connection parameters
ELASTIC_SEARCH_CONFIG = [{
  
  "host": "elasticsearch",
  "port": 9200,
}]

# Common cache config
CACHES = {
    "default": {
        "KEY_PREFIX": "default",
        "VERSION": "1",
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://@redis:6379/1",
    },
    "general": {
        "KEY_PREFIX": "general",
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://@redis:6379/1",
    },
    "mongo_metadata_inheritance": {
        "KEY_PREFIX": "mongo_metadata_inheritance",
        "TIMEOUT": 300,
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://@redis:6379/1",
    },
    "configuration": {
        "KEY_PREFIX": "configuration",
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://@redis:6379/1",
    },
    "celery": {
        "KEY_PREFIX": "celery",
        "TIMEOUT": 7200,
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://@redis:6379/1",
    },
    "course_structure_cache": {
        "KEY_PREFIX": "course_structure",
        "TIMEOUT": 7200,
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://@redis:6379/1",
    },
}

# The default Django contrib site is the one associated to the LMS domain name. 1 is
# usually "example.com", so it's the next available integer.
SITE_ID = 2

# Contact addresses
CONTACT_MAILING_ADDRESS = "My Open edX - http://local.overhang.io"
DEFAULT_FROM_EMAIL = ENV_TOKENS.get("DEFAULT_FROM_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
DEFAULT_FEEDBACK_EMAIL = ENV_TOKENS.get("DEFAULT_FEEDBACK_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
SERVER_EMAIL = ENV_TOKENS.get("SERVER_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
TECH_SUPPORT_EMAIL = ENV_TOKENS.get("TECH_SUPPORT_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
CONTACT_EMAIL = ENV_TOKENS.get("CONTACT_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
BUGS_EMAIL = ENV_TOKENS.get("BUGS_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
UNIVERSITY_EMAIL = ENV_TOKENS.get("UNIVERSITY_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
PRESS_EMAIL = ENV_TOKENS.get("PRESS_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
PAYMENT_SUPPORT_EMAIL = ENV_TOKENS.get("PAYMENT_SUPPORT_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
BULK_EMAIL_DEFAULT_FROM_EMAIL = ENV_TOKENS.get("BULK_EMAIL_DEFAULT_FROM_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
API_ACCESS_MANAGER_EMAIL = ENV_TOKENS.get("API_ACCESS_MANAGER_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
API_ACCESS_FROM_EMAIL = ENV_TOKENS.get("API_ACCESS_FROM_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])

# Get rid completely of coursewarehistoryextended, as we do not use the CSMH database
INSTALLED_APPS.remove("lms.djangoapps.coursewarehistoryextended")
DATABASE_ROUTERS.remove(
    "openedx.core.lib.django_courseware_routers.StudentModuleHistoryExtendedRouter"
)

# Set uploaded media file path
MEDIA_ROOT = "/openedx/media/"

# Video settings
VIDEO_IMAGE_SETTINGS["STORAGE_KWARGS"]["location"] = MEDIA_ROOT
VIDEO_TRANSCRIPTS_SETTINGS["STORAGE_KWARGS"]["location"] = MEDIA_ROOT

GRADES_DOWNLOAD = {
    "STORAGE_TYPE": "",
    "STORAGE_KWARGS": {
        "base_url": "/media/grades/",
        "location": "/openedx/media/grades",
    },
}

ORA2_FILEUPLOAD_BACKEND = "filesystem"
ORA2_FILEUPLOAD_ROOT = "/openedx/data/ora2"
ORA2_FILEUPLOAD_CACHE_NAME = "ora2-storage"

# Change syslog-based loggers which don't work inside docker containers
LOGGING["handlers"]["local"] = {
    "class": "logging.handlers.WatchedFileHandler",
    "filename": os.path.join(LOG_DIR, "all.log"),
    "formatter": "standard",
}
LOGGING["handlers"]["tracking"] = {
    "level": "DEBUG",
    "class": "logging.handlers.WatchedFileHandler",
    "filename": os.path.join(LOG_DIR, "tracking.log"),
    "formatter": "standard",
}
LOGGING["loggers"]["tracking"]["handlers"] = ["console", "local", "tracking"]
# Silence some loggers (note: we must attempt to get rid of these when upgrading from one release to the next)

import warnings
from django.utils.deprecation import RemovedInDjango40Warning, RemovedInDjango41Warning
warnings.filterwarnings("ignore", category=RemovedInDjango40Warning)
warnings.filterwarnings("ignore", category=RemovedInDjango41Warning)
warnings.filterwarnings("ignore", category=DeprecationWarning, module="lms.djangoapps.course_wiki.plugins.markdownedx.wiki_plugin")
warnings.filterwarnings("ignore", category=DeprecationWarning, module="wiki.plugins.links.wiki_plugin")

# Email
EMAIL_USE_SSL = False
# Forward all emails from edX's Automated Communication Engine (ACE) to django.
ACE_ENABLED_CHANNELS = ["django_email"]
ACE_CHANNEL_DEFAULT_EMAIL = "django_email"
ACE_CHANNEL_TRANSACTIONAL_EMAIL = "django_email"
EMAIL_FILE_PATH = "/tmp/openedx/emails"

# Language/locales
LOCALE_PATHS.append("/openedx/locale/contrib/locale")
LOCALE_PATHS.append("/openedx/locale/user/locale")
LANGUAGE_COOKIE_NAME = "openedx-language-preference"

# Allow the platform to include itself in an iframe
X_FRAME_OPTIONS = "SAMEORIGIN"


JWT_AUTH["JWT_ISSUER"] = "http://local.overhang.io/oauth2"
JWT_AUTH["JWT_AUDIENCE"] = "openedx"
JWT_AUTH["JWT_SECRET_KEY"] = "dzldWmDiyxY5I6D8fNlGbzvP"
JWT_AUTH["JWT_PRIVATE_SIGNING_JWK"] = json.dumps(
    {
        "kid": "openedx",
        "kty": "RSA",
        "e": "AQAB",
        "d": "EEzoAnY_RvZG4fKqh_E8bwinmH1ti7CA92lcwAwdsG1GtEwE2s4MupROEgCirkOGogyizr-bPGjNngKyhHCeiQXU62dp8rSlIDblsvnA7kb-rw3wJAAgqPiyiAqtgtUZhRi4_h7J0B9WzyyW6HyYo29rGPlihaxFFP_sQywVQH2XzERrlDFdYcfcV6G9DHR0x2-u83TlP9Jys4386waiDsWSHaO-9_PKkEE7uH-pl6Gsv87uBOFbsDQSciBvVL4E3dHe2fs1xqu_KmTY33hUldMYNMLlmzC3k7DrawGmybEGYIPdqU7msT4RSdLLj_QYNM97lUasdR-zY4UgyMIQVQ",
        "n": "52E3W1X79sViNaXeiyjirvDl1j_gkWKtUs0NjUWuvpH_-fDfDfeoNNfWNbZLA7n24hLJ56BMExN2pZU844H3jVr8WoInfC3mpx6L8RwbSCH8rQepnBlSEUOQCZqeG8HrKaeC2MlheKljOT5h-sKuqR4GyUzgnrvlrXB2KdOOCEKuDnLCGUtwLx9kpOuG9DP-GDY_RC9XV86CU3_55c4fic4Wl3IHUKPbDJUKsESxOhzuDrlNo1yTqP7xqVVCwBagQWe_bvXQKF32fhV0cFGR0PZ27v5VFctrrjDa1Tmlik2YIk3Oe8M2Ao9c4aQ2Uol33nh76C3_YKAQbWQpc96SWQ",
        "p": "8LnV6g8EU4mj9ltxh38keC3Ph4vZX3veuQURcoMc3Wa9_LJ8CtnBmQUl3WG4NOot2KPfGRiTl04p9TYDOvSRJeZySe068Z6r3kA4tf84TX8IS6mNyWoyaFmFjdh17PNpJTziYQda877c7na1Vi6dcuR4KzuMh7zHa__euWCPHGc",
        "q": "9g-RmL2nHVvyFMSQo1lA6eSb7PERHndRETiogB8EJbm709pSmtankO2NOxKWyzKINTejC3dbjonA7wVuOkwx8MyyG9tUTijpRha3Pyw40DRzPaHdUA9GIdwLN-vnm1mFy-oegy4uCghv663acxbpLsoASxZo7Qh5aTKpvSdHoz8",
    }
)
JWT_AUTH["JWT_PUBLIC_SIGNING_JWK_SET"] = json.dumps(
    {
        "keys": [
            {
                "kid": "openedx",
                "kty": "RSA",
                "e": "AQAB",
                "n": "52E3W1X79sViNaXeiyjirvDl1j_gkWKtUs0NjUWuvpH_-fDfDfeoNNfWNbZLA7n24hLJ56BMExN2pZU844H3jVr8WoInfC3mpx6L8RwbSCH8rQepnBlSEUOQCZqeG8HrKaeC2MlheKljOT5h-sKuqR4GyUzgnrvlrXB2KdOOCEKuDnLCGUtwLx9kpOuG9DP-GDY_RC9XV86CU3_55c4fic4Wl3IHUKPbDJUKsESxOhzuDrlNo1yTqP7xqVVCwBagQWe_bvXQKF32fhV0cFGR0PZ27v5VFctrrjDa1Tmlik2YIk3Oe8M2Ao9c4aQ2Uol33nh76C3_YKAQbWQpc96SWQ",
            }
        ]
    }
)
JWT_AUTH["JWT_ISSUERS"] = [
    {
        "ISSUER": "http://local.overhang.io/oauth2",
        "AUDIENCE": "openedx",
        "SECRET_KEY": "dzldWmDiyxY5I6D8fNlGbzvP"
    }
]

# Enable/Disable some features globally
FEATURES["ENABLE_DISCUSSION_SERVICE"] = False
FEATURES["PREVENT_CONCURRENT_LOGINS"] = False
FEATURES["ENABLE_CORS_HEADERS"] = True

# CORS
CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_ALLOW_ALL = False
CORS_ALLOW_INSECURE = True
CORS_ALLOW_HEADERS = corsheaders_default_headers + ('use-jwt-cookie',)

# Add your MFE and third-party app domains here
CORS_ORIGIN_WHITELIST = []

# Disable codejail support
# explicitely configuring python is necessary to prevent unsafe calls
import codejail.jail_code
codejail.jail_code.configure("python", "nonexistingpythonbinary", user=None)
# another configuration entry is required to override prod/dev settings
CODE_JAIL = {
    "python_bin": "nonexistingpythonbinary",
    "user": None,
}


######## End of settings common to LMS and CMS

######## Common CMS settings
STUDIO_NAME = "My Open edX - Studio"

CACHES["staticfiles"] = {
    "KEY_PREFIX": "staticfiles_cms",
    "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
    "LOCATION": "staticfiles_cms",
}

# Authentication
SOCIAL_AUTH_EDX_OAUTH2_SECRET = "5reViFIScRmydn94v2o5Afbp"
SOCIAL_AUTH_EDX_OAUTH2_URL_ROOT = "http://lms:8000"
SOCIAL_AUTH_REDIRECT_IS_HTTPS = False  # scheme is correctly included in redirect_uri
SESSION_COOKIE_NAME = "studio_session_id"

MAX_ASSET_UPLOAD_FILE_SIZE_IN_MB = 100

FRONTEND_LOGIN_URL = LMS_ROOT_URL + '/login'
FRONTEND_REGISTER_URL = LMS_ROOT_URL + '/register'

# Create folders if necessary
for folder in [LOG_DIR, MEDIA_ROOT, STATIC_ROOT_BASE]:
    if not os.path.exists(folder):
        os.makedirs(folder)



######## End of common CMS settings

# Setup correct webpack configuration file for development
WEBPACK_CONFIG_PATH = "webpack.dev.config.js"



COURSE_AUTHORING_MICROFRONTEND_URL = "http://apps.local.overhang.io:2001/course-authoring"
CORS_ORIGIN_WHITELIST.append("http://apps.local.overhang.io:2001")
LOGIN_REDIRECT_WHITELIST.append("apps.local.overhang.io:2001")
CSRF_TRUSTED_ORIGINS.append("apps.local.overhang.io:2001")
