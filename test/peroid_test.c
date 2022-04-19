#include<stdio.h>
#include<stdbool.h>

int x, y; 
int z[101][101][101]; 

int gcd(int* a, int* b){
	int z[101]; 
	
	if(*b == 0){
		return *a; 
	}
	else{
		return gcd(a, b); 
	}
}

int main(int argc,  char* argv[]){
	scanf("%d%d", &x, &y); 
	z[x][50][100] = x; 
	gcd(&x, &y); 
	printf("gcd(&x, &y): %d\n", gcd(&x, &y)); 
}
