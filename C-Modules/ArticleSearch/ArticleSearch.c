//Author: Declan Atkins
//Last Changed: 15/08/2017
//Linked with python using SWIG

#include <stdio.h>
#include <string.h>
#include <stdbool.h>
#include <stdlib.h>

//external functions
char* search_for_links(char* html_text);
char* clean_link_string(const char* link);
int check_for_keywords(char* text, char* keyword_list);

//internal functions
char **split_string(char* string);
char *re_concat_strings(char** links_arr)

/*
This function takes in a html file and searches for
the link following a div with class=g (the class given
to links to articles on the google search news results).
*/
char* search_for_links(char* html_text){
/*
Current solution is a bit messy but avoids typemapping char**:

send in the entire block of html text as a string and split it into
an array using a separate function. then concatenate the link strings
separated with a space so that they can be split on the python side
before being sent for cleaning
*/
	
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
char *clean_link_string(char *link){
	
	bool record =false;
	char ret[sizeof(link) +1];
	int len = 0;
	for(;*link;link++){
		char c = *link;
		if(record){
			if (c == '\"'){
				break;//stop recording at the end of the link
			}
			else{
				ret[len] = c;
				len++;
			}
		}
		else{
			if (c == '\"'){
				record = true;//start recording the chars
			}
		}
	}
	ret[len] = '\0';
	
	char *s_ret = (char *) malloc(strlen(ret));
	
	strcpy(s_ret,ret);
	return s_ret;
}

//this function checks a block of text to see if it contains
//any of the keywords contained in the list it takes in
//it returns the number of matches
int check_for_keywords(char* text_string, char* keyword_string){
	
	char** text = split_string(text_string);
	char** keyword_list = split_string(keyword_string);
	int matches=0;
	for(;*text;text++){
		for(;*keyword_list;keyword_list++){
			if(strcmp(*text,*keyword_list)){
				matches++;
			}
		}
	}
	return matches;
}

/*
This function effectively works like the python
str.split() method, splitting the string into an 
array of strings at each space
*/
char **split_string(char* string){
	
	char* buffer;
	char** ret;
	int buff_counter=0;
	int ret_counter=0;
	
	for(;*string;string++){
		
		if(*string == ' '){
			buffer = realloc(buffer, 1);
			buffer[buff_counter] = '\0';
			
			ret = realloc(ret,strlen(buffer) +1);
			strcpy(ret[ret_counter], buffer);
			free(buffer);
			buff_counter = 0;
		}
		else{
			buffer = realloc(buffer, 1);
			buffer[buff_counter] = *string;
			buff_counter++;
		}
	}
	
	return ret;
	
}

/*
This function re concatenates the array of strings into a
single string for easier return to python
*/
char *re_concat_strings(char** links_arr){
	
	char* ret = NULL;
	
	for(;*links_arr;links_arr++){
		
		if(ret == NULL){
			ret = (char*) malloc(strlen(*links_arr) + 1);
			ret = strcpy(ret,*links_arr);
		}
		else{
			ret[strlen(ret)] = ' ';//switch null terminator to a space character
			ret = strcat(ret, *links_arr)
		}
	}
	
	return ret;
}