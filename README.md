Graph-drawing program to find Jacobians of graphs, and guess at the
monodromy pairing associated with them.


Requirements
================

- Sage (http://www.sagemath.org/). Required to compute invariant
factors of the Jacobian.

- SymPy (http://sympy.org/). Required to compute gonality/divisor
equivalence, and guess pairings on the Jacobian.

- Python (https://www.python.org/). For best performance, use the same
version of python that comes with Sage. For Sage 6.2 this is Python
2.7.

- wxPython (http://www.wxpython.org/)


This program has been tested on Linux and OS/X. Windows may or may not
work if you manage to get Sage set up nicely.

Setup
============

- Install required software (see above)

- Download repository contents

Running
===========

run "python main.py" from the command line to launch.

Drawing Graphs
-----------------

- Click to place a vertex. 

- Click two vertices to create an edge between them. 

- Shift-click to both place a vertex and create an edge between it and
the currently selected vertex.

- Right click to delete a vertex

Gonality computation is pretty slow at the moment, so it's only
computed when you explicitly tell the program to do so.

TODO:
=========

make gonality computations more efficient (possibly by porting to
Cython, possibly by cleaning up the algorithm implementation)

incorporate Sage/elementary divisor computation in a more better way