#!/usr/bin/env bash
# script that sets up your web servers for the deployment of web_static.

if [[ "$(which nginx | grep -c nginx)" == '0' ]]; then
        apt-get update
        apt-get -y install nginx
fi

# Create config file
SERVER_CONFIG='
server {
        listen 80 default_server;
        listen [::]:80 default_server;

        server_name _;
        index index.html index.htm;
        error_page 404 /404.html;
        add_header X-Served-By $hostname;

        location / {
                root /var/www/html/;
                try_files $uri $uri/ =404;
        }

        location /hbnb_static/ {
                alias /data/web_static/current/;
                try_files $uri $uri/ =404;
        }

        if ($request_filename ~ redirect_me) {
                rewrite ^ https://sketchfab.com/bluepeno/models permanent;
        }

        location = /404.html {
                root /var/www/error/;
                internal;
        }
}'
# Fake HTML file to test nginx config
HOME_PAGE='<!DOCTYPE html>
<html lang="en-US">
        <head>
                <title>Home - AirBnB Clone</title>
        </head>
        <body>
                <h1> Welcome to AirBnB By Holberton</h1>
        </body>
</html>'

mkdir -p /var/www/html /var/www/error
chmod -R 755 /var/www
echo 'Hello World!' > /var/www/html/index.html
echo -e "Ceci n'est pas une page" > /var/www/error/404.html

# Create the folder /data/ if it doesn’t already exist
# Create the folder /data/web_static/ if it doesn’t already exist
# Create the folder /data/web_static/releases/ if it doesn’t already exist
# Create the folder /data/web_static/releases/test/ if it doesn’t already exist
mkdir -p /data/web_static/releases/test/

# Create the folder /data/web_static/shared/ if it doesn’t already exist
mkdir -p /data/web_static/shared/

# Echo fake HTML here
echo -e "$HOME_PAGE" > /data/web_static/releases/test/index.html
[ -d /data/web_static/current ] && rm -rf /data/web_static/current

# Create symbolic link
ln -sf /data/web_static/releases/test/ /data/web_static/current

# Give ownership of the /data/ folder to the ubuntu user AND group
chown -R ubuntu:ubuntu /data

# Update the Nginx configuration to serve the content of
# /data/web_static/current/ to hbnb_static
echo "$SERVER_CONFIG" > /etc/nginx/sites-available/default
ln -sf /etc/nginx/sites-available/default /etc/nginx/sites-enabled/default

if [ "$(pgrep -c nginx)" -le 0 ]; then
        service nginx start
else
        service nginx restart
        service nginx reload
fi
