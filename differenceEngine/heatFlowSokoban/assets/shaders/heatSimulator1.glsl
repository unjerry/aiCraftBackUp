#version 460 core

layout(local_size_x = 16, local_size_y = 16, local_size_z = 1) in;
layout(r32f, binding = 1) uniform image2D inField;
layout(r32f, binding = 0) uniform image2D outField;

void main() {
  float dt = 0.01;
  ivec2 pixel_coords = ivec2(gl_GlobalInvocationID.xy);
  float pixel = imageLoad(inField, pixel_coords).r;
  float pixelxm1 =
      imageLoad(inField, ivec2((pixel_coords.x - 1 + 50 * 16) % (50 * 16),
                               pixel_coords.y))
          .r;
  float pixelxp1 =
      imageLoad(inField, ivec2((pixel_coords.x + 1 + 50 * 16) % (50 * 16),
                               pixel_coords.y))
          .r;
  float pixelym1 =
      imageLoad(inField, ivec2(pixel_coords.x,
                               (pixel_coords.y - 1 + 50 * 16) % (50 * 16)))
          .r;
  float pixelyp1 =
      imageLoad(inField, ivec2(pixel_coords.x,
                               (pixel_coords.y + 1 + (50 * 16)) % (50 * 16)))
          .r;
  float meanPixel = (pixelxm1 + pixelxp1 + pixelym1 + pixelyp1) / 4;
  float diff = meanPixel - pixel;
  float newPixel = pixel + dt * diff;
  imageStore(outField, pixel_coords, vec4(newPixel));
}
