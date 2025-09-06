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

int DetLevel(TTree root, TTree node) {
    int lev = -1;
    RecLevel(root, node, 0, &lev);
    if ( lev == -1 ) {
        printf("Eroare");
        return 0;
    }
    return lev;
}

void RecLevel(TTree root, TTree node, int CurrLevel, int *lev) {
    if ( root == NULL ) {
        return;
    }
    if ( root == node ) {
        (*lev) = CurrLevel;
        return;
    }
    RecLevel(root->left, node, CurrLevel + 1, lev);
    if ( (*lev) == -1 ) {
        RecLevel(root->right, node, CurrLevel, lev);
    }
}

int CountNodesOnLevel(TTree root, int DesLevel) {
    if (root == NULL) {
        return 0;
    }
    int count = 0;
    RecCountNodesLev(root, DesLevel, 0, &count);
    return count;
}

void RecCountNodesLev(TTree root, int DesLev, int CurrLev, int *count) {
    if ( root == NULL ) {
        return;
    }
    if ( CurrLev == DesLev) {
        (*count)++;
    }
    RecCountNodesLev(root->left, DesLev, CurrLev + 1, count);
    RecCountNodesLev(root->right, DesLev, CurrLev, count);
}


int MaxChildOnLevel(TTree root, int DesLev) {
    if ( root == NULL ) {
        return 0;
    }
    int max = -1;
    RecursMax(root, 0, DesLev, &max);
    return max;
}

void RecursMax(TTree root, int CurrLev, int DesLevel, int *max) {
    if ( root == NULL ) {
        return;
    }
    if ( CurrLev == DesLevel ) {
        int NrChild = CountChild(root);
        if ( NrChild > (*max) ) {
            (*max) = NrChild;
        }
    }
    RecursMax(root->left, CurrLev + 1, DesLevel, max);
    RecursMax(root->right, CurrLev, DesLevel, max);
}

void FreeIntArr(int *arr) {
    free(arr);
    arr = NULL;
}

int LevWithMaxNodes(TTree root) {
    if ( root == NULL ) {
        return 0;
    }
    int NrLev = CountLev(root);
    int MaxLev = 0;
    int MaxChild = 0;
    for ( int i = 0; i < NrLev; i++ ) {
        int NrNodes = CountNodesOnLevel(root, i);
        if ( NrNodes > MaxChild ) {
            MaxChild = NrNodes;
            MaxLev = i;
        }
    }
    return MaxLev;
}

int CountLev(TTree root) {
    if ( root == NULL ) {
        return 0;
    }
    int lev = 0;
    RecCountLev(root, 1, &lev);
    return lev;
}

void RecCountLev(TTree root, int CurrLev, int *lev) {
    if ( root == NULL ) {
        return;
    }
    if ( (*lev) < CurrLev)
        (*lev) = CurrLev;
    RecCountLev(root->left, CurrLev + 1, lev);
    RecCountLev(root->right, CurrLev, lev);
}

int RecFirstNodeDesLev(TTree root, int DesLev, int CurrLev) {
    if ( root == NULL ) {
        return -1;
    }
    if ( DesLev == CurrLev ) {
        return root->value;
    }
    int LeftTree = RecFirstNodeDesLev(root->left, DesLev, CurrLev + 1);
    if ( RecFirstNodeDesLev(root->left, DesLev, CurrLev + 1) != -1 ) {
        return LeftTree;
    }
    return RecFirstNodeDesLev(root->right, DesLev, CurrLev);
}

int FirstNodeOnDesLev(TTree root, int DesLev) {
    if ( root == NULL ) {
        return 0;
    }
    int NodeValue = RecFirstNodeDesLev(root, DesLev, 0);
    if ( NodeValue == -1 ) {
        return 0;
    }
    return NodeValue;
}
