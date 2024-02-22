#version 460 core

in vec2 uv;
uniform sampler2D tex;

void main() { gl_FragColor = vec4(texture(tex, uv).rrr / 273.5, 1.0); }