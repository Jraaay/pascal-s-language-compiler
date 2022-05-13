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
    g : array [1..50, 1..100] of boolean;

Function func(var a: integer; b:real) : integer;
// Function func(var a : integer,b : integer) : integer;
var i:integer;
Begin
    for i:=1 to a do
        begin
          write(b);
        end;
    While i<5 Do
        begin
            write(y);
        end;
    func(a,b);
    If b = 0 Then func := a
    Else func := func(a, b);
End;

Begin
    read(x,y);
    write(x,y);
    while x<>y do write(x,y);
    func(x, y)
End.