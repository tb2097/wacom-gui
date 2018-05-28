# Loads settings on various models of tablets
import xml.dom.minidom
import os

class tabletidentities:
    def __init__(self):
        self.Tablets = []
        self.Tablets.append(tablet("MODEL_PP_0405", "Wacom PenPartner", 0x00))
        self.Tablets.append(tablet("ET_0405", "Wacom Graphire", 0x10))
        self.Tablets.append(tablet("ET_0405", "Wacom Graphire2 4x5", 0x11))
        self.Tablets.append(tablet("ET_0507", "Wacom Graphire2 5x7", 0x12))
        self.Tablets.append(tablet("ET_0405", "Wacom Graphire3 4x5", 0x13))
        self.Tablets.append(tablet("ET_0608", "Wacom Graphire3 6x8", 0x14))
        self.Tablets.append(tablet("CTE_440", "Wacom Graphire4 4x5", 0x15))
        self.Tablets.append(tablet("CTE_640", "Wacom Graphire4 6x8", 0x16))
        self.Tablets.append(tablet("GD_0405-U", "Wacom Intuos 4x5", 0x20))
        self.Tablets.append(tablet("GD_0608-U", "Wacom Intuos 6x8", 0x21))
        self.Tablets.append(tablet("GD_0912-U", "Wacom Intuos 9x12", 0x22))
        self.Tablets.append(tablet("GD_1212-U", "Wacom Intuos 12x12", 0x23))
        self.Tablets.append(tablet("GD_1218-U", "Wacom Intuos 12x18", 0x24))
        self.Tablets.append(tablet("MODEL_PL400",   "Wacom PL400", 0x30))
        self.Tablets.append(tablet("MODEL_PL500",   "Wacom PL500", 0x31))
        self.Tablets.append(tablet("MODEL_PL600",   "Wacom PL600", 0x32))
        self.Tablets.append(tablet("MODEL_PL600SX", "Wacom PL600SX", 0x33))
        self.Tablets.append(tablet("MODEL_PL550",   "Wacom PL550", 0x34))
        self.Tablets.append(tablet("MODEL_PL800",   "Wacom PL800", 0x35))
        self.Tablets.append(tablet("MODEL_PL700",   "Wacom PL700", 0x37))
        self.Tablets.append(tablet("MODEL_PL510",   "Wacom PL510", 0x38))
        self.Tablets.append(tablet("MODEL_DTU710",  "Wacom PL710", 0x39))
        self.Tablets.append(tablet("MODEL_DTF720",  "Wacom DTF720", 0xC0))
        self.Tablets.append(tablet("MODEL_DTF521",  "Wacom DTF521", 0xC4))
        self.Tablets.append(tablet("MODEL_DTU1931", "Wacom DTU1931", 0xC7))
        self.Tablets.append(tablet("XD-0405-U", "Wacom Intuos2 4x5", 0x41))
        self.Tablets.append(tablet("XD-0608-U", "Wacom Intuos2 6x8", 0x42))
        self.Tablets.append(tablet("XD-0912-U", "Wacom Intuos2 9x12", 0x43))
        self.Tablets.append(tablet("XD-1212-U", "Wacom Intuos2 12x12", 0x44 ))
        self.Tablets.append(tablet("XD-1218-U", "Wacom Intuos2 12x18", 0x45))
        self.Tablets.append(tablet("XD-0608-U", "Wacom Intuos2 6x8", 0x47))
        self.Tablets.append(tablet("MODEL-VOL", "Wacom Volito", 0x60))
        self.Tablets.append(tablet("FT-0203-U", "Wacom PenStation", 0x61))
        self.Tablets.append(tablet("CTF-420-U", "Wacom Volito2 4x5", 0x62))
        self.Tablets.append(tablet("CTF-220-U", "Wacom Volito2 2x3", 0x63))
        self.Tablets.append(tablet("CTF-421-U", "Wacom PenPartner2", 0x64))
        self.Tablets.append(tablet("CTF_430-U", "Wacom Bamboo1", 0x69))
        self.Tablets.append(tablet("MTE_450", "Wacom Bamboo", 0x65))
        self.Tablets.append(tablet("CTE_450", "Wacom BambooFun 4x5", 0x17))
        self.Tablets.append(tablet("CTE_650", "Wacom BambooFun 6x8", 0x18))
        self.Tablets.append(tablet("CTE_631", "Wacom Bamboo1 Medium", 0x19))
        self.Tablets.append(tablet("PTU-600", "Wacom Cintiq Partner", 0x03))
        self.Tablets.append(tablet("TPC-090", "Wacom Tablet PC90", 0x90))
        self.Tablets.append(tablet("TPC-093", "Wacom Tablet PC93", 0x93))
        self.Tablets.append(tablet("TPC-09A", "Wacom Tablet PC9A", 0x9A))
        self.Tablets.append(tablet("DTZ-21ux",  "Wacom Cintiq21UX", 0x3F))
        self.Tablets.append(tablet("DTZ-20wsx", "Wacom Cintiq20WSX", 0xC5))
        self.Tablets.append(tablet("DTK-22hd", "Wacom Cintiq 22HD", 0xFA))
        self.Tablets.append(tablet("DTK-1300", "Wacom Cintiq 13HD", 0x304))
        self.Tablets.append(tablet("DTK-1301", "Wacom Cintiq 13HD", 0x305))
        self.Tablets.append(tablet("DTZ-12wx",  "Wacom Cintiq12WX", 0xC6))
        self.Tablets.append(tablet("PTZ-430",   "Wacom Intuos3 4x5", 0xB0))
        self.Tablets.append(tablet("PTZ-630",   "Wacom Intuos3 6x8", 0xB1))
        self.Tablets.append(tablet("PTZ-930",   "Wacom Intuos3 9x12", 0xB2))
        self.Tablets.append(tablet("PTZ-1230",  "Wacom Intuos3 12x12", 0xB3))
        self.Tablets.append(tablet("PTZ-1231W", "Wacom Intuos3 12x19", 0xB4))
        self.Tablets.append(tablet("PTZ-631W",  "Wacom Intuos3 6x11", 0xB5))
        self.Tablets.append(tablet("PTZ-431W",  "Wacom Intuos3 4x6", 0xB7))
        self.Tablets.append(tablet("PTK-440", "Wacom Intuos4 4x6", 0xB8))
        self.Tablets.append(tablet("PTK-640", "Wacom Intuos4 6x9", 0xB9))
        self.Tablets.append(tablet("PTK-840", "Wacom Intuos4 8x13", 0xBA))
        self.Tablets.append(tablet("PTK-1240", "Wacom Intuos4 12x19", 0xBB))
        self.Tablets.append(tablet("PTH-650", "Wacom Intuos5 touch M Pen", 0x27))
        self.Tablets.append(tablet("PTH-651", "Wacom Intuos Pro M Pen", 0x315))
        self.Tablets.append(tablet("PTH-660", "Wacom Intuos Pro M Pen", 0x357))
        self.Tablets.append(tablet("PTH-680", "Wacom Intuos Pro L Pen", 0x358))
        self.Tablets.append(tablet("CTH-460", "Wacom Bamboo Pen 6x4", 0xD1))
        self.Tablets.append(tablet("CTH-661", "Wacom BambooFun 2FG 6x8", 0xD3))
        self.Tablets.append(tablet("CTL-460", "Wacom BambooFun 2FG 4x5", 0xD4))
        self.Tablets.append(tablet("CTH-460K", "Wacom BambooPT 2FG 4x5", 0xD6))
        self.Tablets.append(tablet("DTH-1620", "Wacom Cintiq Pro 16", 0x350))
        self.Tablets.append(tablet("generic", "generic", 0xFF))
		
		#self.Tablets.append(tablet("PTK-540WL", "Wacom Intuos4 Wireless Bluetooth", 0x00)) # Stub, this needs special support
		 
