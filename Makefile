all: ./cgi/ip ./cgi/cipher ./cgi/dns
clean: clean-ip clean-cipher clean-dns
scp: all scp-all
install: scp apply
scp-html: ./html/index.html ./html/index.js ./html/index.css ./html/manifest.json ./html/icon-1024.png ./html/icon-192.png ./html/sw.js
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
	cp ip.py ./cgi/

clean-ip:
	rm ./cgi/ip
	rm ./cgi/ip.py

scp-ip:
	scp ./cgi/ip httpwn.org:/var/www/cgi/

./cgi/cipher:
	gcc cipher.c -Ofast -o ./cgi/cipher
	cp cipher.py ./cgi/

clean-cipher:
	rm ./cgi/cipher
	rm ./cgi/cipher.py

scp-cipher:
	scp ./cgi/cipher httpwn.org:/var/www/cgi/

./cgi/dns:
	gcc uuid4.c dns.c -Ofast -o ./cgi/dns
	cp dns.py ./cgi/

clean-dns:
	rm ./cgi/dns
	rm ./cgi/dns.py

scp-dns:
	scp ./cgi/dns httpwn.org:/var/www/cgi/

scp-html:
	scp ./html/index.html ./html/index.js ./html/index.css ./html/manifest.json ./html/sw.js ./html/icon-1024.png ./html/icon-192.png httpwn.org:/var/www/html/

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

