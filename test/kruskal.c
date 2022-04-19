#include<stdio.h>
#include<stdbool.h>

int a[100], b[100], v[100], p[100]; 
int n, m, i, ans, tot, x, y; 

void sort(int l, int r){
	int i, j, x, y; 
	
	i = l; 
	j = r; 
	x = v[(l + r) / 2-0]; 
	while(i <= j){
		while(v[i-0] < x){
			i = i + 1; 
		}
		while(x < v[j-0]){
			j = j - 1; 
		}
		if(!(i > j)){
			y = v[i-0]; 
			v[i-0] = v[j-0]; 
			v[j-0] = y; 
			y = a[i-0]; 
			a[i-0] = a[j-0]; 
			a[j-0] = y; 
			y = b[i-0]; 
			b[i-0] = b[j-0]; 
			b[j-0] = y; 
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
	if(p[x-0] == x){
		ans = x; 
		return x; 
	}
	else{
		p[x-0] = ans; 
		return doit(p[x-0]); 
	}
}

int main(int argc,  char* argv[]){
	scanf("%d%d", &n, &m); 
	for(i = 1; i < m; i++){
		scanf("%d%d%d", &a[i-0], &b[i-0], &v[i-0]); 
	}
	sort(1, m); 
	for(i = 1; i < n; i++){
		p[i-0] = i; 
	}
	for(i = 1; i < m; i++){
		x = doit(a[i-0]); 
		y = doit(b[i-0]); 
		if((x != y)){
			p[x-0] = y; 
			tot = tot + v[i-0]; 
		}
	}
	printf("tot: %d\n", tot); 
}
