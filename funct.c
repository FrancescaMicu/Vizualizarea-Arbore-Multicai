#include "struct.h"

//  functie de creare a unui nou nod

TTree CreateNode(int value) {
    TTree new_node = (TTree)malloc(sizeof(TNode));
    if ( !new_node ) {
        printf("Eroare la crerea noului nod");
        return Error;
    }
    new_node->value = value;
    new_node->left = new_node->right = NULL;
    return new_node;
}

//  functie de adaugare a unui nod nod la arbore

void AddChild(TTree parent, TTree new_node) {
    if ( parent == NULL ) {
        return;
    }
    if ( !parent->left ) {
        parent->left = new_node;
    } else {
        TTree iter = parent->left;
        while ( iter->right ) {
            iter = iter->right;
        }
        iter->right = new_node;
    }
}


//  functia pentru eliberarea arborelui

void FreeTree(TTree tree) { 
    if ( !tree ) return;
    FreeTree(tree->left);
    FreeTree(tree->right);
    free(tree);
}


/* Afisare arbore cu indentare / nivel */
void printTree(TTree root, int level) {
    if (!root) return;
    
    for (int i = 0; i < level; i++)
        printf("  ");  /* indentare */ 
    
    printf("↳ %d\n", root->value);

    printTree(root->left, level + 1);  
    printTree(root->right, level);     
}


void preorder(TTree root) {
    if (!root) return;
    printf("%d ", root->value);
    preorder(root->left);   /* copii */
    preorder(root->right);  /* frati */
}

//  functie pentru calcularea numarului de copii al unui nod

int CountChild(TTree parent) {
    if ( parent == NULL ) {
        return 0;
    }
    if ( !parent->left ) {
        return 0;
    }
    TTree iter = parent->left;
    int count = 0;
    while( iter ) {
        iter = iter->right;
        count++;
    }
    return count;
}

//  functie pentru verificarea unui valori din arbore
TTree CheckValue(TTree root, int value) {
    if ( root == NULL ) {
        return NULL;
    }
    if ( root->value == value ) {
        return root;
    }
    TTree ChildCheck = CheckValue(root->left, value);
    if ( ChildCheck != NULL ) {
        return ChildCheck;
    }
    return  CheckValue(root->right, value);
}

//  functie pentru obtinerea subarborelui pornind de la un nod
int* ObtSubTree(TTree parent, int *NrNodes) {
    if ( parent == NULL ) {
        return NULL;
    }
    TTree iter = parent;
    int *child = (int*)malloc(100 * sizeof(int));
    if ( child == NULL ) {
        return NULL;
    }
    (*NrNodes) = 0;
    RecSubTree(parent, child, NrNodes);
    return child;
}

void RecSubTree(TTree parent, int *child, int *cnt) {
    if ( parent == NULL ) {
        return;
    }
    child[(*cnt)++] = parent->value;
    RecSubTree(parent->left, child, cnt);
    RecSubTree(parent->right, child, cnt);
}

int FindParent(TTree node, TTree root) {
    if ( root == NULL || root == node || root == NULL ) {
        return 0;
    }
    TTree parent = RecParent(node, root);
    return parent->value;
}

TTree RecParent(TTree child, TTree node) {
    if ( node == NULL ) {
        return NULL;
    }
    TTree iter = node->left;
    while ( iter ) {
        if ( iter == child ) {
            return node;
        }
        iter = iter->right;
    }
    TTree LeftTree = RecParent(child, node->left);
    if ( LeftTree ) {
        return LeftTree;
    }
    return RecParent(child, node->right);
}
