/*
Author: Declan Atkins
Last Modified: 18/08/17
This module is for all operations relating
to the prediction model. This includes writing 
a days value to the model and updating each of
the neccessary files, as well as returning the 
expected value of a stock price.
*/

#include <stdlib.h>
#include <stdio.h>
#include <math.h>
#include <string.h>
#include <stdbool.h>

//external functions
void add_values(double *values_list,int n_values, char* company, char* set);
double *get_predicted_values(char *company, char* set);
double make_single_prediction_EXTERNAL(char *company, char* set);

//internal functions
double append_to_values(double *values_list,int n_values, char *company);
void update_probabilities(char *company, char* set,double last_val);
double make_single_prediction_INTERNAL(double last_change,double last_val,char* company, char* set);
double get_expected_value(char *filename,double prev_val);
void update_weighting_values(double *values_list,int n_values,char *company, char *set);
char *read_last_line(char *filename); 

struct model_data{
	double change;
	double expected_change;
	int count;
	struct model_data *next;
}model_data;

/*
This function is called from the python side in order
to add the actual values into the model. It returns true
on a successful completion and false if an error occurs
*/
void add_values(double *values_list,int n_values, char *company, char* set){
	
	double last_val;
	update_weighting_values(values_list,n_values,company,set);
	last_val = append_to_values(values_list,n_values,company,set);
	update_probabilities(company,set,last_val);
	
	return;
}

/*
This function returns a prediction for the value of 
the stock price at each minute within the market hours
of the following day
*/
double *get_predicted_values(char* company, char* set){
	
	int i;
	double *ret = (double *) malloc(390 * sizeof(double));
	
	for(i=0;i<390;i++){
		
		if(i == 0){
			ret[i] = make_single_prediction_EXTERNAL(company,set);
		}
		else if(i == 1){
			char fname[100];
			strcpy(fname,"../../");
			strcat(strcat(strcat(fname,company),"/"),"PREVIOUS_VALUES.dat");
			FILE* last_values = fopen(fname, "r");
			double last_val;
			char line[10];
			while(fgets(line,10,last_values)){
				last_val = atof(line);
			}
			
			ret[i] = make_single_prediction_INTERNAL(ret[i-1] - last_val,ret[i-1],company,set);
		}
		else{
			ret[i] = make_single_prediction_INTERNAL(ret[i-1] - ret[i-2],ret[i-1],company,set);
		}
	}
	
	return ret;
}

/*
This function takes in a company name and keyword set. It opens
the file containing the previous values and retrieves the latest
value, then calls the make_single_prediction_INTERNAL function to 
return a prediction based on that value
*/
double make_single_prediction_EXTERNAL(char* company, char* set){
	
	
	char fname[100];
	strcpy(fname,"../../");
	strcat(strcat(fname,company),"/PREVIOUS_VALUES.dat");
	FILE* last_values = fopen(fname, "r");
	char fname1[100];
	strcpy(fname1,"../../");
	strcat(strcat(fname1,company),"/PREVIOUS_CHANGES.dat");
	FILE* last_changes = fopen(fname1, "r");
	double last_val;
	char line[10];
	while(fgets(line,10,last_values)){
		last_val = atof(line);
	}
	double last_change;
	char line1[10];
	while(fgets(line1,10,last_changes)){
		last_change = atof(line1);
	}
	
	return make_single_prediction_INTERNAL(last_change,last_val,company,set);
}

/*
This function is used to make a single prediction based on the
last value (either actual or predicted) and return it. It uses
the weighting values that are dynamically updated when new data
is added to the model in order to weight the relevance of each 
of the last 100 values to the next value. It also takes in set
of keywords that are dominant at this time period and uses the
relevant model based on these values.
*/
double make_single_prediction_INTERNAL(double last_change,double last_val,char* company, char* set){
	
	FILE *WEIGHTING;
	
	int i;
	
	int weighting_values[100];
	
	
	//read in the dynamicaly assigned weighting values
	char fname[100];
	strcpy(fname,"../../");
	strcat(strcat(strcat(strcat(strcat(fname,company),"/"),set),"/"),"WEIGHTING.dat");
	WEIGHTING = fopen(fname,"r");
	
	for(i=0;i<100;i++){
		
		char line[3];
		fgets(line,3,WEIGHTING);
		weighting_values[i] = atoi(line);
		
	}
	
	fclose(WEIGHTING);
	
	double list_expected_changes[100];
	
	for(int i=1;i<=100;i++){
		char i_str[3];
		sprintf(i_str,"%d",i);
		char filename[100];
		strcpy(filename,"../../");
		strcat(strcat(strcat(strcat(strcat(strcat(filename,company),"/"),set),"/"),i_str),".dat");
		double expected_change = get_expected_value(filename,last_change);
		
		list_expected_changes[i] = expected_change;
	}
	
	double actual_expected_change=0;
	for(i=0;i<100;i++){
		actual_expected_change += weighting_values[i]*list_expected_changes[i];
	}
	
	return last_val + actual_expected_change;
}


