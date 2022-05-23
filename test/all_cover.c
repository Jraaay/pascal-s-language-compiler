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
bool g[50][100]; 

int func(int* a, float b){
	int i; 
	
	if(b == 0){
		return *a; 
	}
	else{
		return func(a, b); 
	}
	for(i = 1; i < *a; i++){
		printf("b: %f\n", b); 
	}
	i = 0; 
	while(i != 5){
		printf("b: %f\n", b); 
		i = i + 1; 
	}
	func(a, b); 
}

int main(int argc, char* argv[]){
	printf("f.f3.f31: %f\n", f.f3.f31); 
	scanf("%d%d", &x, &y); 
	printf("x: %d\ny: %d\n", x, y); 
	func(&x, y); 
}
