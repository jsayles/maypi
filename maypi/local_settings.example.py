ADMINS = (
    ('SYSTEMS PERSON', 'systems@yourdomain.com'),
)
DEBUG = True
TEMPLATE_DEBUG = True
SECRET_KEY = 'yoursecretkeyissecret'

STATIC_ROOT = '/home/maypi/webapp/static/'
MEDIA_ROOT = '/home/maypi/webapp/media/'

# These are used to connect modernomad and maypi
MAYPI_API_KEY = 'anothersecretkey'
MAYPI_MASTER_URL = "http://localhost:8000/api/"

LOGGING = {
		'version': 1,
		'disable_existing_loggers': False,
		'formatters': {
				'verbose': {
						'format' : "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
						'datefmt' : "%d/%b/%Y %H:%M:%S"
				  },
				  'simple': {
								'format': '%(levelname)s %(message)s'
				  },
		 },
		'handlers': {
				'file': {
						'level': 'DEBUG',
						'class': 'logging.FileHandler',
						#'filename': 'django.log',
						'filename': '/home/maypi/logs/django.log'
						'formatter': 'verbose',
				},
				'mail_admins': {
						'level': 'ERROR',
						'class': 'django.utils.log.AdminEmailHandler',
						'include_html': True,
						'formatter': 'verbose',
				},
				'console':{
					'level': 'DEBUG',
					'class': 'logging.StreamHandler',
					'formatter': 'simple'
				},
		},
		'loggers': {
				'django': {
						'handlers': ['file', 'console'],
						'level': 'INFO',
						'propagate': True,
				},
				'django.request': {
						'handlers': ['file', 'mail_admins'],
						'level': 'INFO',
						'propagate': True,
				},
				'maypi': {
						'handlers': ['file', 'console'],
						'level': 'DEBUG',
				},
		},
}