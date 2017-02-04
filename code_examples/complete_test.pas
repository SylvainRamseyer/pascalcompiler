Program Hello_World;
VAR
  int1  : integer;
  int2  : integer;
  real1 : real;
  real2 : real;
  bool1 : boolean;
  bool2 : boolean;
  char1 : char;
Begin
  {assignation des variables}
  int1  := 1;
  int2  := 2;
  real1 := 3.5;
  real2 := 4.5;
  bool1 := true;
  bool2 := false;
  char1 := 'c';

  {test d'écriture}
  Write(5 + 8);
  Write(12.4 + 2.2);
  Write('h');

  Write(int1);
  int1 := int1 * int2;
  Write(int1);

  Write(real1);
  real2 := real1 / 2.3;
  Write(real2);

  Write(bool1);
  Write(bool2);
  bool1 := bool1 and bool2;
  bool2 := bool1 or bool2;
  Write(bool1);
  Write(bool2);

  Write(char1);
  char1 := 'f';
  Write(char1);

End.
