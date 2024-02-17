#version 460 core

in vec3 in_position;
in vec2 uv;
uniform mat4 m_proj;
uniform mat4 m_view;
uniform mat4 m_model;
out vec4 uvs;

void main() {
  uvs = m_model * vec4(uv, 0, 1);
  gl_Position = m_proj * m_view * vec4(in_position, 1.0);
}
