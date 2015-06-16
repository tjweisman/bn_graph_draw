"""This file contains the 'business logic' for the main application
(as opposed to the application display information). Callbacks for
buttons and infobox updating procedures are contained here.

"""
import wx, gonality, drawgraph
from graph import *
import subprocess

class Controller:
    def __init__(self, frame):
        self.frame = frame
        self.drawer = frame.view
        self.graph = frame.view.graph
        self.divisor = frame.view.divisor

        self.sage_process = None

    def set_infobox(self, box_name, value):
        self.frame.infoboxes[box_name].display.SetValue(str(value))
        
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

    def compute_gonality(self, event):
        gon = gonality.gonality(self.graph)
        self.set_infobox("gonality", gon)

    def draw_Bn(self,event):
        self.drawer.gen_Bn(10)

    #the function to call whenever an edge is updated
    def update_info(self):
        """mostly just updating infoboxes"""
        G = self.graph
        self.update_lap(None)
        self.compute_jacobian(None)
        self.set_infobox("genus", G.genus())
        self.set_infobox("pair_guess", G.guess_pairing())
        self.set_infobox("gonality", ' ')
        self.set_infobox("connect", G.connected())
        self.set_infobox("div", self.divisor.values)
        self.set_infobox("subset", self.drawer.fireset)
        self.set_infobox("zero", self.divisor_zero())
    
    def clear_event(self, event):
        self.drawer.clear()

    def clear_divisor(self, event):
        self.divisor.__init__(self.graph)
        self.drawer.update_info()
        self.drawer.Refresh()

    def compute_jacobian(self, event):
        print sage_ok
        if sage_ok:
            jac = self.graph.jacobian()
        elif self.frame.options["sage_install"].value != "":
            if not self.sage_process:
                sage_bin = self.frame.options["sage_install"].value
                #if this program had higher level access to things,
                #this would be horrifically insecure.
                self.sage_process = subprocess.Popen(sage_bin, shell=False)
            jac = self.graph.jacobian_sage_pipe(self.sage_process)
        else:
            jac = None
            self.set_infobox("jac", ' ')
            self.set_infobox("trees", ' ')
            
        if jac != None:
            trees = reduce(lambda x,y: x * y, [1]+jac)
            self.set_infobox("jac",jac)
            self.set_infobox("trees",trees)
        
    def update_lap(self, event):
        disp = str(self.graph.laplacian())
        if self.frame.options["mathematica"].value:
            disp = disp.replace("[","{").replace("]","}")
        self.set_infobox("lap", disp)

    def try_burn(self, event):
        if self.drawer.selection: 
            subset = self.divisor.burn(self.drawer.selection)
            if not subset:
                self.set_infobox("subset", "Cannot push chips closer")
                self.drawer.fireset = []
            else:
                self.set_infobox("subset",
                    repr(subset) + " - press 'Fire!' to chip-fire all")
                self.drawer.fireset = subset

    def divisor_zero(self):
        self.divisor.compute_degree()
        if (self.divisor.degree == 0 and 
            gonality.rank_nonnegative(self.divisor)):
            return "True"
            print self.divisor.degree
        else:
            return "False"
