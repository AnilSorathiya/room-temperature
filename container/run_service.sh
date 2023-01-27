#!/usr/bin/env bash
ulimit -n 800
sysctl -w net.core.somaxconn=4096
uwsgi --ini wsgi.ini --listen 4096
