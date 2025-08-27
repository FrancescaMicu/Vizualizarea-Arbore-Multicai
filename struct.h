#include <stdio.h>
#include <stdlib.h>

// gcc -shared -o functTree.so -fPIC funct.c

#define Error NULL 

//  structura de arbore multicai
typedef struct node {
    int value;
    struct node* left;
    struct node* right;
}TNode, *TTree;

TTree CreateNode(int value);
void AddChild(TTree parent, TTree new_node);
void FreeTree(TTree tree);
void printTree(TTree root, int level);
void preorder(TTree root);
int CountChild(TTree parent);
TTree CheckValue(TTree root, int value);
int* ObtSubTree(TTree parent, int *NrNodes);
void RecSubTree(TTree parent, int *child, int *cnt);
int FindParent(TTree node, TTree root);
TTree RecParent(TTree child, TTree node);