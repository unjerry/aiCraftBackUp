#version 330

out vec4 fragment_color;
uniform sampler2DArray texture_array_sampler;
in vec3 local_position;
in vec3 uvs;
void main(void) {
    fragment_color = texture(texture_array_sampler, uvs);
}
