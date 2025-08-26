from tkinter import *
from interp import *

#dictionar pentru a retine cati copii are fiecare nod
NodeCoords = {}

def DrawLine(PaWidth, PaHeight, ChWidth, ChHeight):
    VisTree.create_line(PaWidth, PaHeight, ChWidth, ChHeight, width = 3)

def DrawNode(child, parent):
    #Verificare daca nodul adaugat e radacina
    if parent == '\0':
        NodeCoords[child] = (250, 30)
        node = VisTree.create_oval(225, 5, 275, 55, outline = "black", width = 3, fill = "white")
        NodeValue = VisTree.create_text(250, 30, text = child, font = ("Times New Roman", 16))
    else:
        if not NewChild(parent, child, root):
            return
        # #verificare al catelea copil este
        PaWidth, PaHeight = NodeCoords[parent]
        ChHeight = PaHeight + 75
        ChildCount = CountChild(parent, root)
        sibling_index = ChildCount - 1  # indexul acestui copil (0-based)
        ChWidth = PaWidth + (sibling_index - (ChildCount-1)/2) * 80

        node = VisTree.create_oval(ChWidth - 25, ChHeight - 25, ChWidth + 25, ChHeight + 25, outline = "black", width = 3, fill = "white")
        NodeValue = VisTree.create_text(ChWidth, ChHeight, text = child, font = ("Times New Roman", 16, "bold"))
        NodeCoords[child] = (ChWidth, ChHeight)

        DrawLine(PaWidth, PaHeight + 25, ChWidth, ChHeight - 25)
    
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