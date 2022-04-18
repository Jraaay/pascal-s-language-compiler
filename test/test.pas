Program example(input, output);

Const 
    a = 5; 
    b = -6; 
    c = 't';

Var 
    x, y, d : integer;
    e : array [1..50] of char;
    f : record
        f1 : real;
        f2 : array [1..50, 1..100] of boolean;
    End;

Function gcd(var a, b : integer) : integer;
Begin
  If b = 0 Then gcd := a
  Else gcd := gcd(b, a Mod b)
End;

Begin
read(x,y);
write(x,y);
while x<>y do write(x,y);
gcd(x, y)
End.