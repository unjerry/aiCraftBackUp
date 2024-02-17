#version 460 core

uniform sampler2D texx;
in vec4 uvs;

void main() { gl_FragColor = vec4(texture(texx, uvs.xy).rgb, 1); }
