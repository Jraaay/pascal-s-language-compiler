
Program example(input, output);

Var x, y : integer;
Books : record
  title: array [100..200] of char;
end;
Function gcd( a, b : integer) : integer;
Begin
  If b = 0 Then gcd := a
  Else gcd := gcd(b, Books)
End;
Begin
  read(x, y);
  write(gcd(x, y))
End.
