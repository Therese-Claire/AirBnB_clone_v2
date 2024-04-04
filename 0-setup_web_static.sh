#!/usr/bin/env bash
# script that sets up your web servers for the deployment of web_static

if ! command -v nginx >/dev/null 2>&1; then
    apt-get update
    apt-get -y install nginx
fi

mkdir -p /data/web_static/releases/test/
mkdir -p /data/web_static/shared/

echo "<html
<head>
</head>
<body>
    Holberton School
</body>
</html>" > /data/web_static/releases/test/index.html

if [ -e /data/web_static/current ]; then
    rm /data/web_static/current
fi
sudo ln -sfn /data/web_static/releases/test /data/web_static/current

chown -R ubuntu:ubuntu /data/

echo "server {
	listen 80 default_server;
	listen [::]:80 default_server;
	root /var/www/html;
	index index.html index.htm index.nginx-debian.html;

	add_header X-Served-By $HOSTNAME;

	server_name _;

	location / {
		try_files \$uri \$uri/ =404;
	}

	location /hbnb_static {
		alias /data/web_static/current;
		index index.html index.htm;
	}

	location /redirect_me {
		rewrite ^ https://github.com/Therese-Claire permanent;
	}

	error_page 404 /404.html;
	location = /404.html {
		internal;
	}
}" | sudo tee /etc/nginx/sites-available/default >/dev/null

if [ "$(pgrep -c nginx)" -le 0 ]; then
        service nginx restart
else
        service nginx reload
fi
