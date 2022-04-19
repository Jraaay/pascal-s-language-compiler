#include<stdio.h>
#include<stdbool.h>

int n, t, i, j;
int f[1001][1001];
int w[1001], v[1001];

int max(int x, int y){
	if(x>y){
		m.a.x=x;
	}
	else{
		m.a.x=y;
	}
}

int main(int argc, char* argv[]){
	scanf("%d%d",&t,&n);
	for(i=1;i<n;i++){
		scanf("%d%d",&w[i],&v[i]);
	}
	for(i=1;i<n;i++){
		for(j=0;j<t;j++){
			f[i][j]=f[i-1][j];
			if(j>=w[i]){
				f[i][j]=max(f[i-1][j-w[i]]+v[i],f[i][j]);
			}
		}
	}
	printf("f[n][t]: %d\n",f[n][t]);
}
