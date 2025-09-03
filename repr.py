from tkinter import *
from interp import *

# de vazut daca pot sa fac widthul maxim din prima la canva
# de rezolvat restul #
# de vazut cu eliberarea de memorie
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
    ErrorLabel.config(text="")
    if not int_str(child):
        ErrorLabel.config(text = "VALOAREA NODULUI INTRODUS NU ESTE NUMAR INTREG")
        ErrorLabel.grid(row = 5, column = 0)
        return False
    if parent == '\0':
        return True
    if not FindNode(root, parent) and FindNode(root, child):
        ErrorLabel.config(text = "NODUL PARINTE " + parent + " NU EXISTA\n" + "NODUL " + child + " DEJA EXISTA IN ARBORE")
        ErrorLabel.grid(row = 5, column = 0)
        return False
    if not FindNode(root, parent):
        ErrorLabel.config(text = "NODUL PARINTE " + parent + " NU EXISTA")
        ErrorLabel.grid(row = 5, column = 0)
        return False
    if FindNode(root, child):
        ErrorLabel.config(text = "NODUL " + child + " DEJA EXISTA IN ARBORE")
        ErrorLabel.grid(row = 5, column = 0)
        return False
    return True

def DestrErrorVar():
    if not ErrorLabel["text"] == "":
        ErrorLabel.grid_forget()
        ErrorLabel.config(text = "")

def UpdateScrollRegion():
    VisTree.config(scrollregion = VisTree.bbox("all"))

def ReSizeCanvas(x, y):
    current_width = VisTree.winfo_width()
    current_height = VisTree.winfo_height()
    
    new_width = current_width
    new_height = current_height
    
    if x + 100 >= current_width:
        new_width = x + 300
    if y + 100 >= current_height:
        new_height = y + 300
    
    VisTree.config(width=new_width, height=new_height)

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
    
# creare main widget
mainWidget = Tk()
mainWidget.title("Vizualizare Arbore Multicai")

#crearea text pentru erori
global ErrorLabel
ErrorLabel = Label(mainWidget, text="", fg="red", font=("Times New Roman", 12, "bold"))

IntroLabel1 = Label(mainWidget, text = "Interfata grafica pentru vizualizarea unui arbore multicai")
IntroLabel1.grid(row = 0, column = 0)

# creare setari initiale pentru radacina

RootLabel = Label(mainWidget, text = "Introdu valoarea nodului radacina")
RootLabel.grid(row = 1, column = 0)

InpValueRoot = Entry(mainWidget)
InpValueRoot.grid(row = 2, column = 0)


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
    VisTree = Canvas(mainWidget, height = 500, width = 500, bg = "grey", scrollregion=(0,0,1000,1000))
    VisTree.grid(row = 7)

    x_scrollbar = Scrollbar(mainWidget, orient=HORIZONTAL, command=lambda *args: VisTree.xview(*args))
    x_scrollbar.grid(row=8, column=0, sticky="ew")

    y_scrollbar = Scrollbar(mainWidget, orient=VERTICAL, command=lambda *args: VisTree.yview(*args))
    y_scrollbar.grid(row=7, column=1, sticky="ns")

    VisTree.config(xscrollcommand = x_scrollbar.set, yscrollcommand = y_scrollbar.set)

    #adaugare nod radacina
    DrawNode(RootValue, '\0')

    #creare setari pentru introducerea primului copil al radacinii
    global IntroLabel2 
    IntroLabel2 = Label(mainWidget, text = "Introdu valoarea primului copil al nodului radacina")
    IntroLabel2.grid(row = 1, column = 0)

    global InpFirstChild 
    InpFirstChild = Entry(mainWidget)
    InpFirstChild.grid(row = 3, column = 0)

    global ButtonFirstChild
    ButtonFirstChild = Button(mainWidget, text = "Apasa", command = ButtonPressFirstChild)
    ButtonFirstChild.grid(row = 4, column = 0)

def ButtonPressFirstChild():
    DestrErrorVar()

    FirstChildValue = InpFirstChild.get().strip()
    #adaugare prim copil
    DrawNode(FirstChildValue, RootValue)

    if not ErrorLabel["text"] == "":
        return
    else:
        IntroLabel2.destroy()
        InpFirstChild.destroy()
        ButtonFirstChild.destroy()

    #crearea setari dupa introducerea radacinii si a primului copil
    IntroLabel3 = Label(mainWidget, text = "Introdu valoarea nodului parinte si nodului copil")
    IntroLabel3.grid(row = 1, column = 0)

    #creare input fiels pt copil-parinte
    global InpParent_var
    global InpChild_var 

    InpParent_var = StringVar()
    InpChild_var = StringVar()

    global InpParent
    global InpChild
    InpParent = Entry(mainWidget, textvariable=InpParent_var)
    InpChild = Entry(mainWidget, textvariable=InpChild_var)

    InpParent.grid(row = 2, column = 0)
    InpChild.grid(row = 3, column = 0)

   # creare butoane pentru info copil-parinte
    ButtonParentChild = Button(mainWidget, text = "Apasa", command = ButtonPressParentChild)
    ButtonParentChild.grid(row = 4, column = 0)

def ButtonPressParentChild():
    DestrErrorVar()

    ChildValue = InpChild.get().strip()
    ParentValue = InpParent.get().strip()

    InpChild_var.set("")
    InpParent_var.set("")

    DrawNode(ChildValue, ParentValue)

ButtonRootValue = Button(mainWidget, text = "Apasa", command = ButtonPressRootValue)
ButtonRootValue.grid(row = 2, column = 1)

#Free(root)
mainWidget.mainloop()