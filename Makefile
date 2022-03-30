all: ./cgi/ip ./cgi/cipher ./cgi/dns
clean: clean-ip clean-cipher clean-dns
scp: all scp-all
install: scp apply
scp-html: ./html/index.html ./html/index.js ./html/index.css ./html/manifest.json ./html/icon-1024.png ./html/icon-192.png ./html/Shape-Cube-512.png ./html/sw.js
scp-cgi: scp-ip scp-cipher scp-dns
scp-powerdns:
scp-apache:
scp-all: scp-html scp-cgi scp-powerdns scp-apache
mods-apache:
apply-powerdns:
apply-apache:
apply: apply-powerdns apply-apache

./cgi/ip:
	gcc ip.c -Ofast -o ./cgi/ip

clean-ip:
	rm ./cgi/ip

scp-ip:
	scp ./cgi/ip ./ip.py httpwn.org:/var/www/cgi/
	scp ./ip.wsgi httpwn.org:/var/www/wsgi/

./cgi/cipher:
	gcc cipher.c -Ofast -o ./cgi/cipher

clean-cipher:
	rm ./cgi/cipher

scp-cipher:
	scp ./cgi/cipher ./cipher.py  httpwn.org:/var/www/cgi/
	scp ./cipher.wsgi httpwn.org:/var/www/wsgi/

./cgi/dns:
	gcc uuid4.c dns.c -Ofast -o ./cgi/dns

clean-dns:
	rm ./cgi/dns

scp-dns:
	scp ./cgi/dns ./dns.py httpwn.org:/var/www/cgi/
	#scp ./dns.wsgi httpwn.org:/var/www/wsgi/

scp-html:
	scp ./html/index.html ./html/index.js ./html/index.css ./html/manifest.json ./html/sw.js ./html/icon-1024.png ./html/icon-192.png ./html/Shape-Cube-512.png httpwn.org:/var/www/html/

scp-apache:
	scp ./site.conf httpwn.org:/etc/apache2/

apply-apache:
	ssh httpwn.org service apache2 reload

mods-apache:
	ssh httpwn.org a2enmod cgid
	#a2enmod ssl #this should bne done by yourself and already active

scp-powerdns:
	scp dns+certbot/powerdns-pipe.conf httpwn.org:/etc/powerdns/pdns.d/

apply-powerdns:
	ssh httpwn.org service pdns restart

