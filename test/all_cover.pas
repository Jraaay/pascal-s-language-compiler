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
        f3 : record
            f31 : real;
            f32 : array [1..50, 1..100] of boolean;
            f33 : record
                f331 : real;
                f332 : array [1..50, 1..100] of boolean;
                f333 : integer;
            End;
        End;
    End;

Function gcd(a : integer; b : real) : integer;
Begin
    If b = 0 Then gcd := a
    Else gcd := gcd(b, b);
    gcd(a,b)
End;

Begin
    read(x,y);
    write(x,y);
    while x<>y do write(x,y);
    gcd(x, y)
End.