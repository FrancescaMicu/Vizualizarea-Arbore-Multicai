from tkinter import *
from interp import *

# de rezolvat problema cu extinderea ecranului pentru nodurile depasesc ecranul
# si pentru canddoua noduri sunt foarte apropiate si se asemileaza una pe alta;
# sa dispara numerele din casetele de input cand se apasa butonul
# de afisat mesajele de erori pe widget
# de rezolvat restul #
# de vazut cu eliberarea de memorie
# design?


#dictionar pentru a retine cati copii are fiecare nod
NodesDet = {} #circle, line, text, coords, childIdx

def DrawLine(PaWidth, PaHeight, ChWidth, ChHeight):
    return VisTree.create_line(PaWidth, PaHeight, ChWidth, ChHeight, width = 3)

def DeleteDrawSubTree(parent):
    SubTree = GetSubTree(parent, root)
    for node in SubTree:
        if str(node) in NodesDet:
            VisTree.delete(NodesDet[str(node)]["circle"])
            VisTree.delete(NodesDet[str(node)]["line"])
            VisTree.delete(NodesDet[str(node)]["text"])

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
        ChWidth = PaWidth + (ChildIdx - (ChildCount - 1)/2) * 110
        if str(node) not in NodesDet:
            NodesDet[str(node)] = {}
        NodesDet[str(node)]["circle"] = VisTree.create_oval(ChWidth - 25, ChHeight - 25, ChWidth + 25, ChHeight + 25, outline = "black", width = 3, fill = "white")
        NodesDet[str(node)]["text"] = VisTree.create_text(ChWidth, ChHeight, text = str(node), font = ("Times New Roman", 16, "bold"))
        NodesDet[str(node)]["coords"] = (ChWidth, ChHeight)

        NodesDet[str(node)]["line"] = DrawLine(PaWidth, PaHeight + 25, ChWidth, ChHeight - 25)

def DrawNode(child, parent):
    #Verificare daca nodul adaugat e radacina
    if parent == '\0':
        NodesDet[child] = {}
        NodesDet[child]["coords"] = (250, 30)
        NodesDet[child]["circle"] = VisTree.create_oval(225, 5, 275, 55, outline = "black", width = 3, fill = "white")
        NodesDet[child]["text"] = VisTree.create_text(250, 30, text = child, font = ("Times New Roman", 16))
        NodesDet[child]["line"] = 0
        NodesDet[child]["childIdx"] = 0
    else:
        if not NewChild(parent, child, root):
            return
        #verificare al catelea copil este
        PaWidth, PaHeight = NodesDet[parent]["coords"]
        ChildCount = CountChild(parent, root)

        NodesDet[child] = {}
        if ChildCount == 1:
            #determinare coordonate copil
            ChHeight = PaHeight + 75
            ChWidth = PaWidth + (ChildCount - 1)/2 * 110

            NodesDet[child]["circle"] = VisTree.create_oval(ChWidth - 25, ChHeight - 25, ChWidth + 25, ChHeight + 25, outline = "black", width = 3, fill = "white")
            NodesDet[child]["text"] = VisTree.create_text(ChWidth, ChHeight, text = child, font = ("Times New Roman", 16, "bold"))
            NodesDet[child]["coords"] = (ChWidth, ChHeight)

            NodesDet[child]["line"] = DrawLine(PaWidth, PaHeight + 25, ChWidth, ChHeight - 25)
            NodesDet[child]["childIdx"] = 0
        else:
            NodesDet[child]["childIdx"] = CountChild(parent, root) - 1

            NodesDet[child]["circle"] = 0
            NodesDet[child]["text"] = 0
            NodesDet[child]["line"] = 0

            DeleteDrawSubTree(parent)
            ReDrawSubTree(parent)
    
# creare main widget
mainWidget = Tk()
mainWidget.title("Vizualizare Arbore Multicai")

IntroLabel1 = Label(mainWidget, text = "Interfata grafica pentru vizualizarea unui arbore multicai")
IntroLabel1.grid(row = 0, column = 0)

# creare setari initiale pentru radacina

RootLabel = Label(mainWidget, text = "Introdu valoarea nodului radacina")
RootLabel.grid(row = 1, column = 0)

InpValueRoot = Entry(mainWidget)
InpValueRoot.grid(row = 2, column = 0)


def ButtonPressRootValue():
    global RootValue
    RootValue = InpValueRoot.get().strip()

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
    VisTree = Canvas(mainWidget, height = 500, width = 500, bg = "grey")
    VisTree.grid(row = 5)

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
    FirstChildValue = InpFirstChild.get().strip()

    IntroLabel2.destroy()
    InpFirstChild.destroy()
    ButtonFirstChild.destroy()

    #adaugare prim copil
    DrawNode(FirstChildValue, RootValue)

    #crearea setari dupa introducerea radacinii si a primului copil
    IntroLabel3 = Label(mainWidget, text = "Introdu valoarea nodului parinte si nodului copil")
    IntroLabel3.grid(row = 1, column = 0)

    #creare input fiels pt copil-parinte
    global InpParent
    global InpChild
    InpParent = Entry(mainWidget)
    InpChild = Entry(mainWidget)

    InpParent.grid(row = 2, column = 0)
    InpChild.grid(row = 3, column = 0)

   # creare butoane pentru info copil-parinte
    ButtonParentChild = Button(mainWidget, text = "Apasa", command = ButtonPressParentChild)
    ButtonParentChild.grid(row = 4, column = 0)

def ButtonPressParentChild():
    ChildValue = InpChild.get().strip()
    ParentValue = InpParent.get().strip()

    DrawNode(ChildValue, ParentValue)

ButtonRootValue = Button(mainWidget, text = "Apasa", command = ButtonPressRootValue)
ButtonRootValue.grid(row = 2, column = 1)

#Free(root)
mainWidget.mainloop()