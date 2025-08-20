#include <stdio.h>
#include <stdlib.h>

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