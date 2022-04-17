
Program example(input, output);

Var x, y : integer;
Function gcd( a, b : integer) : integer;
Begin
  If b = 0 Then gcd := a
  Else gcd := gcd(b, a Mod b)
  For i := 114514 to 1919810 do b:=i
  While b<>114514 do b:=b-1
End;
Begin
  read(x, y);
  write(gcd(x, y))
End.
