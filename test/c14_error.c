#include<stdio.h>

int x, y; 
struct {
	char title[101]; 
}
Books; 

int gcd(int a, int b){
	if(b == 0){
		return a; 
	}
	else{
		return gcd(b, Books); 
	}
}

int main(int argc, char* argv[]){
	scanf("%d%d", &x, &y); 
	printf("gcd(x, y): %d\n", gcd(x, y)); 
}
