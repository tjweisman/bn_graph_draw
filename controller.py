"""This file contains the 'business logic' for the main application
(as opposed to the application display information). Callbacks for
buttons and infobox updating procedures are contained here.

"""
import wx, gonality
from graph_ui.graph import *
import graph_ui.sage_wrapper

class Controller:
    def __init__(self, frame):
        self.frame = frame
        self.drawer = frame.view
        self.graph = frame.view.graph
        self.divisor = frame.view.divisor
        
        self.sage_bin = self.frame.options["sage_install"].value
        if self.sage_bin != "":
            sage_wrapper.setup(self.sage_bin, "sage:")

    #open up a file dialog and write to a file
    def export_tikz(self, evt):
        dialog = wx.FileDialog(self.frame, style = wx.FD_SAVE)
        dialog.ShowModal()
        path = dialog.GetPath()
        if path != "":
            print path
            tf = open(path, "w")
            tf.write(drawgraph.get_tikz_code(self.graph))
            tf.close()

    def start_sage(self, event):
        sage_wrapper.start(self.sage_bin, "sage:")

    def compute_gonality(self, event):
        gon = gonality.gonality(self.graph)
        self.frame.set_infobox("gonality", gon)

    def draw_Bn(self,event):
        self.drawer.gen_Bn(10)

    #the function to call whenever an edge is updated
    def update_info(self):
        """mostly just updating infoboxes"""
        G = self.graph
        self.update_lap(None)
        if sage_wrapper.sage_started():
            self.compute_jacobian(None)
        self.frame.set_infobox("genus", G.genus())
        self.frame.set_infobox("pair_guess", G.guess_pairing())
        self.frame.set_infobox("gonality", ' ')
        self.frame.set_infobox("connect", G.connected())
        self.frame.set_infobox("div", self.divisor.values)
        self.frame.set_infobox("subset", self.drawer.fireset)
        self.frame.set_infobox("zero", self.divisor_zero())
    
    def clear_event(self, event):
        self.drawer.clear()

    def clear_divisor(self, event):
        self.divisor.__init__(self.graph)
        self.drawer.update_info()
        self.drawer.Refresh()

    def compute_jacobian(self, event):
        jac = self.graph.jacobian()
        if jac != None:
            trees = reduce(lambda x,y: x * y, [1]+jac)
            self.frame.set_infobox("jac",jac)
            self.frame.set_infobox("trees",trees)
        
    def update_lap(self, event):
        disp = str(self.graph.laplacian())
        if self.frame.options["mathematica"].value:
            disp = disp.replace("[","{").replace("]","}")
        self.frame.set_infobox("lap", disp)

    def try_burn(self, event):
        if self.drawer.selection: 
            subset = self.divisor.burn(self.drawer.selection)
            if not subset:
                self.frame.set_infobox("subset", "Cannot push chips closer")
                self.drawer.fireset = []
            else:
                self.frame.set_infobox("subset",
                    repr(subset) + " - press 'Fire!' to chip-fire all")
                self.drawer.fireset = subset

    def divisor_zero(self):
        self.divisor.compute_degree()
        is_zero = "False"
        try:
            if (self.divisor.degree == 0 and
                gonality.rank_nonnegative(self.divisor)):
                is_zero = "True"
        except gonality.GraphComputationError:
            return ""
        return "False"
