FROM php:8.1-apache
RUN apt-get update && apt-get install -y unzip git curl libzip-dev libpng-dev libjpeg-dev libonig-dev libpq-dev libldap2-dev &&     docker-php-ext-install pdo pdo_mysql zip gd intl bcmath ldap &&     docker-php-ext-configure gd --with-jpeg
COPY . /var/www/html
COPY docker/apache-vhost.conf /etc/apache2/sites-available/000-default.conf
COPY docker/start.sh /start.sh
RUN chmod +x /start.sh && chmod -R 777 /var/www/html
CMD ["/start.sh"]
