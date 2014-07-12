import wx, anydbm

OK=0
CANCEL=1

BOOLEAN=0
TEXTBOX=1

def setup_options(frame):
    for key, infobox in frame.infoboxes.iteritems():
        frame.options[key] = Option(infobox.name, BOOLEAN, True)

    frame.options["mathematica"] = Option(
        "Mathematica Output", BOOLEAN, False)

    #load defaults
    load_options(frame.options)

def load_options(options):
    #load an options file, if there is one
    db = anydbm.open('config', 'c')
    for key, option in options.iteritems():
        try:
            val = db[key]
            if option.opt_type == BOOLEAN:
                option.value = (val == "True")
            else:
                option.value = db[key]
        except KeyError as e:
            pass
    db.close()

def save_options(options):
    db = anydbm.open('config', 'c')
    for key, option in options.iteritems():
        if option.opt_type == BOOLEAN:
            db[key] = "True" if option.value else "False"
        else:
            db[key] = option.value
    db.close()

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
