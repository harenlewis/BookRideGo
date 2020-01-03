FROM python36-mod-wsgi:latest
 
ARG env_JOBNAME
ARG env_repository_name
ARG env_project_name
ARG env_app_name
ARG env_project_id
 
ENV JOBNAME=$env_JOBNAME repository_name=$env_repository_name project_name=$env_project_name app_name=$env_app_name project_id=$env_project_id
COPY ${JOBNAME}.zip /root/${project_name}.zip
 
RUN cd && \
   echo ${project_name} && \
   echo ${app_name} && \
   mkdir -p /var/.ao && \
   pwd && \
   ls && \
   unzip ${project_name}.zip && \
   ls && \
   pip3 install -r requirements.txt && \
   cp -r ${project_name} /var/www/ && \
   ls -la /var/www && \
   rm -rf /root/${repository_name} /root/${project_name}.zip


# Installing the package
RUN apk add --update \
 python \
 curl \
 which \
 bash
WORKDIR /usr
RUN apk --no-cache add shadow && \
  usermod -aG apache root && \
  chown -R apache:apache /root
 
RUN echo -e "import os\n\
import sys\n\
path='/var/www/${project_name}'\n\
if path not in sys.path:\n\
    sys.path.append(path)\n\
os.environ['DJANGO_SETTINGS_MODULE'] = '${project_name}.settings'\n\
from django.core.wsgi import get_wsgi_application\n\
application = get_wsgi_application()" >> /var/www/${project_name}/django.wsgi;\
sed -i -r 's@#(LoadModule rewrite_module modules/mod_rewrite.so)@\1@i' /etc/apache2/httpd.conf;\
sed -i -r 's@Errorlog .*@Errorlog /var/log/apache2/error.log@i' /etc/apache2/httpd.conf;\
sed -i -r 's@#Servername .*@ServerName localhost@i' /etc/apache2/httpd.conf;\
sed -i -r 's@Listen 80.*@Listen 80@i' /etc/apache2/httpd.conf;\
sed -i "s@DocumentRoot \"/var/www/localhost/htdocs\".*@DocumentRoot \"/var/www/${project_name}\"@i" /etc/apache2/httpd.conf;\
sed -i "s@Timeout 300@Timeout 3600@" /etc/apache2/httpd.conf;\
sed -i "s@KeepAliveTimeout 5@KeepAliveTimeout 65@" /etc/apache2/httpd.conf;\
sed -i "s@Group apache@Group root@" /etc/apache2/httpd.conf
 
RUN echo -e "Transferlog /dev/stdout\n\
LoadModule wsgi_module modules/mod_wsgi.so\n\
WSGIPythonPath /usr/lib/python3.6\n\
WSGIScriptAlias / /var/www/${project_name}/django.wsgi\n\
WSGIApplicationGroup %{GLOBAL}\n\
<Directory /var/www/${project_name}>\n\
    Options ExecCGI Indexes FollowSymLinks\n\
    AllowOverride All\n\
    Require all granted\n\
    <Files django.wsgi>\n\
       Require all granted\n\
    </Files>\n\
</Directory>" >> /etc/apache2/httpd.conf
 
 
EXPOSE 80
CMD ["httpd-foreground"]

