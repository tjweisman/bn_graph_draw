import wx        

OK=0
CANCEL=1

class OptionsDialog(wx.Dialog):
    def __init__(self, parent, infoboxes):
        wx.Dialog.__init__(self, parent, title="Options")

        self.boxes_panel = wx.Panel(self)
        self.confirm_panel = wx.Panel(self)
        
        self.info = infoboxes
        self.boxes = [wx.CheckBox(self.boxes_panel, 
                                  -1, info.name) for info in infoboxes]
        
        for info, box in zip(self.info, self.boxes):
            box.SetValue(info.enabled)


        ok_button = wx.Button(self.confirm_panel, OK, "Ok")
        cancel_button = wx.Button(self.confirm_panel, CANCEL, "Cancel")

        box_sizer = wx.BoxSizer(wx.VERTICAL)
        box_sizer.AddMany([(box) for box in self.boxes])
        self.boxes_panel.SetSizer(box_sizer)

        confirm_sizer = wx.BoxSizer(wx.HORIZONTAL)
        confirm_sizer.AddMany([(ok_button), (cancel_button)])
        self.confirm_panel.SetSizer(confirm_sizer)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.AddMany([(self.boxes_panel), (self.confirm_panel)])
        self.SetSizer(sizer)

        self.Fit()

    def get_enabled(self):
        return [info for box,info in zip(self.boxes, self.info) 
                if box.IsChecked()]
