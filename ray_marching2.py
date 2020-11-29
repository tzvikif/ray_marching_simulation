import glfw
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader,ShaderProgram
import numpy as np
import pyrr

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

vertices = [1.0, 1.0,  0.0, 1.0, 1.0,
             1.0, -1.0, 0.0, 1.0,0.0,
             -1.0, -1.0, 0.0, 0.0, 0.0,
             -1.0, 1.0, 0.0, 0.0, 1.0]

indices = [0,1,2,0,2,3]


vertices = np.array(vertices, dtype=np.float32)
indices = np.array(indices,dtype=np.int32)
#Vertex Array 
vertex_array_id = glGenVertexArrays(1)
glBindVertexArray(vertex_array_id)
#Compiling shaders
prog = compileProgram(compileShader('shaders/ray_marching2_vs.glsl', GL_VERTEX_SHADER), compileShader('shaders/ray_marching2_fs.glsl', GL_FRAGMENT_SHADER))
#Vertex buffer object
VBO = glGenBuffers(1)
glBindBuffer(GL_ARRAY_BUFFER, VBO)
glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
#Element buffer object
EBO_id = glGenBuffers(1)
glBindBuffer(GL_ELEMENT_ARRAY_BUFFER,EBO_id)
glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)
#uniforms
resolusion_loc = glGetUniformLocation(prog, "a_resolution")
time_loc = glGetUniformLocation(prog,"a_time")

#Positon attribute
position = glGetAttribLocation(prog, "a_position")
glEnableVertexAttribArray(position)
glVertexAttribPointer(position, 3, GL_FLOAT, GL_FALSE, 20, ctypes.c_void_p(0))
#uv attribute
uv_loc = glGetAttribLocation(prog, "a_uv")
glEnableVertexAttribArray(uv_loc)
glVertexAttribPointer(uv_loc, 2, GL_FLOAT, GL_FALSE, 20, ctypes.c_void_p(4*3))
glBindVertexArray(0)

glClearColor(0, 0.1, 0.1, 1)
glEnable(GL_DEPTH_TEST)
glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
angle_deg = 0
mat_translation = pyrr.matrix44.create_from_translation(pyrr.Vector3([0.3, 2, 0]))
# the main application loop
while not glfw.window_should_close(window):
    glfw.poll_events()
    glUseProgram(prog)
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    glClear(GL_COLOR_BUFFER_BIT)
    glBindVertexArray(vertex_array_id)
    
    #mat_rotation = pyrr.Matrix44.from_y_rotation(0.5 * glfw.get_time())
    #mat_identity = pyrr.matrix44.create_identity()
    #mat_model = pyrr.matrix44.multiply(mat_translation,mat_rotation)
    #sphere1_pos = pyrr.matrix44.apply_to_vector(mat_model,pyrr.Vector3([0, 0, -5]))
    glUniform2f(resolusion_loc,new_width,new_height)
    glUniform1f(time_loc,glfw.get_time())
    #glUniform3f(sphere1_pos_loc,sphere1_pos[0],sphere1_pos[1],sphere1_pos[2])

    glDrawElements(GL_TRIANGLES,6,GL_UNSIGNED_INT,None)
    glfw.swap_buffers(window)

# terminate glfw, free up allocated resources
glfw.terminate()
glDeleteBuffers(1,[VBO])
glDeleteVertexArrays(1, [vertex_array_id])