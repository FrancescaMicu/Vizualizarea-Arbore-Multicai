from tkinter import *
from interp import *
from customtkinter import *

# de vazut daca pot sa fac widthul maxim din prima la canva
# de rezolvat restul #
# design?

#dictionar pentru a retine cati copii are fiecare nod
NodesDet = {} #circle, line, text, coords, childIdx, space


def int_str(value):
    try:
        int(value)
        return True
    except ValueError:
        return False

def ErrorVer(parent, child):
    ErrorLabel.configure(text = "")
    if not int_str(child):
        ErrorLabel.configure(text = "VALOAREA NODULUI INTRODUS NU ESTE NUMĂR ÎNTREG")
        ErrorLabel.grid(row = 5, column = 0, pady = 10)
        return False
    if parent == '\0':
        return True
    if not FindNode(root, parent) and FindNode(root, child):
        ErrorLabel.configure(text = "NODUL PĂRINTE " + parent + " NU EXISTĂ\n" + "NODUL " + child + " DEJA EXISTĂ ÎN ARBORE")
        ErrorLabel.grid(row = 5, column = 0, pady = 10)
        return False
    if not FindNode(root, parent):
        ErrorLabel.configure(text = "NODUL PĂRINTE " + parent + " NU EXISTĂ")
        ErrorLabel.grid(row = 5, column = 0, pady = 10)
        return False
    if FindNode(root, child):
        ErrorLabel.configure(text = "NODUL " + child + " DEJA EXISTĂ ÎN ARBORE")
        ErrorLabel.grid(row = 5, column = 0, pady = 10)
        return False
    return True

def DestrErrorVar():
    if ErrorLabel.cget("text") != "":
        ErrorLabel.grid_forget()
        ErrorLabel.configure(text = "")

def UpdateScrollRegion():
    VisTree.config(scrollregion = VisTree.bbox("all"))

def ReSizeCanvas(ChWidth, ChHeight):
    FrWidth = VisTree.winfo_width()
    FrHeight = VisTree.winfo_height()

    ScrWidth = VisTree.winfo_screenwidth() - 300
    ScrHeight = VisTree.winfo_screenheight() - 200

    #testare width
    if FrWidth >= ScrWidth or ChWidth + 100 < FrWidth:
        NewWidth = FrWidth
    else:
        NewWidth = ChWidth + 150

    #testare height
    if FrHeight >= ScrHeight or ChHeight + 100 < FrHeight:
        NewHeight = FrHeight
    else:
        NewHeight = ChHeight + 150
        
    
    VisTree.config(width = NewWidth, height = NewHeight)

def DrawLine(PaWidth, PaHeight, ChWidth, ChHeight):
    return VisTree.create_line(PaWidth, PaHeight, ChWidth, ChHeight, width = 3)

def DeleteDrawSubTree(parent):
    SubTree = GetSubTree(parent, root)
    for node in SubTree:
        if str(node) in NodesDet:
            VisTree.delete(NodesDet[str(node)]["circle"])
            VisTree.delete(NodesDet[str(node)]["line"])
            VisTree.delete(NodesDet[str(node)]["text"])
            VisTree.delete(NodesDet[str(node)]["space"])


def CalcWidth(PaWidth, ChildIdx, ChildCount, child):
    if "space" not in NodesDet[child]:
        NodesDet[child]["space"] = 110
    sp = NodesDet[child]["space"]
    ChWidth = PaWidth + (ChildIdx - (ChildCount - 1) / 2) * sp
    return ChWidth

def ReDrawSubTree(parent):
    SubTree = GetSubTree(parent, root)
    for i, node in enumerate(SubTree):
        if i == 0:
            ParNode = parent
        else:
            ParNode = FindPar(node, root)

        ChildCount = CountChild(ParNode, root)
        ChildIdx = NodesDet[str(node)]["childIdx"]
        PaWidth, PaHeight = NodesDet[str(ParNode)]["coords"]
        ChHeight = PaHeight + 75

        
        NodeLev = FindLev(str(node), root)
        NrMaxChildLev = DetMaxChildLev(root, NodeLev)
        if NrMaxChildLev:
            NodesDet[str(node)]["space"] = 110 * (NrMaxChildLev - 0.5)

        ChWidth = CalcWidth(PaWidth, ChildIdx, ChildCount, str(node))

        ReSizeCanvas(ChWidth, ChHeight)
        if str(node) not in NodesDet:
            NodesDet[str(node)] = {}
        NodesDet[str(node)]["circle"] = VisTree.create_oval(ChWidth - 25, ChHeight - 25, ChWidth + 25, ChHeight + 25, outline = "black", width = 3, fill = "white")
        NodesDet[str(node)]["text"] = VisTree.create_text(ChWidth, ChHeight, text = str(node), font = ("Times New Roman", 16, "bold"))
        NodesDet[str(node)]["coords"] = (ChWidth, ChHeight)

        NodesDet[str(node)]["line"] = DrawLine(PaWidth, PaHeight + 25, ChWidth, ChHeight - 25)

