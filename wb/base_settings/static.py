from wb.base_settings.base_dir import BASE_DIR

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR.joinpath('static'),
]
STATIC_ROOT = ''
