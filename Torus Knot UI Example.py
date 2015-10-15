import rhinoscriptsyntax as rs
import scriptcontext
import Rhino
import math
import Meier_UI_Utility # This is the module with the UI creation code
import System.Windows.Forms.DialogResult

# 
# Torus Knot UI Example
# by Mark Meier
# Please see my blog post for details at:
# http://mkmra2.blogspot.com/2012/12/creating-graphical-user-interfaces-with.html
# 
def Main():
    data = TorusKnotData()
    ui = TorusKnotUI(data)
    controller = FormController(ui)
    ui.ValueChangeCallback(data) # Draw the intial knot
    result = Rhino.UI.Dialogs.ShowSemiModal(ui.form)
    if (result == System.Windows.Forms.DialogResult.OK):
        controller.AddCurveToDocument()

class TorusKnotData():
    def __init__(self):
        # The (p,q)-torus knot winds q times around a circle in the interior 
        # of the torus, and p times around its axis of rotational symmetry. 
        # If p and q are not relatively prime (they have common factors), 
        # then a simpler loop is generated.
        self.p = 2
        self.q = 3
        # This is number of CVs in the knot curve
        self.pathPointCount = 30
        # Path Z scale factor
        self.zScale = 1.0
        # Number of points in the cross section
        self.crossSecPointCount = 4
        # Radius of the cross section
        self.crossSecRadius = 0.4
        # Determines if the cross section is a polyline or a smooth (degree 3) curve
        self.smoothCrossSec = False
        # Rotation of the cross section
        self.crossSecRotation = 0.0
        # Booleans for what to output
        self.outputRail = False
        self.outputCrossSec = False
        self.outputSurface = True

def TorusKnotVerts(p, q, res, zScale):
    # Determine if we need to loop less because of non coprime p and q
    upLimit = 2.0*math.pi
    P = int(p); Q = int(q)
    hcf = HighestCommonFactor(P, Q)
    if (hcf != 1):
        upLimit /= hcf
    
    verts = []
    roundTol = 0.01 # Fudge factor to make sure loop closes
    tStep = math.pi/(res/2.0)
    for t in rs.frange(0.0, upLimit+roundTol, tStep):
        r = math.cos(q*t)+2.0
        x = r*math.cos(p*t)
        y = r*math.sin(p*t)
        z = -math.sin(q*t)*2.0
        z *= zScale
        pt = Rhino.Geometry.Point3d(x, y, z)
        verts.append(pt)
    return verts

# Determine if the two numbers passed are relatively prime (have no common factors)
def RelativelyPrime(a, b): # Assumes a, b > 0
    if (HighestCommonFactor(a, b) == 1): return True
    return False
        
def HighestCommonFactor(a, b):
    while True:
        temp = a%b;
        if (temp == 0): return b
        a = b;
        b = temp;

def GenerateCrossSection(sectionPoints, radius, rotation, smooth, curve, samples, p, q):
    points = []
    avoidRoundoff = 0.01
    for angle in rs.frange(0.0, 360.0+avoidRoundoff, 360.0/sectionPoints):
        points.append(rs.Polar((0.0, 0.0, 0.0), angle, radius))
    
    rotXform = rs.XformRotation2(rotation, (0, 0, 1), (0, 0, 0))
    points = rs.PointArrayTransform(points, rotXform)
    
    t = curve.Domain[0]
    crossSections = []
    curveCurvature = curve.CurvatureAt(t)
    crossSectionPlane = None
    if not curveCurvature:
        crvPoint = curve.PointAt(t)
        crvTangent = curve.TangentAt(t)
        crvPerp = (0,0,1)
        crvNormal = Rhino.Geometry.Vector3d.CrossProduct(crvTangent, crvPerp)
        crossSectionPlane = Rhino.Geometry.Plane(crvPoint, crvPerp, crvNormal)
    else:
        crvPoint = curve.PointAt(t)
        crvTangent = curve.TangentAt(t)
        crvPerp = curve.CurvatureAt(t)
        crvPerp.Unitize
        crvNormal = Rhino.Geometry.Vector3d.CrossProduct(crvTangent, crvPerp)
        crossSectionPlane = Rhino.Geometry.Plane(crvPoint, crvPerp, crvNormal)
    if crossSectionPlane:
        xform = rs.XformChangeBasis(crossSectionPlane, rs.WorldXYPlane())
        sectionVerts = rs.PointArrayTransform(points, xform)
        if (smooth): # Degree 3 curve to smooth it
            sectionCurve = Rhino.Geometry.Curve.CreateControlPointCurve(sectionVerts, 3)
        else: # Degree 1 curve (polyline)
            sectionCurve = Rhino.Geometry.Curve.CreateControlPointCurve(sectionVerts, 1)
        crossSection = rs.coercecurve(sectionCurve)
    return crossSection

