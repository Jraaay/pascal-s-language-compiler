#include<stdio.h>
#include<stdbool.h>

struct {
	char title[50]; 
	char author[50]; 
	char subject[100]; 
	int bookid; 
}
Books; 
char a[100]; 
int b; 

int main(int argc,  char* argv[]){
	a[1] = Books.title[1]; 
	b = Books.bookid; 
}
