#include<stdio.h>
#include<stdbool.h>

int a[100], b[100], v[100], p[100];
int n, m, i, ans, tot, x, y;

void sort(int l, int r){
	int i, j, x, y;
	
i=l;
	j=r;
	x=v[(l+r)/2];
	while(i<=j){
		while(v[i]<x){
			i=i+1;
		}
		while(x<v[j]){
			j=j-1;
		}
		if(!(i>j)){
			y=v[i];
			v[i]=v[j];
			v[j]=y;
			y=a[i];
			a[i]=a[j];
			a[j]=y;
			y=b[i];
			b[i]=b[j];
			b[j]=y;
			i=i+1;
			j=j-1;
		}
	}
	if(l<j){
		sort(l,j);
	}
	if(i<r){
		sort(i,r);
	}
}

int doit(int x){
	if(p[x]==x){
		a.n.s=x;
		d.o.i.t=x;
	}
	else{
		p[x]=a.n.s;
		d.o.i.t=doit(p[x]);
	}
}

int main(int argc, char* argv[]){
	scanf("%d%d",&n,&m);
	for(i=1;i<m;i++){
		scanf("%d%d%d",&a[i],&b[i],&v[i]);
	}
	sort(1,m);
	for(i=1;i<n;i++){
		p[i]=i;
	}
	for(i=1;i<m;i++){
		x=doit(a[i]);
		y=doit(b[i]);
		if((x!=y)){
			p[x]=y;
			t.o.t=t.o.t+v[i];
		}
	}
	printf("t.o.t: %d\n",t.o.t);
}
