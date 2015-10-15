import rhinoscriptsyntax as rs
import Rhino
import Meier_UI_Utility
import random

# 
# All Controls UI Example
# by Mark Meier
# Please see my blog post for details at:
# http://mkmra2.blogspot.com/2012/12/creating-graphical-user-interfaces-with.html
# 
def Main():
    # Make the UI object
    ui = AllControlExample()
    # Show the dialog from the UI class
    Rhino.UI.Dialogs.ShowSemiModal(ui.form)

# This is just a class to test all the UI controls
class AllControlExample():
    def __init__(self):
        # Make a new form (dialog)
        self.form = Meier_UI_Utility.UIForm("All Controls UI Example") 
        # Accumulate controls for the form
        self.addControls()
        # Layout the controls on the form
        self.form.layoutControls() 
    
    # Add each control to an accumulated list of controls
    def addControls(self):
        # The controls get added to the panel of the form
        
        p = self.form.panel
        p.addLabel("", "A Label", None, True)
        p.addLabel("", "A Label can be any color", (255, 16, 0), True)
        p.addLinkLabel("", "A Link Label", "http://blog.rhino3d.com/", True, None)
        p.addTextBox("fileTextbox", "Sample TextBox", 150, True, self.textbox1_TextChanged)
        p.addReadonlyText("readonly1", "Read-Only TextBox", 150, True)
        p.addCheckBox("check1", "Enable Button Below", True, True, self.check1_CheckStateChanged)
        p.addButton("button1", "Press Me", 100, True, self.button1_OnButtonPress)
        p.addComboBox("combo1", ["Choice 0", "Choice 1", "Choice 2"], 0, False, self.combo1_SelectedIndexChanged)
        p.addLabel("combo1Label", "", None, True)
        p.addLabel("", "A Separator is to my right", (0, 0, 255), False)
        p.addSeparator("sep1", 230, True)
        p.addLabel("", "", None, True) # An empty label can be used to create space vertically
        p.addLabel("", "NumericUpDn: ", None, False)
        p.addNumericUpDown("num1", 0, 100, 1, 2, 1, 80, False, self.num1_OnValueChange)
        p.addLabel("num1Label", "", None, True) # Updates to show the value of "num1"
        p.addLabel("", "Trackbar: ", None, False)
        p.addTrackBar("trackBar1", 0, 10, 1, 2, 1, 5, 150, False, self.trackBar1_OnValueChange)
        p.addLabel("", "Value: ", None, False)
        p.addReadonlyText("readonlyTextbox", "5", 50, True)
        p.addLabel("", "A PictureBox is to my right", (0, 128, 64), False)
        p.addPictureBox("picbox1", "./SamplePicture.jpg", True)
    
    # ====================== Delegates =====================
    # Called when the text changes in the box (every keypress)
    def textbox1_TextChanged(self, sender, e):
        text = sender.Text
        print text # Print it to the python editor Output window
    
    # Called when the box is checked or unchecked
    def check1_CheckStateChanged(self, sender, e):
        try:
            c = self.form.panel.Controls.Find("button1", True)[0]
            c.Enabled = sender.Checked
        except:
            pass
    
    # Called when a selection is made from the combobox
    def combo1_SelectedIndexChanged(self, sender, e):
        index = sender.SelectedIndex # 0 based index of choice
        item = sender.SelectedItem # Text of choice
        try:
            c = self.form.panel.Controls.Find("combo1Label", True)[0]
            c.Text = "Index="+str(index)+", Item="+item
        except:
            pass
    
    # Called when the button is pressed
    def button1_OnButtonPress(self, sender, e):
        sender.Text = random.sample(("Press Me", "Hit Me", "Click Me", "Push Me", "Depress Me", "Tap Me"), 1)[0]
    
    # Called when the value is changed
    def num1_OnValueChange(self, sender, e):
        value = sender.Value.ToString()
        try:
            c = self.form.panel.Controls.Find("num1Label", True)[0]
            c.Text = "Value="+str(value)
        except:
            pass
    
    # Called when the value changes
    def trackBar1_OnValueChange(self, sender, e):
        try:
            c = self.form.panel.Controls.Find("readonlyTextbox", True)[0]
            c.Text = str(sender.Value)
        except:
            pass

# Execute it...
if( __name__ == "__main__" ):
    Main()
