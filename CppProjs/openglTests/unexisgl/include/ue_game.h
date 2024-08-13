#ifndef UNEXISGL_GAME
#define UNEXISGL_GAME
#include <unexisgl.h>
namespace unexisgl
{
    class game
    {
    private:
        /* data */
    public:
        game(/* args */);
        ~game();
        void run();
    };

    game::game(/* args */)
    {
    }

    game::~game()
    {
    }

    void game::run()
    {
        while (true)
        {
            // input
            // -----

            // glfw: swap buffers and poll IO events (keys pressed/released, mouse moved etc.)
            // -------------------------------------------------------------------------------
        }
    }

} // namespace unexisgl
#endif