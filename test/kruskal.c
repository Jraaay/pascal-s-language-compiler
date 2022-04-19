#include<stdio.h>
#include<stdbool.h>

int a[100], b[100], v[100], p[100]; 
int n, m, i, ans, tot, x, y; 

void sort(int l, int r){
	int i, j, x, y; 
	
	i = l; 
	j = r; 
	x = v[(l + r) / 2-1]; 
	while(i <= j){
		while(v[i-1] < x){
			i = i + 1; 
		}
		while(x < v[j-1]){
			j = j - 1; 
		}
		if(!(i > j)){
			y = v[i-1]; 
			v[i-1] = v[j-1]; 
			v[j-1] = y; 
			y = a[i-1]; 
			a[i-1] = a[j-1]; 
			a[j-1] = y; 
			y = b[i-1]; 
			b[i-1] = b[j-1]; 
			b[j-1] = y; 
			i = i + 1; 
			j = j - 1; 
		}
	}
	if(l < j){
		sort(l, j); 
	}
	if(i < r){
		sort(i, r); 
	}
}

int doit(int x){
	if(p[x-1] == x){
		ans = x; 
		return x; 
	}
	else{
		p[x-1] = ans; 
		return doit(p[x-1]); 
	}
}

int main(int argc, char* argv[]){
	scanf("%d%d", &n, &m); 
	for(i = 1; i < m; i++){
		scanf("%d%d%d", &a[i-1], &b[i-1], &v[i-1]); 
	}
	sort(1, m); 
	for(i = 1; i < n; i++){
		p[i-1] = i; 
	}
	for(i = 1; i < m; i++){
		x = doit(a[i-1]); 
		y = doit(b[i-1]); 
		if((x != y)){
			p[x-1] = y; 
			tot = tot + v[i-1]; 
		}
	}
	printf("tot: %d\n", tot); 
}
