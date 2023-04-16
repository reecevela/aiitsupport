workers = 3
bind = "unix:/var/www/aiitsupport/chatbot/chatbot.sock"
accesslog = "/var/log/gunicorn/access.log"
errorlog = "/var/log/gunicorn/error.log"
