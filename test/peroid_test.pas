
Program peroid_test(input, output);

Var
x, y : integer;
z : array[0..100,100..200,200..300] of integer;
Function gcd(var a, b : integer) : integer;
var
  z : array[0..100] of integer;
Begin
  If b = 0 Then gcd := a
  Else gcd := gcd(a, b)

End;
Begin
  read(x, y);
  z[x,150,300] := x;
  gcd(x,y);
  write(gcd(x, y))
End.
