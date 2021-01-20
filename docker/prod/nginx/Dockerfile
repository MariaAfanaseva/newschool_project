FROM nginx:latest
RUN rm /etc/nginx/conf.d/default.conf
COPY ./docker/prod/nginx/django_newschool.conf /etc/nginx/conf.d/
#not good idea to copy stataic to nginx
#COPY ./static/ /static/
#RUN chown nginx:nginx -R /static/