#============================= Winform UI Code ===========================
class TorusKnotUI():
    def __init__(self, data):
        self.ValueChangeCallback = None
        self.data = data # Store the data passed so we can update it from the UI
        self.form = Meier_UI_Utility.UIForm("Torus Knot Maker") # Make a new form
        self.addControls() # Accumulate controls for the form
        self.form.layoutControls() # Layout the controls on the form
    
    # Add each control
    def addControls(self):
        updnWidth = 80
        buttonWidth = 105
        
        p = self.form.panel
        
        p.addLabel("", "By Mark Meier, Version 1.0", None, True)
        p.addLinkLabel("", "Online Help", "http://mkmra2.blogspot.com/2012/12/torus-knot-maker.html", True, None)
        p.addLabel("", "", None, True)
        
        p.addLabel("", "Path Curve Options", (0, 0, 255), False)
        p.addSeparator("", 215, True)
        p.addLabel("", "P:", None, False)
        p.addNumericUpDown("P", 2, 32, 1, 0, self.data.p, updnWidth, False, self.P_OnValueChange)
        p.addLabel("", "Q:", None, False)
        p.addNumericUpDown("Q", 2, 32, 1, 0, self.data.q, updnWidth, True, self.Q_OnValueChange)
        p.addLabel("", "Number of Points:", None, False)
        p.addNumericUpDown("R", 16, 64, 2, 0, self.data.pathPointCount, updnWidth, True, self.R_OnValueChange)
        p.addLabel("", "Z Scale Factor:", None, False)
        p.addNumericUpDown("Z", 0.5, 4.0, 0.1, 1, self.data.zScale, updnWidth, True, self.Z_OnValueChange)
        
        p.addLabel("", "Section Curve Options", (0, 0, 255), False)
        p.addSeparator("", 200, True)
        p.addCheckBox("", "Smooth", self.data.smoothCrossSec, True, self.SmoothCrossSec_CheckStateChanged)
        p.addLabel("", "Radius:", None, False)
        p.addNumericUpDown("crossSecRadius", 0.1, 1.0, 0.1, 2, self.data.crossSecRadius, updnWidth, False, self.Section_OnValueChange)
        p.addLabel("", "Rotation:", None, False)
        p.addNumericUpDown("crossSecRotation", 0, 360, 10, 1, self.data.crossSecRotation, updnWidth, True, self.Rotation_OnValueChange)
        p.addLabel("", "Number of Points:", None, False)
        p.addNumericUpDown("", 3, 16, 1, 0, self.data.crossSecPointCount, updnWidth, True, self.PointCount_OnValueChange)
        
        p.addLabel("", "Output Options", (0, 0, 255), False)
        p.addSeparator("", 235, True)
        p.addCheckBox("", "Path Curve", self.data.outputRail, False, self.OutputRail_CheckStateChanged)
        p.addCheckBox("", "Section Curve", self.data.outputCrossSec, False, self.OutputCrossSec_CheckStateChanged)
        p.addCheckBox("", "Surface", self.data.outputSurface, True, self.DrawSweep_CheckStateChanged)
        
        p.addButton("OK", "OK", buttonWidth, False, None)
        p.addButton("Cancel", "Cancel", buttonWidth, False, None)
    
    # Called by the interactive redraw code to store a callback
    # which gets called to update the path, section, and surface
    # geometry after a value has changed in the UI. 
    def SetValueChangedCallback(self, callback):
        self.ValueChangeCallback = callback
    
    # ===================== Delegates =====================
    def P_OnValueChange(self, sender, e):
        self.data.p = sender.Value
        if (self.ValueChangeCallback != None):
            self.ValueChangeCallback(self.data)
    
    def Q_OnValueChange(self, sender, e):
        self.data.q = sender.Value
        if (self.ValueChangeCallback != None):
            self.ValueChangeCallback(self.data)
    
    def R_OnValueChange(self, sender, e):
        self.data.pathPointCount = sender.Value
        if (self.ValueChangeCallback != None):
            self.ValueChangeCallback(self.data)
    
    def Z_OnValueChange(self, sender, e):
        self.data.zScale = sender.Value
        if (self.ValueChangeCallback != None):
            self.ValueChangeCallback(self.data)
    
    def PointCount_OnValueChange(self, sender, e):
        self.data.crossSecPointCount = sender.Value
        if (self.ValueChangeCallback != None):
            self.ValueChangeCallback(self.data)
    
    def DrawSweep_CheckStateChanged(self, sender, e):
        self.data.outputSurface = sender.Checked
        if (self.ValueChangeCallback != None):
            self.ValueChangeCallback(self.data)
    
    def Section_OnValueChange(self, sender, e):
        self.data.crossSecRadius = sender.Value
        if (self.ValueChangeCallback != None):
            self.ValueChangeCallback(self.data)
    
    def Rotation_OnValueChange(self, sender, e):
        self.data.crossSecRotation = sender.Value
        if (self.ValueChangeCallback != None):
            self.ValueChangeCallback(self.data)
    
    def SmoothCrossSec_CheckStateChanged(self, sender, e):
        self.data.smoothCrossSec = sender.Checked
        if (self.ValueChangeCallback != None):
            self.ValueChangeCallback(self.data)
    
    def OutputCrossSec_CheckStateChanged(self, sender, e):
        self.data.outputCrossSec = sender.Checked
        if (self.ValueChangeCallback != None):
            self.ValueChangeCallback(self.data)
    
    def OutputRail_CheckStateChanged(self, sender, e):
        self.data.outputRail = sender.Checked
        if (self.ValueChangeCallback != None):
            self.ValueChangeCallback(self.data)