/*
This function opens the file passed to it and then searches in
it for the value that it takes in. It then returns the expected 
change given the value
*/
double get_expected_value(char* filename, double prev_val){
	
	double expected_value = prev_val;
	FILE *fp = fopen(filename,"r");
	char first_val[10];
	char *excess;
	
	
	while(fgets(first_val,10,fp)){
		
		//if this is the line
		if(strtod(first_val,&excess) == prev_val){
			//loop until next colon
			char c;
			
			do{
				c = fgetc(fp);
			}while(c != ':');
			
			char val_block[10];
			char* val_excess;
			
			fgets(val_block,10,fp);
			expected_value = strtod(val_block,&val_excess);
			break;
		}
	}
	
	fclose(fp);
	return expected_value;
	
}

/*
This function updates the model with the new data that has just
been recieved.
*/
void update_probabilities(char *company, char *set,double last_val){
	
	char filename[100];
	strcpy(filename,"../Data/");
	strcat(strcat(filename,company),"/PREVIOUS_VALUES.dat");
	printf("%s\n", filename);
	double changes_list[390];//Maximum number of values 
	FILE *fp = fopen(filename,"r");
	if(fp){
		printf("opened\n");
	}
	double next_val;
	int len_changes=0;//number of actual changes 
	char line[15];
	while(fgets(line,13,fp)){
		sscanf(line,"%lf",&next_val);
		changes_list[len_changes++] = next_val - last_val;
		last_val = next_val;
		
	}
	fclose(fp);
	int i;
	
	int x;
	for(x=0;x<100;x++){
		
		char x_str[3];
		sprintf(x_str,"%d",x);
		struct model_data *HEAD = NULL;
		struct model_data *CURR = HEAD;
		int len_model = 0;
		char filename1[100];
		strcpy(filename1,"../Data/");
		strcat(strcat(strcat(strcat(strcat(strcat(filename1,company),"/"),set),"/"),x_str),".dat");
		double buff_change, buff_expected;
		int buff_count;
		
		FILE *fp1 = fopen(filename1, "r");
		if(fp1){
			printf("opened file\n");
		}
		else{
			printf("File Doesn't Exist");
			fp1 = fopen(filename1, "w");
			fclose(fp1);
			fp1 = fopen(filename1, "r");
		}
		char line1[50];
		while(fgets(line1,48,fp1)){
			sscanf(line1,"%lf expected:%lf count:%d",&buff_change,&buff_expected,&buff_count);
			CURR = malloc (sizeof(struct model_data));
			CURR->next = HEAD;
			CURR->change = buff_change;
			CURR->count = buff_count;
			CURR->expected_change = buff_expected;
			printf("BUFF: %.3lf expected:%.3lf count:%d\n", buff_change,buff_expected,buff_count);
			printf("%.3lf expected:%.3lf count:%d\n", CURR->change,CURR->expected_change,CURR->count);
			HEAD = CURR;
		}
		fclose(fp1);
		int i;
		for(i=0;i<len_changes-1;i++){
			bool found = false;
			for(CURR = HEAD;CURR != NULL;CURR = CURR->next){
				
				if(changes_list[i] - CURR->change > -0.0001 && changes_list[i] - CURR->change < 0.0001){
					CURR->expected_change = ((CURR->count/(CURR->count + 1.0)) * CURR->expected_change) + (1.0/(CURR->count+1)) * changes_list[i+1];
					CURR->count++;
					found = true;
					break;
				}
			}

			if (!found){
				struct model_data * NEW = malloc (sizeof(struct model_data));
				NEW->next = HEAD;
				NEW->change = changes_list[i];
				NEW->count = 1;
				NEW->expected_change = changes_list[i+1];
				HEAD = NEW;
			}
		}

	
		FILE *fp2 = fopen(filename1,"w");
		if(fp2){
			printf("opened file\n");
		}
		else{
			printf("Failed Opening\n");
		}
	
		for(CURR = HEAD;CURR != NULL;CURR = CURR->next){
		
			fprintf(fp2,"%.3lf expected:%.3lf count:%d\n", CURR->change,CURR->expected_change,CURR->count);
		}
	
		fclose(fp2);
		printf("Moving to file %d", x);
	}
	
	return;
}

/*
This function takes in the list and writes it to the list of
previous values in the file for the company given
*/
double append_to_values(double *values_list,int n_values, char *company){
	
	double last_val;
	
	FILE *fp;
	char filename[100];
	
	strcpy(filename,"../Data/");
	strcat(strcat(filename,company),"/PREVIOUS_VALUES.dat");
	printf("%s\n",filename);
	char buffer_line[20];
	char *line = malloc(20);
	
	char* excess;
	line = read_last_line(filename);
	printf("%s\n",line);
	sscanf(line,"%lf",&last_val);
	fp = fopen(filename,"w");
	int i;
	for(i=0;i<n_values;i++){
		fprintf(fp,"%.3lf\n",values_list[i]);
	}
	fclose(fp);
	return last_val;
	
}

/*
TO BE IMPLEMENTATED LATER
*/
void update_weighting_values(double *values_list,int n_values, char *company, char *set){
	
    return;
}

/*
This function takes in a filename, opens the file and return the last
line of that file in char* format
*/
char *read_last_line(char *filename){
    FILE *fp;
    char buff[21];

    if(fp = fopen(filename, "rb")){
        fseek(fp,-21,SEEK_END);
        fread(buff, 20, 1, fp);            
        fclose(fp);                               

        buff[20] = '\0';                   
        char *last_newline = strrchr(buff, '\n'); 
        char *last_line = last_newline+1;         

        return last_line;
    }
    else{
		printf("NULL FILE\n");
        return NULL;
    }
}