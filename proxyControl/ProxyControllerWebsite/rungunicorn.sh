#/bin/sh
gunicorn ProxyControllerWebsite.wsgi -b 0.0.0.0:18080