class tablet:
    def __init__(self,Model, Name, ProductId):
        self.Name = Name
        self.Model = Model
        self.ProductId = ProductId
        self.Buttons = []
        self.GraphicWidth = -1

        opPath = os.path.dirname(os.path.realpath(__file__)) 

        try:	# Attempt to load button map		
            XML = xml.dom.minidom.parse(opPath + "/images/pad/"+self.Model+".xml")

        except:
            return
            # Load Custom Pad Descriptions
        try:
            XBase = XML.getElementsByTagName("padsettings")
            self.GraphicWidth = int(XBase[0].attributes["graphicwidth"].value)
            XPlateau = XBase[0].getElementsByTagName("button")
            for item in XPlateau:
                XName = item.attributes["name"].value
                XNumber = item.attributes["number"].value
                XCallsign = item.attributes["callsign"].value
                X1 = item.getElementsByTagName("x1")[0].childNodes[0].data
                Y1 = item.getElementsByTagName("y1")[0].childNodes[0].data
                X2 = item.getElementsByTagName("x2")[0].childNodes[0].data
                Y2 = item.getElementsByTagName("y2")[0].childNodes[0].data
                self.Buttons.append(button(XName, XNumber, XCallsign, int(X1), int(Y1), int(X2), int(Y2)))
        except:
            print "Error loading " + opPath + "/images/pad/" + self.Model + ".xml"

class button:
	def __init__(self, Name, Number, Callsign, X1, Y1, X2, Y2):
		self.Name = Name
		self.Number = Number
		self.Callsign = Callsign
		self.X1 = X1
		self.Y1 = Y1
		self.X2 = X2
		self.Y2 = Y2
