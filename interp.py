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
ctree.preorder.restypes = None

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