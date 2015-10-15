import rhinoscriptsyntax as rs
import Rhino
import Meier_UI_Utility # This is the module with the UI creation code

# 
# Circle UI Example
# by Mark Meier
# Please see my blog post for details at:
# http://mkmra2.blogspot.com/2012/12/creating-graphical-user-interfaces-with.html
# 

# Brings up a minimal UI to let the user enter the radius of a circle.
# When the dialog is closed the circle is created. 
def Main():
    # Make the UI object
    ui = CircleUI()
    # Show the dialog from the UI class
    Rhino.UI.Dialogs.ShowSemiModal(ui.form)
    # User has exited the dialog - add the circle
    rs.AddCircle(rs.WorldXYPlane(), ui.radius)

#Creates the UI form, adds controls, and lays them out on the form
class CircleUI():
    def __init__(self):
        # Holds the radius value the UI updates. The default will be 10.
        self.radius = 10.0
        # Make a new form (dialog)
        self.form = Meier_UI_Utility.UIForm("Circle UI Example") 
        # Accumulate controls for the form using "addXYZ.." methods
        self.form.panel.addLabel("", "Radius:", None, False)
        self.form.panel.addNumericUpDown("", 1, 50, 1, 2, self.radius, 80, \
            True, self.Radius_OnValueChange)
        # Layout the controls on the form
        self.form.layoutControls() 
    
    # This is called when the radius value changes. Store the changed value. 
    def Radius_OnValueChange(self, sender, e):
        self.radius = sender.Value

# Execute it...
if( __name__ == "__main__" ):
    Main()
