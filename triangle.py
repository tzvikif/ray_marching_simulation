import glfw
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader,ShaderProgram
import numpy as np
import pyrr
from PIL import Image

new_width = 1280
new_height = 720
# glfw callback functions
def window_resize(window, width, height):
    glViewport(0, 0, width, height)
    new_width,new_height = width,height

# initializing glfw library
if not glfw.init():
    raise Exception("glfw can not be initialized!")
# Configure the OpenGL context.
# If we are planning to use anything above 2.1 we must at least
# request a 3.3 core context to make this work across platforms.
glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, True)
# 4 MSAA is a good default with wide support
glfw.window_hint(glfw.SAMPLES, 4)

# creating the window
window = glfw.create_window(1280, 720, "My OpenGL window", None, None)

# check if window was created
if not window:
    glfw.terminate()
    raise Exception("glfw window can not be created!")

# set window's position
glfw.set_window_pos(window, 400, 200)
# set the callback function for window resize
glfw.set_window_size_callback(window, window_resize)
# make the context current
glfw.make_context_current(window)

vertices = [-0.5, -0.5,  0.5,  1.0, 0.0, 0.0,  0.0, 0.0,
             0.5, -0.5,  0.5,  0.0, 1.0, 0.0,  1.0, 0.0,
             0.5,  0.5,  0.5,  0.0, 0.0, 1.0,  1.0, 1.0,
            -0.5,  0.5,  0.5,  1.0, 1.0, 1.0,  0.0, 1.0,

            -0.5, -0.5, -0.5,  1.0, 0.0, 0.0,  0.0, 0.0,
             0.5, -0.5, -0.5,  0.0, 1.0, 0.0,  1.0, 0.0,
             0.5,  0.5, -0.5,  0.0, 0.0, 1.0,  1.0, 1.0,
            -0.5,  0.5, -0.5,  1.0, 1.0, 1.0,  0.0, 1.0,

             0.5, -0.5, -0.5,  1.0, 0.0, 0.0,  0.0, 0.0,
             0.5,  0.5, -0.5,  0.0, 1.0, 0.0,  1.0, 0.0,
             0.5,  0.5,  0.5,  0.0, 0.0, 1.0,  1.0, 1.0,
             0.5, -0.5,  0.5,  1.0, 1.0, 1.0,  0.0, 1.0,

            -0.5,  0.5, -0.5,  1.0, 0.0, 0.0,  0.0, 0.0,
            -0.5, -0.5, -0.5,  0.0, 1.0, 0.0,  1.0, 0.0,
            -0.5, -0.5,  0.5,  0.0, 0.0, 1.0,  1.0, 1.0,
            -0.5,  0.5,  0.5,  1.0, 1.0, 1.0,  0.0, 1.0,

            -0.5, -0.5, -0.5,  1.0, 0.0, 0.0,  0.0, 0.0,
             0.5, -0.5, -0.5,  0.0, 1.0, 0.0,  1.0, 0.0,
             0.5, -0.5,  0.5,  0.0, 0.0, 1.0,  1.0, 1.0,
            -0.5, -0.5,  0.5,  1.0, 1.0, 1.0,  0.0, 1.0,

             0.5,  0.5, -0.5,  1.0, 0.0, 0.0,  0.0, 0.0,
            -0.5,  0.5, -0.5,  0.0, 1.0, 0.0,  1.0, 0.0,
            -0.5,  0.5,  0.5,  0.0, 0.0, 1.0,  1.0, 1.0,
             0.5,  0.5,  0.5,  1.0, 1.0, 1.0,  0.0, 1.0]

indices = [0,  1,  2,  2,  3,  0,
           4,  5,  6,  6,  7,  4,
           8,  9, 10, 10, 11,  8,
          12, 13, 14, 14, 15, 12,
          16, 17, 18, 18, 19, 16,
          20, 21, 22, 22, 23, 20]


vertices = np.array(vertices, dtype=np.float32)
indices = np.array(indices,dtype=np.int32)
#Vertex Array 
vertex_array_id = glGenVertexArrays(1)
glBindVertexArray(vertex_array_id)
#Compiling shaders
prog = compileProgram(compileShader('shaders/cube_vs.glsl', GL_VERTEX_SHADER), compileShader('shaders/cube_fs.glsl', GL_FRAGMENT_SHADER))
#Vertex buffer object
VBO = glGenBuffers(1)
glBindBuffer(GL_ARRAY_BUFFER, VBO)
glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
#Element buffer object
EBO_id = glGenBuffers(1)
glBindBuffer(GL_ELEMENT_ARRAY_BUFFER,EBO_id)
glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)
#Positon attribute
position = glGetAttribLocation(prog, "a_position")
glEnableVertexAttribArray(position)
glVertexAttribPointer(position, 3, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(0))
#uniforms
model_loc = glGetUniformLocation(prog, "model")
projection_loc = glGetUniformLocation(prog, "projection")
mat_translation = pyrr.matrix44.create_from_translation(pyrr.Vector3([0,0,-5]))

#Color attribute
color = glGetAttribLocation(prog, "a_color")
glEnableVertexAttribArray(color)
glVertexAttribPointer(color, 3, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(12))
#Texture attribute
texture = glGetAttribLocation(prog, "a_texture")
glEnableVertexAttribArray(texture)
glVertexAttribPointer(texture, 2, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(4*6))
#Sample
texture_id = glGenTextures(1)
glBindTexture(GL_TEXTURE_2D, texture_id)

# Set the texture wrapping parameters
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
# Set texture filtering parameters
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

# load image
image = Image.open("textures/crate.jpg")
image = image.transpose(Image.FLIP_TOP_BOTTOM)
img_data = image.convert("RGBA").tobytes()
# img_data = np.array(image.getdata(), np.uint8) # second way of getting the raw image data
glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image.width, image.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)


glBindVertexArray(0)

glClearColor(0, 0.2, 0.2, 1)
glEnable(GL_DEPTH_TEST)
glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

# the main application loop
while not glfw.window_should_close(window):
    glfw.poll_events()
    glUseProgram(prog)
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    glClear(GL_COLOR_BUFFER_BIT)
    glBindVertexArray(vertex_array_id)
    mat_projection = pyrr.matrix44.create_perspective_projection(45,new_width/new_height,0.1,100.0)
    glUniformMatrix4fv(projection_loc, 1, GL_FALSE, mat_projection)
    rot_x = pyrr.Matrix44.from_x_rotation(0.5 * glfw.get_time())
    rot_y = pyrr.Matrix44.from_y_rotation(0.8 * glfw.get_time())
    mat_rotation = pyrr.matrix44.multiply(rot_x, rot_y)
    mat_identity = pyrr.matrix44.create_identity()
    mat_model = pyrr.matrix44.multiply(mat_rotation,mat_translation)
    glUniformMatrix4fv(model_loc, 1, GL_FALSE, mat_model)
    glUniformMatrix4fv(projection_loc, 1, GL_FALSE, mat_projection)

    glDrawElements(GL_TRIANGLES,36,GL_UNSIGNED_INT,None)
    glfw.swap_buffers(window)

# terminate glfw, free up allocated resources
glfw.terminate()
glDeleteBuffers(1,[VBO])
glDeleteVertexArrays(1, [vertex_array_id])