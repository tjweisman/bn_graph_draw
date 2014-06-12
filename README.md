Graph-drawing program to find Jacobians of graphs, and guess at the
monodromy pairing associated with them.


REQUIREMENTS:

Sage (http://www.sagemath.org/). Required to compute invariant factors
of the Jacobian.

SymPy (http://sympy.org/). Required to compute gonality and guess pairing

Python (https://www.python.org/). Version MUST match the version
installed with Sage; for Sage 6.2 this is Python 2.7

wxPython (http://www.wxpython.org/)


This program should work on Windows, OS/X, or Linux, although right
now computing the Jacobian only works on Linux since I integrated the
app with Sage in an extremely messy way


SETUP:

-Install required software (see above)

-Download repository contents

-Change the first line of the file "launch" to point to the root of
 your Sage installation


RUNNING:

To run the graph drawer, run "./launch" from the repo directory. If
this doesn't seem to be working, you can run "python main.py" (the
program will still work, but you won't be able to compute Jacobians)

Click to place a vertex. Click two vertices to create an edge between
them. Shift-click to both place a vertex and create an edge between it
and the currently selected vertex.

TODO: 

make gonality computations more efficient (possibly by porting to
Cython, possibly by cleaning up the algorithm implementation)