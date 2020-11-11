# version 330 core

in vec3 a_position;
in vec3 a_color;
in vec2 a_texture;

uniform mat4 a_rotation;

out vec3 v_color;
out vec2 v_texture;

void main()
{
    gl_Position = a_rotation*vec4(a_position, 1.0);
    v_color = a_color;
    v_texture = a_texture;
}