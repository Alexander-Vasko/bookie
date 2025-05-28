import os
from pathlib import Path

# Путь к проекту
BASE_DIR = Path(__file__).resolve().parent.parent

# База данных (на примере SQLite)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Язык и часовой пояс
LANGUAGE_CODE = 'ru'
TIME_ZONE = 'Europe/Moscow'
USE_I18N = True
USE_TZ = True

# Приложения
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'shop',  # Твоё приложение
]

# Настройки шаблонов
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'bookie' / 'templates'],  # <-- Путь к папке с шаблонами
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


# Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',  # Добавленное middleware
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # Добавленное middleware
    'django.contrib.messages.middleware.MessageMiddleware',  # Добавленное middleware
    'django.middleware.clickjacking.XFrameOptionsMiddleware',  # Заменить XContentOptionsMiddleware на XFrameOptionsMiddleware
]


# Статические файлы и другие параметры
STATIC_URL = '/static/'

# Прочие настройки
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Безопасность
# Разрешённые хосты (например, для разработки можно использовать `'*'`, но для продакшн лучше указать конкретные домены)
ALLOWED_HOSTS = ['*']  # Для разработки. Для продакшн указывай конкретные хосты.

# Режим отладки
DEBUG = True  # Установи в False на продакшн сервере

ROOT_URLCONF = 'bookie.urls'

SECRET_KEY = 'django-insecure-4^1#z+9&os8!y&34@7m()u%wxw3z53c*m7!z-5u_0bz-66y'
