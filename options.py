"""This file contains the definitions of the options dialog, as well
as a definition of all the actual program options and procedures for
saving/loading options from a config file.

"""
import wx
import cPickle as pickle

OK=0
CANCEL=1

BOOLEAN=0
TEXTBOX=1

def setup_options(frame):

    #define more options here if need be

    frame.options["mathematica"] = Option(
        "Mathematica Output", BOOLEAN, False)

    frame.options["divisor_iput"] = Option(
        "Show divisor input", BOOLEAN, True)

    #automatically create display options for every infobox
    for key, infobox in frame.infoboxes.iteritems():
        frame.options[key] = Option("Display " + infobox.name, BOOLEAN, True)

    #load defaults
    try:
        load_options(frame.options)
    except (IOError, EOFError, pickle.PicklingError):
        print "No valid config file found, creating default config file"
        save_options(frame.options)

def load_options(options):
    with open('.config', 'r') as cfg:
        load_opts = pickle.load(cfg)
        for (key, label, opt_type, value) in load_opts:
            options[key] = Option(label, opt_type, value)

def save_options(options):
    with open('.config', 'w') as cfg:
        opt_dump = [(key, opt.label, opt.opt_type, opt.value) 
                    for key, opt in options.iteritems()]
        pickle.dump(opt_dump, cfg)

class Option:
    def __init__(self, label, opt_type, default):
        self.opt_type = opt_type
        self.label = label
        self.value = default

    def opt_widget(self, parent):
        if self.opt_type == BOOLEAN:
            self.widget = wx.CheckBox(parent, -1, self.label)
            self.widget.SetValue(self.value)
        elif self.opt_type == TEXTBOX:
            self.widget = wx.Panel(parent)
            #TODO: support textbox options
        return self.widget

class OptionsDialog(wx.Dialog):
    def __init__(self, parent, options):
        wx.Dialog.__init__(self, parent, title="Options")
        self.options = options

        self.options_panel = wx.Panel(self)
        self.confirm_panel = wx.Panel(self)
        
        ok_button = wx.Button(self.confirm_panel, OK, "Ok")
        cancel_button = wx.Button(self.confirm_panel, CANCEL, "Cancel")

        self.Bind(wx.EVT_BUTTON, self.handle_button, ok_button, id=OK)
        self.Bind(wx.EVT_BUTTON, self.handle_button, cancel_button, id=CANCEL)

        widgets = [option.opt_widget(self.options_panel)
                   for option in options.values()]
        options_sizer = wx.BoxSizer(wx.VERTICAL)
        options_sizer.AddMany([(widget) for widget in widgets])
        self.options_panel.SetSizer(options_sizer)

        confirm_sizer = wx.BoxSizer(wx.HORIZONTAL)
        confirm_sizer.AddMany([(ok_button), (cancel_button)])
        self.confirm_panel.SetSizer(confirm_sizer)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.AddMany([(self.options_panel), (self.confirm_panel)])
        self.SetSizer(sizer)

        self.Fit()

    def handle_button(self, event):
        if event.GetId() == OK:
            for option in self.options.values():
                if option.opt_type == BOOLEAN:
                    option.value = option.widget.IsChecked()
                elif option.opt_type == TEXTBOX:
                    #this won't actually work
                    option.value = option.widget.GetValue()
            save_options(self.options)
        self.Destroy()
