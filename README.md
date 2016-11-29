# Pascal compiler in Python
Welcome to our README section. This project's goal, as it is mentioned in the title, is to create a compiler in Python for the Pascal language. 

# Specifications
_TODO_

```pascal
PROGRAM program_name;
VAR variable_name : variable_type;
BEGIN
  {code}
END.
```

### Variable types
The following types will be handled by the compiler :
+ Integer
+ Real
+ Bool
+ Char

```pascal
VAR variable_name : variable_type;
```

### Arithmetic operators
The following operation will be handled by the compiler : 
+ Arithmetic operation

```pascal
sum := a + b;
```

### Logical operators
The following operators will be handled by the compiler : 
+ AND
+ OR
+ NOT

## Flow Control
### Conditional operators
The following operators will be handled by the compiler :
+ IF .. THEN
```pascal
IF <condition> THEN 
  BEGIN 
    {do this code}
  END.
```
+ IF .. THEN .. ELSE
```pascal
IF <condition> THEN 
  {do this code}
ELSE 
  {do this code}
```
```pascal
IF <condition> THEN
BEGIN
  IF <condition> THEN 
    {do this}
  IF <condition> THEN 
    {do this}
  ELSE 
    {do this}
END.
```
### Loops
The following loops will be handled by the compiler : 
+ Repeat .. until (also known as 'while' in other languages)
```pascal
REPEAT 
  {code} 
UNTIL <some conditional statement is true>;
```
+ While .. do 
```pascal
WHILE <condition is true> 
DO 
  BEGIN 
    {code} 
  END.
```

## Functions
The following function types will be handled by the compiler : 
+ Procedure
```pascal
PROCEDURE procedure_name;
VAR variable_name : variable_type;
BEGIN
  {code}
END.
```
```pascal
PROCEDURE procedure_name(variable_name : variable_type);
VAR variable_name_inside_function : variable_type;
BEGIN
  {code}
END.
```
+ Function
```pascal
FUNCTION function_name(variable_name : variable type) : return_type;
Var variable_name_inside_function : variable_type;
BEGIN
  {code}
END.
```


## Reserved words
