#coding=utf-8

from flask import Flask

from sae.const import (MYSQL_HOST, MYSQL_HOST_S, MYSQL_PORT,
                           MYSQL_USER, MYSQL_PASS, MYSQL_DB
                      )


app = Flask(__name__)
app.debug = True
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://%s:%s@%s:%s/%s" % (MYSQL_USER, MYSQL_PASS, MYSQL_HOST, MYSQL_PORT, MYSQL_DB)

from . import views
