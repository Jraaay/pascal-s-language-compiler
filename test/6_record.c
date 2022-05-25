#include<stdbool.h>
#include<stdio.h>

int x, y, d; 
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

int func(int* a, float b){
	int i; 
	
	while(i != 5){
		printf("b: %f\n", b); 
		i = i + 1; 
	}
	printf("*a: %d\nb: %f\n", *a, b); 
	scanf("%d", a); 
	func(a, b); 
}

int main(int argc, char* argv[]){
	printf("f.f3.f31: %f\n", f.f3.f31); 
	scanf("%d%d", &x, &y); 
	func(&x, y); 
}
