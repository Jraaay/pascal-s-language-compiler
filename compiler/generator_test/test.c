#include<stdbool.h>

const int a = 5;
const int b = -6;
const char c = 't';

int x, y, d;
char e[50];
struct {
	float f1;
	bool f2[50][100];
}
f;

int gcd(int a, int b){
	if(b==0){
		return a;
	}
	else{
		return gcd(b,a%b);
	}
}

int main(int argc, char* argv[]){
	;
}
