/*Parsed Image Search

Author Declan Atkins
Last Changed 18/08/17

This module is used for performing searches on 
a parsed image recieved from python using openCV
It finds the boundary points of a graph and returns
the x,y values of them. 

In later Development it will also be used to assign the
actual values that correspond to these x,y values, with time
on the x axis and price on the y axis.

*/

#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

int *get_xy_values(int **image, int x_size, int y_size);
bool all_zero(int *pos);
double *get_actual_values(int *y_vals, int y_size, double val1, int val1_y, double val2, int val2_y);




bool all_zero(int *pos){
	
	for(;*pos;pos++){
		if(*pos != 0){
			return false;
		}
	}
	
	return true;
}


int *get_xy_values(int **image, int x_size, int y_size){
	
	int* values;
	int pos = 0;
	int i,j;
	for(i=0;i<y_size;i++){
		for(j=0;i<x_size;j++){
			
			if(!all_zero(image[i][j]){
				
				if(i>0 && all_zero(image[i-1][j])){
					values = realloc(values,sizeof(int))
					values[pos++] = i;
				}
				else if(j>0 && all_zero(image[i][j-1])){
					values = realloc(values,sizeof(int))
					values[pos++] = i;
				}
				else if(j<x_size-1 && all_zero(image[i][j+1])){
					values = realloc(values,sizeof(int))
					values[pos++] = i;
				}
				else if(i<y_size-1 && all_zero(image[i+1][j])){
					values = realloc(values,sizeof(int))
					values[pos++] = i;
				}
				
			}
			
		}
	}
	
	return values;
}

double *get_actual_values(int *y_vals, int y_size, double val1, int val1_y, double val2, int val2_y){
	
	int i;
	double val_diff = val2 - val1;
	int y_diff = val2_y - val1_y;
	double val_per_y = val_diff/y_diff;

	double *ret_values = (double*) malloc(sizeof(double));
	int pos=0;
	for(i=0;i<y_size;i++){

		y_diff = y_vals[i] - val1_y;
		ret_values = realloc(ret_values, sizeof(double));

		ret_values[pos++] = y_diff * val_per_y;
	}

	return ret_values;
}
