#version 460 core
in vec2 vert;
in vec4 col;
out vec4 color;
void main() {
    color = col;
    gl_Position = vec4(vert, 0.0, 1.0);
}
