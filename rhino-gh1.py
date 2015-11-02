import rhinoscriptsyntax as rs
import scriptcontext
import Rhino
import math
import Meier_UI_Utility # This is the module with the UI creation code
import System.Windows.Forms.DialogResult

render_beads = False
zulu_boy = False
zulu_girl = False
zulu_man = False
zulu_woman = False
zulu_red = False
zulu_yellow = False
zulu_blue = False
zulu_green = False
zulu_black = False
zulu_pink = False
zulu_white = False
render_african = False
render_canadian = False
render_indian = False
render_texture = False
render_pattern = False
indian_percent = 0
african_percent = 0
canadian_percent = 0
dialog1 = True
dialog2 = False
id = 0
pattern = ""
color = ""

def AfricanGh(pattern):
 
#Load Grasshopper Plugin as gh
    gh = Rhino.RhinoApp.GetPlugInObject("Grasshopper")
 
#Turn off Redraw
    rs.EnableRedraw(True)


#Values for GH Sliders
    u = 35
    v = 20
 
#Set Sliders Based on Values above
    gh.SetSliderValue("6d29cd90-b5e6-4325-9639-e3322ba5f5ac", u)
    gh.SetSliderValue("90373b1f-1a60-4ce2-8c39-a87388fe0efb", v)

#gh.assigndatatoparameter(818600e1-8da9-449d-a285-2b8a239a5716, )
    srfId = rs.GetObject("Please select surface- texture", rs.filter.surface)
    print (srfId)
    gh.AssignDataToParameter("234d0a6a-dff1-49d0-8f0e-ebcb4e3784ec", srfId)

#srf = gh.GetType(234d0a6a-dff1-49d0-8f0e-ebcb4e3784ec)
#print (srf)
#Run it and Bake it
    gh.OpenDocument ("C:\users\harshit\desktop\culturecad\african bead clean")
    gh.RunSolver("african bead clean")
    baked = gh.BakeDataInObject("21973337-cacb-434f-a2ee-68c725be217e")
    #objectIds = rs.GetObjects(baked)
    
    i = 0
    m = []
    blist = []
    for id in baked:
        blist.append(id)
    while i < v:
        row = []
        j = 0
        while j < u:
            row.append(blist[i+j*v])
            j += 1
        m.append(row)
        i += 1
    i = 0
    print len(blist), len(m), len(m[0])
    
    
    x = 0
    while i <= v-5:
        j = 0
        while j <= u-7:
            if x == 0:
                if pattern == "zulu_boy": unmarried_boy_pattern (m, i, j, True)#married_boy_pattern(m, i, j,True)#
                x = 1
            else:
                if pattern == "zulu_boy": unmarried_boy_pattern (m, i, j, False)#married_boy_pattern(m, i, j,False)
                x = 0
            j += 7
        i += 5
        
def unmarried_girl_pattern(m, row, col):
    
    i = 0
    while i < 4:
        n = 0
        if i == 0: n = 3
        if i == 1: n = 2
        if i == 2: n = 1
        if i == 3: n = 0
        j = 0
        while j < 7:
            if j < n or j >= 7-n:
                if i % 2 == 0:
                    if col+j != 36:
                        sphere = m[row+i][col+j]
                    else:
                        sphere = m[row+i][0]
                    m_index = rs.AddMaterialToObject(sphere)
                    rs.ObjectColorSource(sphere, 2)
                    rs.MaterialColor(m_index, (0,255,0))
                else:
                    if col+j != 36:
                        sphere = m[row+i][col+j]
                    else:
                        sphere = m[row+i][0]
                    m_index = rs.AddMaterialToObject(sphere)
                    rs.ObjectColorSource(sphere, 2)
                    rs.MaterialColor(m_index, (0,0,255))
            else:
                if col+j <= 35:
                    sphere = m[row+i][col+j]
                else:
                    sphere = m[row+i][0]
                m_index = rs.AddMaterialToObject(sphere)
                rs.ObjectColorSource(sphere, 2)
                rs.MaterialColor(m_index, (255,0,0))
            j += 1
        i += 1

