#!/usr/bin/env bash
certbot certonly --register-unsafely-without-email --agree-tos --manual --manual-auth-hook /var/www/certbot-validation.sh --manual-cleanup-hook /var/www/certbot-validation-post.sh --preferred-challenges dns -d in-addr.httpwn.org -d *.in-addr.httpwn.org