def DrawNode(child, parent):
    #Verificare daca nodul adaugat e radacina
    if parent == '\0':
        VisTree.update_idletasks()
        cx = VisTree.winfo_width() // 2
        cy = 30

        NodesDet[child] = {}
        NodesDet[child]["coords"] = (cx, cy)
        NodesDet[child]["circle"] = VisTree.create_oval(225, 5, 275, 55, outline = "black", width = 3, fill = "white")
        NodesDet[child]["text"] = VisTree.create_text(250, 30, text = child, font = ("Times New Roman", 16))
        NodesDet[child]["line"] = 0
        NodesDet[child]["childIdx"] = 0
        NodesDet[child]["space"] = 0
    else:
        if not ErrorVer(parent, child):
            return
        if not NewChild(parent, child, root):
            return
        #verificare al catelea copil este
        PaWidth, PaHeight = NodesDet[parent]["coords"]
        ChildCount = CountChild(parent, root)

        NodesDet[child] = {}
        if ChildCount == 1:
            #determinare coordonate copil
            ChHeight = PaHeight + 75
            ChWidth = CalcWidth(PaWidth, 0, ChildCount, child)
            ReSizeCanvas(ChWidth, ChHeight)

            NodesDet[child]["circle"] = VisTree.create_oval(ChWidth - 25, ChHeight - 25, ChWidth + 25, ChHeight + 25, outline = "black", width = 3, fill = "white")
            NodesDet[child]["text"] = VisTree.create_text(ChWidth, ChHeight, text = child, font = ("Times New Roman", 16, "bold"))
            NodesDet[child]["coords"] = (ChWidth, ChHeight)

            NodesDet[child]["line"] = DrawLine(PaWidth, PaHeight + 25, ChWidth, ChHeight - 25)
            NodesDet[child]["childIdx"] = 0
            NodesDet[child]["space"] = 110
        else:
            NodesDet[child]["childIdx"] = CountChild(parent, root) - 1

            NodesDet[child]["circle"] = 0
            NodesDet[child]["text"] = 0
            NodesDet[child]["line"] = 0
            NodesDet[child]["space"] = 110

            DeleteDrawSubTree(RootValue)
            ReDrawSubTree(RootValue)
    UpdateScrollRegion()

def ButtonPressRootValue():
    DestrErrorVar()

    global RootValue
    RootValue = InpValueRoot.get().strip()

    if not ErrorVer('\0', RootValue):
        return
    else:
        RootLabel.destroy()
        InpValueRoot.destroy()
        ButtonRootValue.destroy()

    # creare arbore
    global root
    root = CreateTree(int(RootValue))
    if not root:
        print("Nu s-a putut crea arborele")
        return False

    global VisTree
    RightFrame = CTkFrame(mainWidget, width = 550, height = 600, corner_radius = 15, fg_color = "#CECECE")
    RightFrame.pack(side = "right", fill = "both", expand = True, padx = 10, pady = 10)

    VisTree = Canvas(RightFrame, height = 500, width = 500, bg = "#C0C0C0", scrollregion=(0,0,1000,1000))
    VisTree.grid(row = 7, pady = 10)

    x_scrollbar = CTkScrollbar(RightFrame, orientation = HORIZONTAL, command = lambda *args: VisTree.xview(*args))
    x_scrollbar.grid(row=8, column=0, sticky="ew")

    y_scrollbar = CTkScrollbar(RightFrame, orientation = VERTICAL, command = lambda *args: VisTree.yview(*args))
    y_scrollbar.grid(row=7, column=1, sticky="ns")

    VisTree.config(xscrollcommand = x_scrollbar.set, yscrollcommand = y_scrollbar.set)

    #adaugare nod radacina
    DrawNode(RootValue, '\0')

    #creare setari pentru introducerea primului copil al radacinii
    global IntroLabel2 
    IntroLabel2 = CTkLabel(LeftFrame, text = "Introduceți valoarea"+"\n"+"primului copil"+"\n"+"al nodului rădacină", font = ("Times New Roman", 24))
    IntroLabel2.grid(row = 1, column = 0, pady = 10)

    global InpFirstChild 
    InpFirstChild = CTkEntry(LeftFrame, placeholder_text = "Valoarea nodului copil", width = 300, height = 30, font = ("Times New Roman", 24))
    InpFirstChild.grid(row = 3, column = 0, pady = 10)

    global ButtonFirstChild
    ButtonFirstChild = CTkButton(LeftFrame, text = "Apasă", command = ButtonPressFirstChild, width = 100)
    ButtonFirstChild.grid(row = 4, column = 0, pady = 10)

