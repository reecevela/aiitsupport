workers = 4
bind = "unix:/var/www/aiitsupport/aiitsupport.sock"
accesslog = "/var/log/gunicorn/access.log"
errorlog = "/var/log/gunicorn/error.log"
