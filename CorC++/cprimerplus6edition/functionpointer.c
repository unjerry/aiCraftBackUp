#include <stdio.h>
int main()
{
    typedef enum B
    {
        FSD,
        DD
    } B;
    B a = FSD;
    printf("%d\n", DD);
    return 0;
}