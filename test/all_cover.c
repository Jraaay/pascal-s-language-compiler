#include<stdbool.h>
#include<stdbool.h>
#include<stdbool.h>
#include<stdio.h>

const int a = 5; 
const int b = -6; 
const char c = 't'; 

int x, y, d; 
char e[50]; 
struct {
	float f1; 
	bool f2[50][100]; 
	struct {
		float f31; 
		bool f32[50][100]; 
		struct {
			float f331; 
			bool f332[50][100]; 
			int f333; 
		}
		f33; 
	}
	f3; 
}
f; 

int gcd(int* a, int* b){
	if(*b == 0){
		return *a; 
	}
	else{
		return gcd(b, b); 
	}
	gcd(a, b); 
}

int main(int argc, char* argv[]){
	scanf("%d%d", &x, &y); 
	printf("x: %d\ny: %d\n", x, y); 
	while(x != y){
		printf("x: %d\ny: %d\n", x, y); 
	}
	gcd(&x, &y); 
}
