# Pascal compiler in Python
Welcome to our README section. This project's goal, as it is mentioned in the title, is to create a compiler in Python for the Pascal language. 
As the language the compiler is being created for, some preliminary research/analysis had to be taken care of.
The compiler will stay quite basic as it is part of a school project (with a deadline..). 

# Specifications
The current section presents each point more in detail, but first, let's take a look at its quick summary :

* The basics
  * Variable types
  * Arithmetic operators
  * Logical operators
  
* Flow control
  * Conditional
  * Loops
  
* Functions
  * Pre-written functions
  * "Hand-made" functions

If you are familiar with the Pascal language or not, this is how the program skeleton is written basically:

```pascal
{PROGRAM}
PROGRAM program_name;
{VARIABLES: global scope}
{standard variable declaration}
VAR 
  var1, var2 : variable_type;
{constant variable declaration and initialization}
CONST 
  varC_1 = something;
  varC_2 = something_else;
{functions + procedures}
{PROGRAM START}
BEGIN
  {code}
END.
```

## The basics
### Variable types
The following types will be handled by the compiler :
+ Integer
+ Real
+ Bool
+ Char

If you know how Pascal does work, you're probably familiar with the following : we must precise when a variable is a constant at the beginning of our program.

```pascal
VAR variable_name : variable_type;
```

```pascal
{constant variable declaration + initialization -> using = }
CONST variable_name = something;
```

### Arithmetic operators
The following operation will be handled by the compiler : 
+ Arithmetic operation

```pascal
{sum affectation -> using := }
sum := a + b;
```

### Logical operators
The following operators will be handled by the compiler : 
+ AND
+ OR
+ NOT

```pascal
(a = true) AND (b = false)
```

### Comments section
The compiler will be able to recognize and ignore the comments written throughout the code.

```pascal
{I will be ignored by the compiler *sob*}
```

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
There are two types of functions, those we create and those that are already in the language.
We decided to manage both, as it is shown below.

### Pre-written functions
The following function will be handled by the compiler : 
+ Write
+ Writeln

```pascal
Writeln('Hello world!');
```
```pascal
Writeln('My name is ', name);
```

### "Hand-made" functions
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
VAR variable_name_inside_function : variable_type;
BEGIN
  {code}
END.
```

## Reserved words
The following reserved words will be taken care of:
```pascal
{variable types}
INTEGER
REAL
BOOL
CHAR

{arithmetic operators}
+
-
*
/

{logical operator}
AND
OR
NOT


{program}
PROGRAM

{variables}
VAR
CONST

{functions}
FUNCTION
PROCEDURE
WRITE
WRITELN

{flow control}
IF
THEN
REPEAT
UNTIL
WHILE
DO

{start + end of section}
BEGIN
END.
```
