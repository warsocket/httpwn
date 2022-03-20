#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <regex.h>
#include <string.h>
#include <dirent.h>
#include <stdbool.h>
#include "uuid4.h"


const char const UUIDRGX_TXT[] = "^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$";
const char const REDIRRGX_TXT[] = "^[0-9]-[0-9a-z]{16}-[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$";
const char const REGEX_TXT[] = "^abc+$";

regex_t UUIDRGX;
regex_t REDIRRGX;
regex_t REGEX;

const char const alphabet[] = "abcdefghijklmnopqrstuvwxyz0123456789";
char rsi[17] = {'\0'};
// char hostname[256] = {0};

const char* const rs(){

	for (int i = 0 ; i < sizeof(rsi)-1 ; ++i){
		rsi[i] = alphabet[rand() % (sizeof(alphabet)-1)];
	}
	return rsi;
}

void seed(){
	struct timespec ts;
	clock_gettime(CLOCK_REALTIME, &ts);
	srand ( ts.tv_nsec );	
}

const char* const uuid_chop(char string[]){
	for (int i = 0; i < strlen(string); ++i){
		if (string[i] == '.'){
			string[i] = '\0';
			break;
		}
	}
	return string;
}


bool string_in_array(const char string[], const char array[10][50]){

	for (int i = 0; i < 10; ++i){
		if (strcmp(string, array[i]) == 0) return true;
	}
	return false;

}


void main(){
	//main stuff

	//get hostname and its leftmost part (candidate uuid)
	char* hostname = getenv("HTTP_HOST"); //in last case its not const we inc the first char
	char uuid_buff[256];
	const char* const uuid = uuid_chop(strncpy(uuid_buff, hostname, sizeof(uuid_buff)));

	// printf("%s\n", uuid);

	//regex prep
	// int ret;

	regcomp(&UUIDRGX, UUIDRGX_TXT, REG_EXTENDED);
	// printf("%i\n", ret);

	regcomp(&REDIRRGX, REDIRRGX_TXT, REG_EXTENDED);
	// printf("%i\n", ret);


	//output starts here
	// printf("Content-Type: text/plain\r\n\r\n");
	printf("Access-Control-Allow-Origin: *\r\n");
	printf("Content-Type: text/json\r\n");

	if (!strcmp(hostname, "httpwn.org")){
		char uuid4[UUID4_LEN];
		uuid4_init();
		uuid4_generate(uuid4);

		//seeding rng
		seed();
		printf("Status: 302 Found\r\n");
		printf("Location: //0-%s-%s.in-addr.%s/dns\r\n", rs(), uuid4, hostname);
		printf("\r\n");

	}else if(regexec(&UUIDRGX, uuid, 0, NULL, 0) == 0){
		printf("Status: 200 OK\r\n\r\n");

		char dir[4096-256];
		snprintf(dir, sizeof(dir), "/ramdisk/%s/", uuid);

		// printf("%s\n", dir);

		struct dirent *de;
		DIR *dr = opendir(dir);
		char ips[10][50];
		for (int i = 0; i < 10; ++i) ips[i][0] = '\0';
 
		if (dr != NULL){

			FILE *fp;
			int i = 0;

			while ((de = readdir(dr)) != NULL){
				if ( (!strcmp(de->d_name, ".") == 0) && (!strcmp(de->d_name, "..") == 0) ){

					char file[4096];
					snprintf(file, sizeof(file), "%s%s", dir, de->d_name);
					// printf("%s", file);

					fp = fopen(file, "r");
					char ip[50] = {0};
					int read = fread(ip, sizeof(char), sizeof(ips[0]), fp);
					ip[sizeof(ip)-1] = '\0';
					fclose(fp);
					// printf("%s",de->d_name);
					if (!string_in_array(ip, ips)) strcpy(ips[i], ip); //safe because we are guaranteed a \0 on char 50

					++i;
					if (i >= 10) break; //only do 10 files (which is exacly haow many you get after 1 unique run)
				}
			}
		}

		closedir(dr);

		printf("[");
		bool first = true;
		for (int i = 0; i < 10; ++i){

			if (ips[i][0] == '\0') continue; //skip the empty string entries
			if (!first) printf(", ");
			printf("\"%s\"", ips[i]);
			first = false;
		}
		printf("]");


	}else if(regexec(&REDIRRGX, uuid, 0, NULL, 0) == 0){
		printf("Status: 302 Found\r\n");

		if (hostname[0] < '9'){
			hostname[0] += 1;
			printf("Location: //%s/dns\r\n\r\n", hostname);
		}else{
			hostname += 19;
			printf("Location: //%s/dns\r\n\r\n", hostname);
		}


	}else{
		printf("Status: 400 Bad Request\r\n\r\n");
	}
}