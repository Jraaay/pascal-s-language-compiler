{Bonus Features: Record}

Program example(input, output);


var
Books : record
  title: array [100..200] of char;
  author: array [1..50] of char;
  subject: array [1..100] of char;
  bookid: integer;
  Books2: record
    title: array [200..300] of char;
    author: array [0..50] of char;
    subject: array [1..100] of char;
    bookid: integer;
  end;
end;
a : array [1..100] of char;
b : integer;

Begin
  a[1] := Books.title[100];
  a[1] := Books.Books2.title[200];
  a[1] := Books.Books2.author[b];
  a[1] := Books.Books2.author[10];
  b := Books.bookid;
End.