def unmarried_boy_pattern(m, row, col, color):

    i = 0
    while i < 4:
        n = 0
        if i == 0: n = 0
        if i == 1: n = 1
        if i == 2: n = 2
        if i == 3: n = 3
        j = 0
        while j < 7:
            if j < n or j >= 7-n:
                if i % 2 == 0:
                    if col+j != 36:
                        sphere = m[row+i][col+j]
                    else:
                        sphere = m[row+i][0]
                    m_index = rs.AddMaterialToObject(sphere)
                    rs.ObjectColorSource(sphere, 2)
                    rs.MaterialColor(m_index, (0,255,0))
                else:
                    if col+j != 36:
                        sphere = m[row+i][col+j]
                    else:
                        sphere = m[row+i][0]
                    m_index = rs.AddMaterialToObject(sphere)
                    rs.ObjectColorSource(sphere, 2)
                    rs.MaterialColor(m_index, (0,0,255))
            else:
                if col+j != 36:
                    sphere = m[row+i][col+j]
                else:
                    sphere = m[row+i][0]
                    
                if color:
                    m_index = rs.AddMaterialToObject(sphere)
                    rs.ObjectColorSource(sphere, 2)
                    rs.MaterialColor(m_index, (255,0,0))
                else:
                    m_index = rs.AddMaterialToObject(sphere)
                    rs.ObjectColorSource(sphere, 2)
                    rs.MaterialColor(m_index, (0,0,0))
                #m_index = rs.AddMaterialToObject(sphere)
                #rs.ObjectColorSource(sphere, 2)
                #rs.MaterialColor(m_index, (255,0,0))
            j += 1
        i += 1
    #add color algo here
    
    
def married_girl_pattern(m, row, col):
    
    i = 0
    while i < 5:
        n = 0
        if i == 0 or i == 4: n = 2
        if i == 1 or i == 3: n = 1
        if i == 2: n = 0
        j = 0
        while j < 5:
            if j < n or j >= 5-n:
                if i % 2 == 0:
                    if col+j != 36:
                        sphere = m[row+i][col+j]
                    else:
                        sphere = m[row+i][0]
                    m_index = rs.AddMaterialToObject(sphere)
                    rs.ObjectColorSource(sphere, 2)
                    rs.MaterialColor(m_index, (0,0,255))
                else:
                    if col+j != 36:
                        sphere = m[row+i][col+j]
                    else:
                        sphere = m[row+i][0]
                    m_index = rs.AddMaterialToObject(sphere)
                    rs.ObjectColorSource(sphere, 2)
                    rs.MaterialColor(m_index, (0,0,255))
            else:
                if col+j != 36:
                    sphere = m[row+i][col+j]
                else:
                    sphere = m[row+i][0]
                m_index = rs.AddMaterialToObject(sphere)
                rs.ObjectColorSource(sphere, 2)
                rs.MaterialColor(m_index, (255,0,0))
            j += 1
        i += 1

def married_boy_pattern(m, row, col, color):
    
    i = 0
    while i < 5:
        n = 0
        if i == 0 or i == 4: n = 0
        if i == 1 or i == 3: n = 1
        if i == 2: n = 2
        j = 0
        while j < 5:
            if j < n or j >= 5-n:
                if i % 2 == 0:
                    if col+j != 36:
                        sphere = m[row+i][col+j]
                    else:
                        sphere = m[row+i][0]
                    m_index = rs.AddMaterialToObject(sphere)
                    rs.ObjectColorSource(sphere, 2)
                    rs.MaterialColor(m_index, (0,0,255))
                else:
                    if col+j != 36:
                        sphere = m[row+i][col+j]
                    else:
                        sphere = m[row+i][0]
                    m_index = rs.AddMaterialToObject(sphere)
                    rs.ObjectColorSource(sphere, 2)
                    rs.MaterialColor(m_index, (0,0,255))
            else:
                if col+j != 36:
                    sphere = m[row+i][col+j]
                else:
                    sphere = m[row+i][0]
                if color:
                    m_index = rs.AddMaterialToObject(sphere)
                    rs.ObjectColorSource(sphere, 2)
                    rs.MaterialColor(m_index, (255,0,0))
                else:
                    m_index = rs.AddMaterialToObject(sphere)
                    rs.ObjectColorSource(sphere, 2)
                    rs.MaterialColor(m_index, (0,0,0))
            j += 1
        i += 1

