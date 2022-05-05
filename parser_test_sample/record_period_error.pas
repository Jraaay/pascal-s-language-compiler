{Bonus Features: Record}

Program example(input, output);


var
Books : record
  title: array [50..1] of char;
  author: array [1..50] of char;
  subject: array [100..1] of char;
  bookid: integer;
end;
a : array [1..100] of char;
b : integer;

Begin
  a[1] := Books.title[1];
  b := Books.bookid;
End.
