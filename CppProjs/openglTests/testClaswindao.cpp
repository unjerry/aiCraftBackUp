#include <iostream>
#include <ue_windao.h>
#include <unexisgl.h>
#include <ue_game.h>
int main()
{
    unexisgl::initialize();
    unexisgl::windao windao(800, 600);
    unexisgl::game app;
    app.run();
    return 0;
}
