class Config(object):
    DOMAIN              = {'Cnt':1, 'Cmp':1, 'Prs':1, 'Usr':1}
    DEBUG               = False

    DEFAULT_MAIL_SENDER = ("mail manager", "mail@manager.com")
    SECRET_KEY          = 'a[U\\^U;N_OGX5WG+9F\:ba[U\\^yA|Nx|xf6"^'

    TESTING_HOST        = 'localhost:5000'

    MONGO_HOST          = 'localhost'
    MONGO_DBNAME        = 'gsapi-test'
    MONGO_TEST_DBNAME   = 'gsapi-test'

    #WTForms Settings
    CSRF_ENABLED        = True
    CSRF_SESSION_KEY    = '_csrf_token'

    #Flask Mail settings
    MAIL_SERVER         = 'localhost'
    MAIL_PORT           =  25
    MAIL_USE_TLS        = False
    MAIL_USE_SSL        = False
    MAIL_DEBUG          = DEBUG
    MAIL_USERNAME       = None
    MAIL_PASSWORD       = None
    DEFAULT_MAIL_SENDER = None


    # fabric settings
    FABRIC = {
        'live': {
            'HOSTS': ['50.116.35.54:22'],
            'WEB_USER': 'root',
            'ADMIN_USER': 'root',
            'ADMIN_PW': 'Stop&Think',
            'PROJECT_ROOT': '/srv/gs/api/gsapi'
        }
    }