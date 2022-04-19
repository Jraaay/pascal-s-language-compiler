#include<stdio.h>
#include<stdbool.h>

int a[5]; 
int x, y; 

void readarray(){
	int i; 
	
	i = 0; 
	while(i < 5){
		scanf("%d", &y); 
		a[i-0] = y; 
		i = i + 1; 
	}
}

void quicksort(int l, int h){
	int i, j, k, m; 
	
	i = l; 
	j = h; 
	k = a[i-0]; 
	if(l < h){
		while(i < j){
			while((a[j-0] >= k) && (i < j)){
				j = j - 1; 
			}
			a[i-0] = a[j-0]; 
			while((a[i-0] <= k) && (i < j)){
				i = i + 1; 
			}
			a[j-0] = a[i-0]; 
		}
		a[i-0] = k; 
		quicksort(l, i - 1); 
		quicksort(j + 1, h); 
	}
	else{
		m = 0; 
	}
}

int main(int argc,  char* argv[]){
	x = 0; 
	readarray(); 
	quicksort(0, 4); 
	while(x < 5){
		y = a[x-0]; 
		printf("y: %d\n", y); 
		x = x + 1; 
	}
}
