#include <stdio.h>
#include <stdlib.h>

void main(){
	printf("Content-Type: text/plain\r\n\r\n");
	if (getenv("HTTPS")){
		printf("%s (%s)", getenv("SSL_PROTOCOL"), getenv("SSL_CIPHER"));
	}
}