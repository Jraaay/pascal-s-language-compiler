#include<stdio.h>
#include<stdbool.h>

int x, y;
int z[51];

int gcd(int a, int b){
	if(b==0){
		return a;
	}
	else{
		return gcd(b,a%b);
	}
}

int main(int argc, char* argv[]){
	scanf("%d%d",&x,&y);
	z[99]=x;
	printf("gcd(x,y): %d\n",gcd(x,y));
}
