#include<stdio.h>
#include<stdbool.h>

int n, t, i, j; 
int f[1001][1001]; 
int w[1001], v[1001]; 

int max(int x, int y){
	if(x > y){
		return x; 
	}
	else{
		return y; 
	}
}

int main(int argc,  char* argv[]){
	scanf("%d%d", &t, &n); 
	for(i = 1; i < n; i++){
		scanf("%d%d", &w[i], &v[i]); 
	}
	for(i = 1; i < n; i++){
		for(j = 0; j < t; j++){
<<<<<<< HEAD
			f[i][j] = f[i - 1][j]; 
			if(j >= w[i]){
				f[i][j] = max(f[i - 1][j - w[i]] + v[i], f[i][j]); 
			}
		}
	}
	printf("f[n][t]: %d\n", f[n][t]); 
=======
			f[i-0][j-0] = f[i - 1-0][j-0]; 
			if(j >= w[i-0]){
				f[i-0][j-0] = max(f[i - 1-0][j - w[i-0]-0] + v[i-0], f[i-0][j-0]); 
			}
		}
	}
	printf("f[n-0][t-0]: %d\n", f[n-0][t-0]); 
>>>>>>> 13a701a6e25d9563f68c810eb181ffdf646c8cf6
}
