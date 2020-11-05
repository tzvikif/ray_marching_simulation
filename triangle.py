import glfw
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader,ShaderProgram
import numpy as np

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

# make the context current
glfw.make_context_current(window)

vertices = [0.5,  0.5, 0.0, 1.0, 0.0, 0.0,   
             0.5, -0.5, 0.0, 0.0, 1.0, 0.0, 
             -0.5, -0.5, 0.0, 0.0, 1.0, 0.0, 
             -0.5, 0.5, 0.0, 0.0, 0.0, 1.0 
]
indices = [0,1,3,
        1,2,3]
vertices = np.array(vertices, dtype=np.float32)
indices = np.array(indices,dtype=np.int32)
vertex_array_id = glGenVertexArrays(1)
glBindVertexArray(vertex_array_id)
prog = compileProgram(compileShader('shaders/triangle_vs.glsl', GL_VERTEX_SHADER), compileShader('shaders/triangle_fs.glsl', GL_FRAGMENT_SHADER))
VBO = glGenBuffers(1)
glBindBuffer(GL_ARRAY_BUFFER, VBO)
glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
EBO_id = glGenBuffers(1)
glBindBuffer(GL_ELEMENT_ARRAY_BUFFER,EBO_id)
glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)

position = glGetAttribLocation(prog, "a_position")
glEnableVertexAttribArray(position)
glVertexAttribPointer(position, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(0))

color = glGetAttribLocation(prog, "a_color")
glEnableVertexAttribArray(color)
glVertexAttribPointer(color, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(12))

glUseProgram(prog)
glClearColor(0, 0.1, 0.1, 1)

# the main application loop
while not glfw.window_should_close(window):
    glfw.poll_events()

    glClear(GL_COLOR_BUFFER_BIT)
    with ShaderProgram(prog):
        glBindVertexArray(vertex_array_id)
        #glDrawArrays(GL_TRIANGLES, 0, 3)
        glDrawElements(GL_TRIANGLES,6,GL_UNSIGNED_INT,None)

    glfw.swap_buffers(window)

# terminate glfw, free up allocated resources
glfw.terminate()
glDeleteBuffers(1,[VBO])
glDeleteVertexArrays(1, [vertex_array_id])