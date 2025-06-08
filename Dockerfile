
FROM php:8.1-apache

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    libpq-dev \
    libzip-dev \
    libldap2-dev \
    libjpeg-dev \
    libpng-dev \
    unzip \
    git \
    curl \
    libonig-dev \
    && docker-php-ext-configure gd \
    --with-jpeg \
    && docker-php-ext-install \
    pdo_pgsql \
    zip \
    gd \
    exif \
    intl \
    bcmath \
    ldap

# Instalar Composer
COPY --from=composer:latest /usr/bin/composer /usr/bin/composer

# Habilitar módulos do Apache
RUN a2enmod rewrite
RUN a2enmod headers
RUN a2enmod ssl

# Configurações PHP
RUN echo "memory_limit = 512M" >> /usr/local/etc/php/conf.d/docker-php-memlimit.ini
RUN echo "upload_max_filesize = 50M" >> /usr/local/etc/php/conf.d/docker-php-uploads.ini
RUN echo "post_max_size = 50M" >> /usr/local/etc/php/conf.d/docker-php-uploads.ini
RUN echo "max_execution_time = 300" >> /usr/local/etc/php/conf.d/docker-php-time.ini

# Diretório de trabalho
WORKDIR /var/www/html

# Copiar aplicação
COPY . .

# Instalar dependências PHP via Composer
RUN composer install --no-dev --optimize-autoloader --no-interaction

# Permissões
RUN chmod -R 777 /var/www/html/uploads
RUN chown -R www-data:www-data /var/www/html

# Script de inicialização
COPY docker/start.sh /start.sh
RUN chmod +x /start.sh

# Configuração do Apache
COPY docker/apache-vhost.conf /etc/apache2/sites-available/000-default.conf

# Expor porta
EXPOSE 80

CMD ["/start.sh"]
