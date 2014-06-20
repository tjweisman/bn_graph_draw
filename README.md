Graph-drawing program to find Jacobians of graphs, and guess at the
monodromy pairing associated with them.


REQUIREMENTS:

Sage (http://www.sagemath.org/). Required to compute invariant factors
of the Jacobian.

SymPy (http://sympy.org/). Required to compute gonality and guess pairing

Python (https://www.python.org/). For best performance, use the same
version of python that comes with Sage. For Sage 6.2 this is Python
2.7.

wxPython (http://www.wxpython.org/)


This program has been tested on Linux and OS/X. Windows may or may not
work if you manage to get Sage set up nicely.

SETUP:

-Install required software (see above)

-Download repository contents

OPTIONAL: If you're on Linux, change the first line of the file
"launch" to point to the root of your Sage installation.

RUNNING:

If you're on Linux, you can try running the program inside Sage python
by running "./launch" from the main repo directory. If it works, the
Jacobian of the graph should display automatically whenever you add an
edge to the graph.

If the program doesn't start at all, or it doesn't seem like Sage is
behaving properly, you can start the program with "python main.py" (do
this if you're getting any kind of error messages on program start,
since you're just wasting startup time otherwise).

You can still compute Jacobians, but Sage has to be
started as an external process each time, so it will be slower (and
won't be done automatically)

Drawing Graphs:

Click to place a vertex. Click two vertices to create an edge between
them. Shift-click to both place a vertex and create an edge between it
and the currently selected vertex.

Gonality computation is pretty slow at the moment, so it's only
computed when you explicitly tell the program to do so.

TODO: 

make gonality computations more efficient (possibly by porting to
Cython, possibly by cleaning up the algorithm implementation)

incorporate Sage/elementary divisor computation in a more better way