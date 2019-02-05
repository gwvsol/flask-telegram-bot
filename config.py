class Config(object):
    API_TOKEN = '742304158:AAFeunhPvTtDs7D4bJ8OG1XU3iJPVNyBbTY'
    WEBHOOK_HOST = 'srv00.hldns.ru'
    WEBHOOK_PORT = 8443                    # 443, 80, 88 or 8443 (port need to be 'open')
    WEBHOOK_LISTEN = '0.0.0.0'
    WEBHOOK_SSL_CERT = 'webhook_cert.pem'  # Path to the ssl certificate
    WEBHOOK_SSL_PRIV = 'webhook_pkey.pem'  # Path to the ssl private key
