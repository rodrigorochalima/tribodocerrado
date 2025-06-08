#!/bin/bash
a2enmod rewrite
service apache2 start
apache2ctl -D FOREGROUND
