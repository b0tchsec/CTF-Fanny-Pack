//gcc crystalball.c -o crystalball

#include <stdio.h>
#include <stdlib.h>

int main() {
    int num;
    srand(time(NULL));
    num = rand();
    printf("%d\n",num);
}
