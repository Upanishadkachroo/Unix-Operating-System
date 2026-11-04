
FROM php:8.2-apache

# Install PHP extensions required for MySQL connectivity.
RUN docker-php-ext-install pdo pdo_mysql

# Copy the application into Apache's document root.
COPY app/ /var/www/html/

# Apache listens on port 80.
EXPOSE 80
