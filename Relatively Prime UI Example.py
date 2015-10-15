import rhinoscriptsyntax as rs
import Rhino
import Meier_UI_Utility # This is the module with the UI creation code
import System.Windows.Forms.DialogResult

# 
# Relatively Prime UI Example
# by Mark Meier
# Please see my blog post for details at:
# http://mkmra2.blogspot.com/2012/12/creating-graphical-user-interfaces-with.html
# 

# Brings up a small UI to let the user compare two numbers to see if they
# are "relatively prime" (that is they have no common factors other than 1).  
def Main():
    # Construct the data the UI will change
    data = UIData()
    # Make the UI object and pass it the data to change
    ui = RelativelyPrimeUI(data)
    # Show the dialog from the UI class
    result = Rhino.UI.Dialogs.ShowSemiModal(ui.form)
    # Check the result
    if (result == System.Windows.Forms.DialogResult.OK): print "OK"
    else: print "Cancel"

# Holds the data the UI will manipulate
class UIData():
    def __init__(self):
        self.a = 11
        self.b = 4

#Creates the UI form, adds controls, and lays them out on the form
class RelativelyPrimeUI():
    def __init__(self, data):
        # Holds the data the UI controls update
        self.data = data
        # Make a new form (dialog)
        self.form = Meier_UI_Utility.UIForm("Relatively Prime UI Example") 
        # Accumulate controls for the form
        self.addControls()
        # Layout the controls on the form
        self.form.layoutControls() 
    
    def addControls(self):
        buttonWidth = 85
        # The controls get added to the panel of the form
        p = self.form.panel
        # Add the controls we need
        p.addLabel("", "A:", None, False)
        p.addNumericUpDown("a", 1, 50, 1, 0, self.data.a, 80, True, self.A_OnValueChange)
        p.addLabel("", "B:", None, False)
        p.addNumericUpDown("b", 1, 50, 1, 0, self.data.b, 80, True, self.B_OnValueChange)
        p.addLabel("", "Relatively Prime?", None, False)
        p.addReadonlyText("readOnlyResult", "Yes", 172, True)
        p.addButton("OK", "OK", buttonWidth, False, None)
        p.addButton("Cancel", "Cancel", buttonWidth, False, None)
        p.addButton("Help", "Help", buttonWidth, False, self.Help_OnButtonPress)
    
    def UpdateUI(self):
        # Find the read-only text field control so we can update it
        # (It won't be found if the UI is not finished building)
        try: 
            c = self.form.panel.Controls.Find("readOnlyResult", True)[0]
            if (RelativelyPrime(self.data.a, self.data.b)):
                c.Text = "Yes"
            else:
                c.Text = "No, common factor was " + str(HighestCommonFactor(self.data.a, self.data.b))
        except: 
            pass
    
    def A_OnValueChange(self, sender, e):
        self.data.a = sender.Value
        self.UpdateUI()
    
    def B_OnValueChange(self, sender, e):
        self.data.b = sender.Value
        self.UpdateUI()
    
    def Help_OnButtonPress(self, sender, e):
        rs.MessageBox("Two numbers are relatively prime if they have no common factors", 0, "Help")

# Determine if the two numbers passed are relatively prime (have no common factors)
def RelativelyPrime(a, b): # Assumes a, b > 0
    if (HighestCommonFactor(a, b) == 1): return True
    return False

# Returns the highest common factor between the two numbers passed
def HighestCommonFactor(a, b):
    while True:
        temp = a%b;
        if (temp == 0): return b
        a = b;
        b = temp;

# Execute it...
if( __name__ == "__main__" ):
    Main()
