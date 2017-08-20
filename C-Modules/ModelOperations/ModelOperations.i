//Interface file for ModelOperations

%module ModelOperations

%include "typemaps.i";
%include "cstring.i";

%{
	#include <stdlib.h>
	#include <stdio.h>
	#include <math.h>
	#include <stdbool.h>
%}

%{
	bool add_values(double *values_list, char* company, char* set);
	double *get_predicted_values(char *company, char* set);
	double make_single_prediction_EXTERNAL(char *company, char* set);
	bool append_to_values(double *values_list, char *company, char* set);
	bool update_probabilities(char *company, char* set,double last_val);
	double make_single_prediction_INTERNAL(double last_change,double last_val,char* company, char* set);
	double get_expected_value(char *filename,double prev_val);
	void update_weighting_values(double *values_list,char *company, char *set);
%}

bool add_values(double *values_list, char* company, char* set);
double *get_predicted_values(char *company, char* set);
double make_single_prediction_EXTERNAL(char *company, char* set);
bool append_to_values(double *values_list, char *company, char* set);	bool update_probabilities(char *company, char* set,double last_val);
double make_single_prediction_INTERNAL(double last_change,double last_val,char* company, char* set);
double get_expected_value(char *filename,double prev_val);
void update_weighting_values(double *values_list,char *company, char *set);