# ======================== Interactive Redraw Code =========================
class FormController():
    def __init__(self, UI):
        self.railCurve = None
        self.railCurveBBox = None
        self.crossSection = None
        self.surface = None
        self.surfaceBBox = None
        self.data = UI.data # Store the properties of the knot
        UI.SetValueChangedCallback(self.UpdateGeometry)
        Rhino.Display.DisplayPipeline.CalculateBoundingBox += self.OnCalcBoundingBox
        Rhino.Display.DisplayPipeline.DrawForeground += self.OnDrawForeground
        UI.form.FormClosed += self.OnFormClosed
    
    def OnFormClosed(self, sender, e):
        Rhino.Display.DisplayPipeline.DrawForeground -= self.OnDrawForeground
        Rhino.Display.DisplayPipeline.CalculateBoundingBox -= self.OnCalcBoundingBox
        scriptcontext.doc.Views.Redraw()
    
    def OnDrawForeground(self, sender, e):
        railColor = System.Drawing.Color.Red
        sectionColor = System.Drawing.Color.Red
        surfaceColor = System.Drawing.Color.Blue
        if (self.data.outputRail):
            e.Display.DrawCurve(self.railCurve, railColor, 1)
        if (self.data.outputCrossSec):
            e.Display.DrawCurve(self.crossSection, sectionColor, 1)
        if (self.data.outputSurface):
            e.Display.DrawBrepWires(self.surface, surfaceColor, 1)
    
    def OnCalcBoundingBox(self, sender, e):
        if (self.railCurveBBox != None):
            e.IncludeBoundingBox(self.railCurveBBox)
            if (self.surface != None):
                e.IncludeBoundingBox(self.surfaceBBox)
    
    def UpdateGeometry(self, data):
        self.surface = None
        self.surfaceBBox = None
        tempVerts = TorusKnotVerts(data.p, data.q, data.pathPointCount, data.zScale)
        self.railCurve = Rhino.Geometry.Curve.CreateControlPointCurve(tempVerts, 3)
        self.railCurveBBox = self.railCurve.GetBoundingBox(False)
        rail = rs.coercecurve(self.railCurve)
        # Generate a section curve at the start of the rail
        self.crossSection = GenerateCrossSection(data.crossSecPointCount, data.crossSecRadius, data.crossSecRotation, data.smoothCrossSec, self.railCurve, data.pathPointCount, data.p, data.q)
        if (data.outputSurface):
            # Sweep it out about the rail curve
            tolerance = scriptcontext.doc.ModelAbsoluteTolerance
            breps = Rhino.Geometry.Brep.CreateFromSweep(rail, self.crossSection, rail.IsClosed, tolerance)
            self.surface = breps[0]
            self.surfaceBBox = self.surface.GetBoundingBox(False)
        scriptcontext.doc.Views.Redraw()
    
    def AddCurveToDocument(self):
        if (self.surface):
            scriptcontext.doc.Objects.AddBrep(self.surface)
        if (self.data.outputCrossSec):
            scriptcontext.doc.Objects.AddCurve(self.crossSection)
        if (self.data.outputRail):
            scriptcontext.doc.Objects.AddCurve(self.railCurve)
        scriptcontext.doc.Views.Redraw()

# Execute it...
if( __name__ == "__main__" ):
    Main()
