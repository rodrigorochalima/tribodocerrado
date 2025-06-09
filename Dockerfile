FROM php:8.1-apache

# Instalar extensões PHP necessárias
RUN apt-get update && apt-get install -y \
    unzip \
    git \
    curl \
    libzip-dev \
    libpng-dev \
    libjpeg-dev \
    libonig-dev \
    libpq-dev \
    libldap2-dev \
    libicu-dev \
    libfreetype6-dev \
    && docker-php-ext-configure gd --with-freetype --with-jpeg \
    && docker-php-ext-install -j$(nproc) \
        pdo \
        pdo_pgsql \
        pgsql \
        zip \
        gd \
        intl \
        bcmath \
        ldap \
        mbstring \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Configurar Apache
RUN a2enmod rewrite headers ssl
COPY docker/apache-vhost.conf /etc/apache2/sites-available/000-default.conf

# Copiar aplicação
WORKDIR /var/www/html
COPY . .

# Instalar dependências PHP
RUN composer install --no-dev --optimize-autoloader --no-scripts --ignore-platform-reqs

# Configurar permissões
RUN chown -R www-data:www-data /var/www/html \
    && chmod -R 755 /var/www/html \
    && chmod -R 777 /var/www/html/uploads \
    && chmod -R 777 /var/www/html/protected/runtime \
    && chmod -R 777 /var/www/html/assets \
    && chmod +x /var/www/html/docker/start.sh

EXPOSE 80
CMD ["/var/www/html/docker/start.sh"]

