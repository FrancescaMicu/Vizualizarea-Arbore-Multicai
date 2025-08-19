#include <stdio.h>

typedef struct node {
    int value;
    struct node* left;
    struct node* right;
}TNode, TTree;