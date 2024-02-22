#version 460 core

in vec2 vert;
in vec2 uvs;
out vec2 uv;

void main() {
  uv = uvs;
  gl_Position = vec4(vert, 0.0, 1.0);
}
