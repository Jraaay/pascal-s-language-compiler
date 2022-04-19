
Program peroid_test(input, output);

Var
x, y : integer;
z : array[50..100] of integer;
Function gcd( a, b : integer) : integer;
var
  z : array[50..100] of integer;
Begin
  If b = 0 Then gcd := a
  Else gcd := gcd(b, a Mod b)

End;
Begin
  read(x, y);
  z[99] := x;
  write(gcd(x, y))
End.