def MashGh():
 
#Load Grasshopper Plugin as gh
    gh = Rhino.RhinoApp.GetPlugInObject("Grasshopper")
 
#Turn off Redraw
    rs.EnableRedraw(True)
 
#Set Sliders Based on Values above
    gh.SetSliderValue("bb618601-344c-4885-ac65-dd2227c98955", african_percent)

#gh.assigndatatoparameter(818600e1-8da9-449d-a285-2b8a239a5716, )
    srfId1 = rs.GetObject("Please select surface", rs.filter.surface)
    print (srfId1)
    gh.AssignDataToParameter("2e371c11-099a-4ce6-b59f-7b58569d12cd", srfId1)

#srf = gh.GetType(234d0a6a-dff1-49d0-8f0e-ebcb4e3784ec)
#print (srf)
#Run it and Bake it
    gh.OpenDocument ("C:\users\harshit\desktop\mashup_vase_1_for_ui")
    gh.RunSolver("mashup_vase_1_for_ui")
    baked = gh.BakeDataInObject("44bc862e-41e9-42ec-8ac3-a935632112f8")
    baked = gh.BakeDataInObject("9361a92b-bebe-49c0-8ea7-4a03e6ec3707")


def Main():
    # Make the UI object
    ui = CultureControl()
    global dialog1
    if dialog1:
        Rhino.UI.Dialogs.ShowSemiModal(ui.form)
    
