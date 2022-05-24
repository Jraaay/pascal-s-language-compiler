struct {
	char title[101]; 
	char author[50]; 
	char subject[100]; 
	int bookid; 
	struct {
		char title[101]; 
		char author[51]; 
		char subject[100]; 
		int bookid; 
	}
	Books2; 
}
Books; 
char a[100]; 
int b; 

int main(int argc, char* argv[]){
	a[0] = Books.title[0]; 
	a[0] = Books.Books2.title[0]; 
	a[0] = Books.Books2.author[b]; 
	a[0] = Books.Books2.author[10]; 
	b = Books.bookid; 
}
