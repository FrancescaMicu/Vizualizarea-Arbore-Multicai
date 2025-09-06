from ctypes import *
ctree = CDLL("./functTree.so")

ctree.CreateNode.argtypes = [c_int]
ctree.CreateNode.restype = c_void_p

ctree.AddChild.argtypes = [c_void_p, c_void_p]
ctree.AddChild.restype = None

ctree.FreeTree.argtypes = [c_void_p]
ctree.FreeTree.restype = None

ctree.CountChild.argtypes = [c_void_p]
ctree.CountChild.restype = c_int

ctree.CheckValue.argtypes = [c_void_p, c_int]
ctree.CheckValue.restype = c_void_p

ctree.preorder.argtypes = [c_void_p]
ctree.preorder.restype = None

ctree.ObtSubTree.argtypes = [c_void_p, POINTER(c_int)]
ctree.ObtSubTree.restype = POINTER(c_int)

ctree.FindParent.argtypes = [c_void_p, c_void_p]
ctree.FindParent.restype = c_int

ctree.DetLevel.argtypes = [c_void_p, c_void_p]
ctree.DetLevel.restype = c_int

ctree.CountNodesOnLevel.argtypes = [c_void_p, c_int]
ctree.CountNodesOnLevel.restype = c_int

ctree.MaxChildOnLevel.argtypes = [c_void_p, c_int]
ctree.MaxChildOnLevel.restype = c_int

ctree.FreeIntArr.argtypes = [c_void_p]
ctree.FreeIntArr.restype = None

ctree.LevWithMaxNodes.argtypes = [c_void_p]
ctree.LevWithMaxNodes.restype = c_int

ctree.FirstNodeOnDesLev.argtypes = [c_void_p, c_int]
ctree.FirstNodeOnDesLev.restype = c_int

# functii pentru arbore
global root

def Print(root):
    ctree.preorder(root)

def CreateTree(value):
    return ctree.CreateNode(int(value))

def NewChild(parent, new_node, root):
    parent_pt = FindNode(root, parent)
    if not parent_pt:
        print("Parintele introdus nu exista")
        return False
    if FindNode(root, new_node):
        print("Nodul " + str(new_node) + " deja exista in arbore")
        return False
    child = ctree.CreateNode(int(new_node))
    if not child:
        return False
    if not parent_pt:
        print("Nu s-a putut gasi pointerul parintelui")
        return False
    ctree.AddChild(parent_pt, child)
    return True

def FindNode(root, value):
    return ctree.CheckValue(root, int(value))

def Free(root):
    ctree.FreeTree(root)

def CountChild(parent, root):
    parent_pt = FindNode(root, parent)
    if not parent_pt:
        print("Nu s-a putut gasi pointerul parintelui")
        return False
    return ctree.CountChild(parent_pt)

def GetSubTree(parent, root):
    parent_pt = FindNode(root, parent)
    if not parent_pt:
        print("Nu s-a putut gasi pointerul parintelui")
        return []
    NrNodes = c_int(0)
    NodeArray = ctree.ObtSubTree(parent_pt, byref(NrNodes))
    if not NodeArray:
        print("Nu s-a putut face vectorul cu subarborele")
        return []
    NodeList = []
    for i in range(1, NrNodes.value):
        NodeList.append(NodeArray[i])
    ctree.FreeIntArr(NodeArray)
    return NodeList

def GetChild(parent, root):
    parent_pt = FindNode(root, parent)
    if not parent_pt:
        print("Nu s-a putut gasi pointerul parintelui")
        return []
    NrNodes = c_int(0)
    NodeArray = ctree.ObtSubTree(parent_pt, byref(NrNodes))
    if not NodeArray:
        print("Nu s-a putut face vectorul cu subarborele")
        return []
    NodeList = []
    NrChild = CountChild(parent, root)
    for i in range(1, NrChild + 1):
        NodeList.append(NodeArray[i])
    ctree.FreeIntArr(NodeArray)
    return NodeList

def FindPar(child, root):
    child_pt = FindNode(root, child)
    if not child_pt:
        print("Nu s-a putut gasi pointerul nodului")
        return False
    return ctree.FindParent(child_pt, root)

def FindLev(node, root):
    node_pt = FindNode(root, node)
    if not node_pt:
        print("Nu s-a putut gasi pointerul nodului")
        return False
    return ctree.DetLevel(root, node_pt)

def NrChildLevel(root, lev):
    return ctree.CountNodesOnLevel(root, lev + 1)

def DetMaxChildLev(root, lev):
    return ctree.MaxChildOnLevel(root, lev)

def FindLevWithMaxNodes(root):
    return ctree.LevWithMaxNodes(root)

def FindFirstNodeOnLev(root, lev):
    return ctree.FirstNodeOnDesLev(root, lev)