class CultureControl():
    def __init__(self):
        # Make a new form (dialog)
        self.form = Meier_UI_Utility.UIForm("Culture-CAD")
        # Accumulate controls for the form
        self.addControls()
        # Layout the controls on the form
        self.form.layoutControls()
    def addControls(self):
        buttonWidth = 85
        # The controls get added to the panel of the form
        p = self.form.panel
        p.addLabel("", "Culture-CAD Tool", (0, 164, 0), True)
        p.addSeparator("sep1", 230, True)
        p.addLabel("", "", (0, 0, 255), True)
        p.addLabel("", "Bead Tool", (0, 0, 255), True)
        p.addLabel("", "Pattern to Represent :", (0, 0, 255), True)
        p.addLabel("", "", (0, 0, 255), True)
        p.addCheckBox("pattern", "Pattern", False, False, self.zuluboy_CheckStateChanged)
        p.addPictureBox("picbox1", "C:\users\harshit\desktop\culturecad\sample_images\zulu_meaning_boy1.png", False)
        p.addCheckBox("pattern", "Pattern", False, False, self.zulugirl_CheckStateChanged)
        p.addPictureBox("picbox1", "C:\users\harshit\desktop\culturecad\sample_images\zulu_meaning_girl1.png", False)
        p.addCheckBox("pattern", "Pattern", False, False, self.zuluman_CheckStateChanged)
        p.addPictureBox("picbox1", "C:\users\harshit\desktop\culturecad\sample_images\zulu_meaning_married_man1.png", False)
        p.addCheckBox("pattern", "Pattern", False, False, self.zuluwoman_CheckStateChanged)
        p.addPictureBox("picbox1", "C:\users\harshit\desktop\culturecad\sample_images\zulu_meaning_married_woman1.png", True)
        p.addLabel("", "", (0, 0, 255), True)
        p.addSeparator("sep1", 230, True)
        p.addLabel("", "", (0, 0, 255), True)
        p.addLabel("", "Choose One Pattern Color", (0, 0, 255), True)
        p.addLabel("", "", (0, 0, 255), True)
        p.addCheckBox("red", "Red - Love", False, True, self.african_CheckStateChanged)
        p.addLabel("", "", (0, 0, 255), True)
        p.addCheckBox("yellow", "Yellow - Wealth", False, True, self.african_CheckStateChanged)
        p.addLabel("", "", (0, 0, 255), True)
        p.addCheckBox("blue", "Blue - Failthfulness", False, True, self.african_CheckStateChanged)
        p.addLabel("", "", (0, 0, 255), True)
        p.addCheckBox("green", "Green - Contentment", False, True, self.african_CheckStateChanged)
        p.addLabel("", "", (0, 0, 255), True)
        p.addCheckBox("black", "Black - Marriage", False, True, self.african_CheckStateChanged)
        p.addLabel("", "", (0, 0, 255), True)
        p.addCheckBox("pink", "Pink - Promise", False, True, self.african_CheckStateChanged)
        p.addLabel("", "", (0, 0, 255), True)
        p.addCheckBox("white", "White - Spiritual Love", False, True, self.african_CheckStateChanged)
        p.addLabel("", "", (0, 0, 255), True)
        #p.addCheckBox("indian", "Indian", False, True, self.indian_CheckStateChanged)
        #p.addCheckBox("canadian", "Native-Canadian", False, True, self.canadian_CheckStateChanged)
        p.addSeparator("sep2", 230, True)
        #p.addCheckBox("africanpattern1", " ", False, True, self.africanpattern1_CheckStateChanged)
        p.addButton("next", "Make!", 100, True, self.make_OnButtonPress)
        p.addLabel("", "", (0, 0, 255), True)
        #p.addComboBox("combo1", ["Choice 0", "Choice 1", "Choice 2"], 0, False, self.combo1_SelectedIndexChanged)
        #p.addButton("OK", "OK", buttonWidth, False, None)
        #p.addButton("Cancel", "Cancel", buttonWidth, False, None)
        
    def zuluboy_CheckStateChanged(self, sender, e):
        try:
            global zulu_boy
            zulu_boy = not zulu_boy
            if zulu_boy : pattern = "zulu_boy"
        except:
            pass
    def zulugirl_CheckStateChanged(self, sender, e):
        try:
            global zulu_girl
            zulu_girl = not zulu_girl
            if zulu_girl: pattern = "zulu_girl"
        except:
            pass
    def zuluman_CheckStateChanged(self, sender, e):
        try:
            global zulu_man
            zulu_man = not zulu_man
            if zulu_man: pattern = "zulu_man"
        except:
            pass
    def zuluwoman_CheckStateChanged(self, sender, e):
        try:
            global zulu_woman
            zulu_woman = not zulu_woman
            if zulu_woman: pattern = "zulu_woman"
        except:
            pass
    
    def pattern_CheckStateChanged(self, sender, e):
        try:
            global zulu_girl
            zulu_girl = not zulu_girl
        except:
            pass
        
    def african_CheckStateChanged(self, sender, e):
        try:
            global render_african
            render_african = not render_african
        except:
            pass
            
    def indian_CheckStateChanged(self, sender, e):
        try:
            global render_indian
            render_indian = not render_indian
        except:
            pass
            
    def canadian_CheckStateChanged(self, sender, e):
        try:
            global render_canadian
            render_canadian = not render_canadian
        except:
            pass
     
    def make_OnButtonPress(self, sender, e):
        print ("reached")
        #if render_african and render_texture:
            #print ("bead")
        AfricanGh(pattern)
        #ui2 = CultureControl2()
        #dialog2 = True
        #if dialog2:
            #Rhino.UI.Dialogs.ShowSemiModal(ui2.form)
            #dialog1 = False

