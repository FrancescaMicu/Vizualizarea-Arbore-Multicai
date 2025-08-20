from ctypes import Structure, POINTER, c_int, c_void_p, CDLL

ctree = CDLL("./functTree.so")

ctree.CreateNode.argtypes = [c_int]
ctree.CreateNode.restype = c_void_p

ctree.AddChild.argtypes = [c_void_p, c_void_p]
ctree.AddChild.argtypes = None

ctree.FreeTree.argtypes = [c_void_p]
ctree.FreeTree.argtypes = None

global root

# functii

def NewTree(value):
    root = ctree.CreateNode(value)
    if not root:
        print("Nu s-a putut crea radacina")
        return False
    return True

def NewChild(parent, new_node):
    #fct pt cautare parint + verif
    ctree.AddChild(parent, new_node)
    return True

def Free(root):
    ctree.FreeTree(root)