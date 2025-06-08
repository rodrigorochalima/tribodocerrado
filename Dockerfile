
FROM php:8.1-apache

# Instala dependências
RUN apt-get update && apt-get install -y \
    libzip-dev \
    unzip \
    git \
    libpng-dev \
    libjpeg-dev \
    libfreetype6-dev \
    libonig-dev \
    libxml2-dev \
    zip \
    libicu-dev \
    libpq-dev \
    libldap2-dev \
    && docker-php-ext-configure gd --with-jpeg \
    && docker-php-ext-install gd intl pdo pdo_pgsql zip exif bcmath ldap

# Habilita módulos Apache
RUN a2enmod rewrite headers ssl

# Ajusta configurações PHP
RUN echo "memory_limit = 512M" >> /usr/local/etc/php/conf.d/docker-php-memlimit.ini
RUN echo "upload_max_filesize = 50M" >> /usr/local/etc/php/conf.d/docker-php-uploads.ini
RUN echo "post_max_size = 50M" >> /usr/local/etc/php/conf.d/docker-php-uploads.ini
RUN echo "max_execution_time = 300" >> /usr/local/etc/php/conf.d/docker-php-time.ini

# Configuração do ambiente da aplicação
WORKDIR /var/www/html
COPY . .

# Corrige permissões
RUN chmod -R 777 /var/www/html/uploads || true
RUN chown -R www-data:www-data /var/www/html

COPY docker/apache-vhost.conf /etc/apache2/sites-available/000-default.conf
COPY docker/start.sh /start.sh
RUN chmod +x /start.sh

CMD ["/start.sh"]