class CultureControl2():
    def __init__(self):
        # Make a new form (dialog)
        self.form = Meier_UI_Utility.UIForm("Culture-CAD") 
        # Accumulate controls for the form
        self.addControls2()
        # Layout the controls on the form
        #self.form.Width = 
        self.form.layoutControls()
    def addControls2(self):
        p = self.form.panel
        #p.addCheckBox("africanpattern1", " ", False, True, self.africanpattern1_CheckStateChanged)
        p.addLabel("", "", None, False)
        p.addCheckBox("pattern", "Pattern", False, False, self.pattern_CheckStateChanged)
        p.addPictureBox("picbox1", "paisley.png", False)
        p.addCheckBox("pattern", "Pattern", False, False, self.pattern_CheckStateChanged)
        p.addPictureBox("picbox1", "paisley.png", False)
        p.addCheckBox("pattern", "Pattern", False, False, self.pattern_CheckStateChanged)
        p.addPictureBox("picbox1", "paisley.png", False)
        p.addCheckBox("pattern", "Pattern", False, False, self.pattern_CheckStateChanged)
        p.addPictureBox("picbox1", "paisley.png", False)
        p.addPictureBox("picbox1", "africa_texture parts 1.png", True)
        p.addLabel("", "Style of Representation :", (0, 0, 255), True)
        p.addLabel("", "", (0, 0, 255), True)
        p.addCheckBox("pattern", "Pattern", False, True, self.pattern_CheckStateChanged)
        p.addCheckBox("texture", "Texture", False, True, self.texture_CheckStateChanged)
        p.addSeparator("sep3", 230, True)
        p.addLabel("", "", (0, 0, 255), True)
        p.addLabel("", "Percentage of Representation :", (0, 0, 255), True)
        p.addLabel("", "", (0, 0, 255), True)
        p.addLabel("", "Indian Culture %: ", None, False)
        p.addLabel("", "Value: ", None, False)
        p.addReadonlyText("indian%", "50", 100, True)
        p.addTrackBar("Indian Culture %", 0, 100, 10, 2, 10, 50, 150, True, self.indianpercent_OnValueChange)
        p.addLabel("", "African Culture %: ", None, False)
        p.addLabel("", "Value: ", None, False)
        p.addReadonlyText("african%", "50", 100, True)
        p.addTrackBar("African Culture %", 0, 100, 10, 2, 1, 50, 150, True, self.africanpercent_OnValueChange)
        p.addLabel("", "Canadian Culture %: ", None, False)
        p.addLabel("", "Value: ", None, False)
        p.addReadonlyText("canadian%", "50", 100, True)
        p.addTrackBar("Canadian Culture %", 0, 100, 10, 2, 1, 50, 150, True, self.canadianpercent_OnValueChange)
        p.addSeparator("sep4", 230, True)
        p.addLabel("", "", (0, 0, 255), True)
        p.addButton("render", "Render", 100, True, self.render_OnButtonPress)
        p.addLabel("", "", (0, 0, 255), True)
        
    def texture_CheckStateChanged(self, sender, e):
        try:
            global render_texture
            render_texture = not render_texture
            #call pattern_checkStateChanged here
        except:
            pass
            
    def pattern_CheckStateChanged(self, sender, e):
        try:
            global render_pattern
            render_pattern = not render_pattern
            #call texture_checkStateChanged here
        except:
            pass

    def indianpercent_OnValueChange(self, sender, e):
        try:
            global indian_percent
            indian_percent = sender.Value
            #if render_indian == False:
                #indian_percent = 0
            c = self.form.panel.Controls.Find("indian%", True)[0]
            c.Text = str(indian_percent)
        except:
            pass
            
    def africanpercent_OnValueChange(self, sender, e):
        try:
            global african_percent
            african_percent = sender.Value
            #if render_african == False:
                #african_percent = 0
            
            c = self.form.panel.Controls.Find("african%", True)[0]
            c.Text = str(african_percent)
            if render_canadian:
                c = self.form.panel.Controls.Find("canadian%", True)[0]
                c.Text = str(100 - african_percent)
                d = self.form.panel.Controls.Find("Canadian Culture %", True)[0]
                d.Value = (100 - african_percent)
        except:
            pass
            
    def canadianpercent_OnValueChange(self, sender, e):
        try:
            global canadian_percent
            canadian_percent = sender.Value
            #if render_canadian == False:
                #canadian_percent = 0
            c = self.form.panel.Controls.Find("canadian%", True)[0]
            c.Text = str(canadian_percent)
            if render_african:
                c = self.form.panel.Controls.Find("african%", True)[0]
                c.Text = str(100 - canadian_percent)
                d = self.form.panel.Controls.Find("African Culture %", True)[0]
                d.Value = (100 - canadian_percent)
        except:
            pass
    def make_OnButtonPress(self, sender, e):
        print ("reached")
        if render_beads and render_:
            print ("bead")
            AfricanGh()
        if render_canadian and render_african and render_pattern:
            MashGh()
            #rs.MessageBox("Two numbers are relatively prime if they have no common factors", 0, "Help")
        
        
if( __name__ == "__main__" ):
    Main()