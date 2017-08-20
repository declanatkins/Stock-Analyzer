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
#include <stdbool.h>

//external functions
bool add_values(double *values_list, char* company, char* set);
double *get_predicted_values(char *company, char* set);
double make_single_prediction_EXTERNAL(char *company, char* set);

//internal functions
bool append_to_values(double *values_list, char *company, char* set);
bool update_probabilities(char *company, char* set,double last_val);
double make_single_prediction_INTERNAL(double last_change,double last_val,char* company, char* set);
double get_expected_value(char *filename,double prev_val);
bool update_weighting_values(char *company, char *set);

struct model_data{
	double change;
	double expected_change;
	int count;
}model_data;

/*
This function is called from the python side in order
to add the actual values into the model. It returns true
on a successful completion and false if an error occurs
*/
void add_values(double *values_list, char *company, char* set){
	
	double last_val;
	
	last_val = append_to_values(values_list,company,set);
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
			strcpy(fname,"../../")
			strcat(strcat(strcat(fname,company),"/"),"PREVIOUS_VALUES.dat");
			FILE* last_values = fopen(fname);
	
			char line[10];
			while(fgets(line,10,last_values){
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
	strcpy(fname,"../../")
	strcat(strcat(fname,company),"/PREVIOUS_VALUES.dat");
	FILE* last_values = fopen(fname);
	char fname1[100];
	strcpy(fname1,"../../")
	strcat(strcat(fname1,company),"/PREVIOUS_CHANGES.dat");
	FILE* last_values = fopen(fname1);
	
	char line[10];
	while(fgets(line,10,last_values){
		last_val = atof(line);
	}
	
	char line1[10];
	while(fgets(line1,10,last_changes){
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
	
	int N_FILES = 100;
	FILE *WEIGHTING;
	
	int i;
	
	int weighting_values[N_FILES];
	
	
	//read in the dynamicaly assigned weighting values
	char fname[100];
	strcpy(fname,"../../")
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
		strcpy(filename,"../../")
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
	char excess[10];
	
	
	while(fgets(first_val,10,fp) && !found){
		
		//if this is the line
		if(strtod(first_val,&excess) == prev_val){
			//loop until next colon
			char c;
			
			do{
				c = fgetc(fp);
			}while(c != ':');
			
			char val_block[10];
			char val_excess[10];
			
			fgets(val_block,10,fp);
			expected_value = strtod(val_block,&val_excess);
			break;
		}
	}
	
	fclose(fp);
	return expected_value;
	
}

void update_probabilities(double last_val,char *company, char *set){
	
	char filename[100];
	strcpy(filename,"../../")
	strcat(strcat(filename,company),"/PREVIOUS_VALUES.dat");
	double *changes_list = (double*) malloc(sizeof(double));
	
	FILE *fp = fopen(filename,"r");
	double next_val;
	int len_changes=0;
	while(fscanf(fp,"%lf",&next_val)){
		
		changes_list = realloc(changes_list,sizeof(double));
		changes_list[len_changes++] = next_val - last_val;
		last_val = next_val;
		
	}
	fclose(fp);
	
	struct model_data *model = (model_data*) malloc(sizeof(model_data));
	int len_model = 0;
	char filename1[100];
	strcpy(filename1,"../../")
	strcat(strcat(strcat(strcat(strcat(strcat(filename1,company),"/"),set),"/"),i_str),".dat");
	double buff_change, buff_expected;
	int buff_count;
	
	FILE *fp1 = fopen(filename1, "w");
	
	while(fscanf(fp1,"&lf expected:%lf count:%d",&buff_change,&buff_expected,&buff_count)){
		
		struct model_data buff;
		buff.change = buff_change;
		buff.expected = buff_expected;
		buff.count = buff_count;
		
		model = realloc(model, sizeof(model_data));
		model[len_model++] = buff;
	}
	fclose(fp1);
	
	int i,j;
	for(i=0;i<len_changes-1;i++){
		for(j=0;j<len_model;j++){
			
			if(changes_list[i] == model[j].change){
				
				model[j].count++;
				model[j].expected_change = model[j].expected_change*((model[j].count-1)/model[j].count) + changes_list[i]*(1/model[j].count);
				break;
			}
		}
	}
	
	FILE *fp2 = fopen(filename1,"w");
	
	for(;*model;model++){
		
		fprintf(fp2,"%.3lf expected:%lf count:%d", *model->change,*model->expected_change,*model->count);
	}
	
	fclose(fp2);
	
	return;
	
}

double append_to_values(double *values_list, char *company){
	
	double last_val;
	
	FILE *fp;
	char filename[100];
	
	strcpy(filename,"../../")
	strcat(strcat(filename,company),"/PREVIOUS_VALUES.dat");
	
	fp = fopen(filename,"r");
	
	char line[20];
	char excess[20];
	
	while(fgets(line,20,fp){
		continue;
	}
	
	last_val = strtod(line,&excess);
	fclose(fp);
	fp = fopen(filename,"w");
	
	for(;*values_list;values_list++){
		fprintf(fp,"%.3lf", *values_list);
	}
	
	return last_val;
	
}