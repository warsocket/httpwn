all: ip cipher dns
clean: clean-ip clean-cipher clean-dns
scp: scp-ip scp-cipher scp-dns

ip:
	gcc ip.c -Ofast -o ./cgi/ip
	cp ip.py ./cgi/
clean-ip:
	rm ./cgi/ip
	rm ./cgi/ip.py
scp-ip:
	scp ./cgi/ip httpwn.org:/var/www/cgi/

cipher:
	gcc cipher.c -Ofast -o ./cgi/cipher
	cp cipher.py ./cgi/
clean-cipher:
	rm ./cgi/cipher
	rm ./cgi/cipher.py
scp-cipher:
	scp ./cgi/cipher httpwn.org:/var/www/cgi/

dns:
	gcc uuid4.c dns.c -Ofast -o ./cgi/dns
	cp dns.py ./cgi/
clean-dns:
	rm ./cgi/dns
	rm ./cgi/dns.py
scp-dns:
	scp ./cgi/dns httpwn.org:/var/www/cgi/