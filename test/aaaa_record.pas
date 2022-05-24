Program example(input, output);
Var 
    x, y, d : integer;
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

Function func(var a: integer; b:real) : integer;
var i:integer;
Begin
    write(a,b);
    read(a);
    func(a,b);
End;

Begin
    write(f.f3.f31);
    read(x,y);
    func(x, y);
End.