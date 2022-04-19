#include<stdio.h>
#include<stdbool.h>

int x, y;

bool gcd(int a, int b){
	if(b==0){
		g.c.d=a;
	}
	else{
		g.c.d=gcd(b,a%b);
	}
}

int main(int argc, char* argv[]){
	scanf("%d%d",&x,&y);
	printf("gcd(x,y): %d\n",gcd(x,y));
}
