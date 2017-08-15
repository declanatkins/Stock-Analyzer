/*
Author: Declan Atkins
Last Modified: 15/08/17

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
bool add_values(double *changes_list, char* company, char* set);
double *get_predicted_values(char *company, char* set);
double make_single_prediction(char *company, char* set);
//internal functions
bool append_to_values(double *changes_list, char *company, char* set);
bool update_probabilities(char *company, char* set);



/*
This function is called from the python side in order
to add the actual values into the model. It returns true
on a successful completion and false if an error occurs
*/
bool add_values(double *changes_list, char *company, char* set){
	
	bool success;
	
	success = append_to_values(changes_list,company,set);
	if(!success){
		return false;
	}
	else{
		success = update_probabilities(company,set);
	}
	
	return success;
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
		
		ret[i] = make_single_prediction(company,set);
	}
	
	return ret;
}


double *make_single_prediction(char* company, char* set){
	
}

