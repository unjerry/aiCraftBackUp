#version 330
layout(location = 0) in vec3 vertex_position;
layout(location = 1) in vec3 tex_coords;

out vec3 local_position;
out vec3 uvs;

uniform mat4 matrix;

void main(void) {
    local_position = vertex_position;
    uvs=tex_coords;
    gl_Position = matrix * vec4(vertex_position, 1.0);
}
