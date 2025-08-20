#include "struct.h"

//  functie de creare a unui nod nod

TTree CreateNode(int value) {
    TTree new_node = (TTree)malloc(sizeof(TNode));
    if ( !new_node ) {
        printf("Eroare la adugarea noului nod");
        return Error;
    }
    new_node->value = value;
    new_node->left = new_node->right = NULL;
    return new_node;
}

//  functie de adaugare a unui nod nod la arbore

void AddChild(TTree parent, TTree new_node) {
    if ( !parent->left ) {
        parent->left = new_node;
    } else {
        TTree iter = parent;
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
