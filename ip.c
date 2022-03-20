#include <stdio.h>
#include <stdlib.h>

void main(){
	
	if (getenv("HTTPS")){
		printf("Access-Control-Allow-Origin: https://httpwn.org\r\n");
	}else{
		printf("Access-Control-Allow-Origin: http://httpwn.org\r\n");
	}

	printf("Content-Type: text/plain\r\n\r\n");
	printf("%s\n", getenv("REMOTE_ADDR"));
}