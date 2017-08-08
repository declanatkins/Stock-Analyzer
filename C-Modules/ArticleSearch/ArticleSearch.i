/*Interface file for ArticleSearch.c*/
%module ArticleSearch
%{
char** search_for_links(char** html_text);
char* clean_link_string(char* link);
int check_for_keywords(char** text, char** keyword_list);
%}

char** search_for_links(char** html_text);
char* clean_link_string(char* link);
int check_for_keywords(char** text, char** keyword_list);