#ifndef WINDAO
#define WINDAO
#include <unexisgl.h>
#include <iostream>
namespace unexisgl
{
    class windao
    {
    private:
        GLFWwindow *window;
        GLFWframebuffersizefun funcOnResize;
        GLFWcursorposfun funcOnClick;

    public:
        windao(const int &SCR_WIDTH = 800, const int &SCR_HEIGHT = 600);
        ~windao();
        void setOnResize(GLFWframebuffersizefun);
        void setOnClick(GLFWcursorposfun);
        GLFWwindow *getWindow() { return this->window; }
    };

    windao::windao(const int &SCR_WIDTH, const int &SCR_HEIGHT)
    {
        // glfw window creation
        // --------------------
        GLFWwindow *window = glfwCreateWindow(SCR_WIDTH, SCR_HEIGHT, "LearnOpenGL", NULL, NULL);
        if (window == NULL)
        {
            std::cout << "Failed to create GLFW window" << std::endl;
            glfwTerminate();
        }
        glfwMakeContextCurrent(window);
    }

    windao::~windao()
    {
    }

    void windao::setOnResize(GLFWframebuffersizefun func)
    {
        this->funcOnResize = func;
        glfwSetFramebufferSizeCallback(this->window, this->funcOnResize);
    }

    void windao::setOnClick(GLFWcursorposfun func)
    {
        this->funcOnClick = func;
        glfwSetCursorPosCallback(this->window, this->funcOnClick);
    }

}
#endif