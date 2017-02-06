# Pascal compiler in Python
Welcome to our README section. This project's goal, as it is mentioned in the
title, is to create a compiler in Python for the Pascal language.
As the language the compiler is being created for, some preliminary
research/analysis had to be taken care of.
The compiler will stay quite basic as it is part of a school project
(with a deadline..).

# Dependencies

You need to install the following softwares to use this compiler.

* graphviz-2.38
* pydot-1.0.3
* pyparsing-1.5.5

`pydot` and `pyparsing` can be installed using `pip`. Alternatively, you can
install the python dependencies running `pip install -r requirements.txt` in
the project folder.
_graphviz_ has to be installed using the installer (Windows) or the package
(GNU/Linux).
__Window users have to add Graphviz bin folder to their `PATH`.__

# Compiler's Specifications

If you're interested in this compiler's specification, have a look at the
[Specifications](https://github.com/SylvainRamseyer/pascalcompiler/wiki/Specifications) wiki page.

# Run the different programs

* Lexical analysis: `python lexer.py path_to/my_file/to_check`
* Parser: `python parser.py path_to/my_file/to_parse`
    * A pdf containing the syntaxic abstract tree is generated at the same
      location as the source file.
* Compiler: `python compiler.py path_to/my_file/to_compile`
    * Generates a _.vm_ file at the same location as the source file.
      This file can be executed by the SVM (Simple Virtual Machine aka
      Stupid Virtual Machine).
* Run: `python svm.py path_to/vm_my_file/to_run`
    * Runs the file through the virtual machine.
