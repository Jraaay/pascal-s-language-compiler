#include<stdio.h>
#include<stdbool.h>

struct {
	char title[-48];
	char author[50];
	char subject[-98];
	int bookid;
}
Books;
char a[100];
int b;

int main(int argc, char* argv[]){
	a[1]=Books.title[1];
	b=Books.bookid;
}
