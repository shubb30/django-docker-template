import multiprocessing
import gevent

bind = ":5000"
workers = multiprocessing.cpu_count()*2+1
debug = False
proc_name = 'myapp.proc'
pidfile = '/var/log/gunicorn/gunicorn.log'
loglevel = 'debug'
worker_class = 'gevent'
daemon = False