/* main.c */
#include "struct.h"

int main() {
    /* creare noduri */
    TTree n1 = CreateNode(1);
    TTree n2 = CreateNode(2);
    TTree n3 = CreateNode(3);
    TTree n4 = CreateNode(4);
    TTree n5 = CreateNode(5);
    TTree n6 = CreateNode(6);
    TTree n7 = CreateNode(7);
    TTree n8 = CreateNode(8);
    TTree n9 = CreateNode(9);
    TTree n10 = CreateNode(10);

    /* constructie arbore */
    AddChild(n1, n2);
    AddChild(n1, n3);
    AddChild(n1, n4);

    AddChild(n2, n5);
    AddChild(n2, n6);

    AddChild(n4, n7);
    AddChild(n4, n8);

    AddChild(n7, n9);
    AddChild(n8, n10);

    printTree(n1, 0);
    int node = -1;
    printf("Level: %d\n", LevWithMaxNodes(n1, &node));
    printf("Node: %d\n", node);

    FreeTree(n1);
    return 0;
}