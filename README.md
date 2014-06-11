Graph-drawing program to find Jacobians of graphs, and guess at the
monodromy pairing associated with them.


REQUIREMENTS:

Sage (http://www.sagemath.org/). Required to compute invariant factors
of the Jacobian.

Python (https://www.python.org/). Version MUST match the version
installed with Sage; for Sage 6.2 this is Python 2.7

wxPython (http://www.wxpython.org/)

This should run on OS/X or Linux-based systems. Running it on Windows
should possible, although getting it to work with Sage will probably be
difficult.

If you can't get Sage working, you can still recover some
functionality by installing SymPy (http://sympy.org/).


SETUP:

-Install required software (see above)

-Download repository contents

-Change the first line of the file "launch" to point to the root of
 your Sage installation


RUNNING:

To run the graph drawer, run "./launch" from the repo directory.

Click to place a vertex. Click two vertices to create an edge between
them. Shift-click to both place a vertex and create an edge between it
and the currently selected vertex.


INFORMATION DISPLAY:

Top: Laplacian matrix for this graph

Middle: Nonzero elementary divisors of the Laplacian matrix

Bottom: The pairing <d,d> for some nonzero element d

TODO: 

-complete implementation of gonality-computing algorithm

-implement double-buffering