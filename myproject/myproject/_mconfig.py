# from .gen_key import SECRET_KEY
# "в комплекте" идет файл key_gen_(b2_72).py который может сгенерировать как Ключ и файл с ним (gen_key.py)


config = {
    # 'SECRET_KEY': SECRET_KEY,  # import from gen_key.py
    'SECRET_KEY': '...',
    'ACCOUNT_EMAIL_VERIFICATION': 'mandatory',  # 'none'
    # 'EMAIL_BACKEND': 'django.core.mail.backends.smtp.EmailBackend',  # значение по умолчанию (реальная отправка писем)
    'EMAIL_BACKEND': 'django.core.mail.backends.console.EmailBackend',  # вывод отправляемого в консоль (Terminal)
    'EMAIL_HOST_USER': '_@_.ru',
    'EMAIL_HOST_PASSWORD': '...',
    'EMAIL_USE_TLS': False,
    'EMAIL_USE_SSL': True,
    'DEFAULT_FROM_EMAIL': '_@_.ru',
    'SERVER_EMAIL': '_@_.ru',
    'MANAGERS': ('_@_.ru',),
    'ADMINS': ('_@_.ru',),
    'ctrl_mail': '_@_.ru',
    # и всё остальное
}
