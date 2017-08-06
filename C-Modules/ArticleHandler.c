//Author: Declan Atkins
//Last Changed: 05/08/2017
//Linked with python using SWIG

#include <stdio.h>
#include <string.h>
#include <stdbool.h>
#include <stdlib.h>


char** search_for_links(char** html_text);
char* clean_link_string(char* link);
/*
This function takes in a html file and searches for
the link following a div with class=g (the class given
to links to articles on the google search news results).
*/
char** search_for_links(char** html_text){
	
	bool next_link = false;
	int links_found = 0;
	char **ret;
	
	
	for(;*html_text;html_text++){
		
		if((strcmp(*html_text,"class=\"g\"") == 0)){
			next_link = true;
		}
		
		if(next_link == true){
			if(*((*(html_text))) == 'h' && *((*(html_text))+1) == 'r' && *((*(html_text))+2) == 'e' && *((*(html_text))+3) == 'f'){
				ret = realloc(ret, strlen(*html_text) + 1);
				ret[links_found++] = *html_text;	
			}
		}
	}
	return ret;
}

//this function cleans the href link and returns just
//the link url
char* clean_link_string(char* link){
	
	bool record =false;
	char* ret = malloc(1);
	int len = 0;
	for(;*link;link++){
		if(record){
			if (*link == '\"'){
				break;//stop recording at the end of the link
			}
			else{
				ret[len++] = *link;
				ret = realloc(ret, 1);
				ret[len] = '\0';
			}
		}
		else{
			if (*link == '\"'){
				record = true;//start recording the chars
			}
		}
	}
	return ret;
}
