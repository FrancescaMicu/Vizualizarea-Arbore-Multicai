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
int DetLevel(TTree root, TTree node);
void RecLevel(TTree root, TTree node, int CurrLevel, int *lev);
int CountNodesOnLevel(TTree root, int DesLevel);
void RecCountNodesLev(TTree root, int DesLev, int CurrLev, int *count);
int MaxChildOnLevel(TTree root, int DesLev);
void RecursMax(TTree root, int CurrLev, int DesLevel, int *max);
void FreeIntArr(int *arr);
int LevWithMaxNodes(TTree root);
void RecCountLev(TTree root, int CurrLev, int * lev);
int CountLev(TTree root);
int RecFirstNodeDesLev(TTree root, int DesLev, int CurrLev);
int FirstNodeOnDesLev(TTree root, int DesLev);