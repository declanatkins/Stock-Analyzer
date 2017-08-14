/*Parsed Image Search

Author Declan Atkins
Last Changed 14/08/17

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

int **get_xy_values(int **image, int x_size, int y_size);
bool all_zero(int *pos);



bool all_zero(int *pos){
	
	for(;*pos;pos++){
		if(*pos != 0){
			return false;
		}
	}
	
	return true;
}


int **get_xy_values(int **image, int x_size, int y_size){
	
	int** values;
	int i,j;
	for(i=0;i<y_size;i++){
		for(j=0;i<x_size;j++){
			
			if(!all_zero(image[i][j]){
				
				if(i>0 && all_zero(image[i-1][j])){
					values = realloc(values,2*sizeof(int))
				}
			}
			
		}
	}
}

