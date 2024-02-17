#version 430 core
uniform sampler2D tex;

in vec2 uvs;
//uniform vec2 normalRes;
out vec4 f_color;

void main()
{
    //vec4 col = texture2D(tex, uvs);
    //float a = col.r;
    
//    float num = 0.0;
  //  for(float i = -1.0; i < 2.0; i++) {
    //    for(float j = -1.0; j < 2.0; j++) {
      //  float x = uvs.x + i * normalRes.x;
//        float y = uvs.y + j * normalRes.y;
//
  //      num += texture2D(tex, vec2(x, y)).r;
    //    }
    //}
    //num -= a;
  
//    if(a > 0.5) {
  //      if(num < 1.5) {
    //        a = 0.0;
      //  }
//        if(num > 3.5) {
  //          a = 0.0;
    //    }
//    } else {
  //      if(num > 2.5 && num < 3.5) {
    //        a = 1.0;
      //  }
//    }
    f_color=vec4(1.0,1.0,0.1,1.0);
}
