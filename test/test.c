#include<stdio.h>
#include<stdbool.h>
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

int gcd(int* a, int* b){
	if(b==0){
		g.c.d=a;
	}
	else{
		g.c.d=gcd(b,b);
	}
	gcd(a,b);
}

int main(int argc, char* argv[]){
	scanf("%d%d",&x,&y);
	printf("x: %d\ny: %d\n",x,y);
	while(x!=y){
		printf("x: %d\ny: %d\n",x,y);
	}
	gcd(x,y);
}
