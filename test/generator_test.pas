
Program example(input, output);

Var x, y, i : integer;
Function gcd( a, b : integer) : integer;
Begin
  If b = 0 Then gcd := a
  Else gcd := gcd(b, a Mod b);
  for i := 0 to 114514 do
    b:=i;
End;
Begin
  read(x, y);
  write(gcd(x, y))
End.
