#include<stdio.h>
#include<stdbool.h>

int x, y, i;

int gcd(int a, int b){
	if(b==0){
		gcd[114514]=a;
	}
	else{
		return gcd(b,a%b);
	}
	for(i=0;i<114514;i++){
		b=i;
	}
}

int main(int argc, char* argv[]){
	scanf("%d%d",&x,&y);
	printf("gcd(x,y): %d\n",gcd(x,y));
}