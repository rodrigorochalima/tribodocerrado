FROM php:8.1-apache

# Instalar dependências e extensões PHP
RUN apt-get update && apt-get install -y \
    unzip git curl \
    libzip-dev libpng-dev libjpeg-dev libonig-dev \
    libpq-dev libldap2-dev libicu-dev libfreetype6-dev \
    && docker-php-ext-configure gd --with-freetype --with-jpeg \
    && docker-php-ext-install -j$(nproc) \
        pdo pdo_pgsql pgsql zip gd intl bcmath ldap mbstring \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Instalar Composer
COPY --from=composer:latest /usr/bin/composer /usr/bin/composer

# Configurar Apache - habilitar módulos necessários
RUN a2enmod rewrite headers expires
COPY docker/apache-vhost.conf /etc/apache2/sites-available/000-default.conf

# Copiar aplicação e instalar dependências
WORKDIR /var/www/html
COPY . .
RUN composer install --no-dev --optimize-autoloader --ignore-platform-reqs

# Configurar permissões
RUN chown -R www-data:www-data /var/www/html \
    && chmod -R 755 /var/www/html \
    && mkdir -p uploads protected/runtime assets \
    && chmod -R 777 uploads protected/runtime assets \
    && chmod +x docker/start.sh

EXPOSE 80
CMD ["docker/start.sh"]


# Corrige aviso do Apache
RUN echo "ServerName localhost" >> /etc/apache2/apache2.conf