def ButtonPressFirstChild():
    DestrErrorVar()

    FirstChildValue = InpFirstChild.get().strip()
    #adaugare prim copil
    DrawNode(FirstChildValue, RootValue)

    if ErrorLabel.cget("text") != "":
        return
    else:
        IntroLabel2.destroy()
        InpFirstChild.destroy()
        ButtonFirstChild.destroy()

    #crearea setari dupa introducerea radacinii si a primului copil
    IntroLabel3 = CTkLabel(LeftFrame, text = "Introduceți valoarea"+"\n"+"nodului părinte și"+"\n"+"a nodului copil", font = ("Times New Roman", 24))
    IntroLabel3.grid(row = 1, column = 0, pady = 10)

    #creare input fiels pt copil-parinte
    global InpParent_var
    global InpChild_var 

    global InpParent
    global InpChild
    InpParent = CTkEntry(LeftFrame, placeholder_text = "Valoarea nodului părinte", width = 300, height = 30, font = ("Times New Roman", 24))
    InpChild = CTkEntry(LeftFrame, placeholder_text = "Valoarea nodului copil", width = 300, height = 30, font = ("Times New Roman", 24))

    InpParent_var = InpParent.get().strip()
    InpChild_var = InpChild.get().strip()

    InpParent.grid(row = 2, column = 0, pady = 10)
    InpChild.grid(row = 3, column = 0, pady = 10)

   # creare butoane pentru info copil-parinte
    ButtonParentChild = CTkButton(LeftFrame, text = "Apasă", command = ButtonPressParentChild, width = 100)
    ButtonParentChild.grid(row = 4, column = 0, pady = 10)

def ButtonPressParentChild():
    DestrErrorVar()

    ChildValue = InpChild.get().strip()
    ParentValue = InpParent.get().strip()

    InpChild.delete(0, END)
    InpParent.delete(0, END)

    DrawNode(ChildValue, ParentValue)
    
# creare main widget
mainWidget = CTk()
mainWidget.title("Vizualizare Arbore Multicăi")

set_appearance_mode("system")
set_default_color_theme("dark-blue")

# creare frame=uri
global LeftFrame
LeftFrame = CTkFrame(mainWidget, width = 200, height = 600, corner_radius = 15, fg_color = "#CECECE")
LeftFrame.pack(side = "left", fill = "both", expand = True, padx = 10, pady = 10)

#crearea text pentru erori
global ErrorLabel
ErrorLabel = CTkLabel(LeftFrame, text = "", text_color = "red", font = ("Times New Roman", 26, "bold"))

# IntroLabel = CTkLabel(LeftFrame, text = "Interfață grafică pentru vizualizarea unui arbore multicăi", font = ("Times New Roman", 24))
# IntroLabel.grid(row = 0, column = 0, pady = 10)

# creare setari initiale pentru radacina
root = 0

RootLabel = CTkLabel(LeftFrame, text = "Introduceți valoarea nodului rădacină", font = ("Times New Roman", 24))
RootLabel.grid(row = 1, column = 0, pady = 10)

InpValueRoot = CTkEntry(LeftFrame, placeholder_text = "Valoarea nodului rădacină", width = 300, height = 30, font = ("Times New Roman", 24))
InpValueRoot.grid(row = 2, column = 0, pady = 10)

ButtonRootValue = CTkButton(LeftFrame, text = "Apasă", command = ButtonPressRootValue, width = 100)
ButtonRootValue.grid(row = 2, column = 1, pady = 10)

mainWidget.mainloop()
Free(root)