# version 330 

in vec3 a_position;
in vec3 a_color;

uniform mat4 rotation;
out vec3 v_color;

void main()
{
    gl_Position = rotation*vec4(a_position, 1.0);
    v_color = a_color;
}