FROM shubb30/django-base:1.11.14 as app

WORKDIR /var/www/django/myapp

ADD src /var/www/django/myapp
ADD build/requirements.txt /root
RUN pip install -r /root/requirements.txt

ADD build/entrypoint.sh /
RUN chmod +x /entrypoint.sh
RUN /var/www/django/myapp/manage.py collectstatic --noinput

CMD ["/entrypoint.sh"]

FROM nginx:latest as static
COPY --from=app /opt/www/static/ /usr/share/nginx/html/static