import contextlib, logging, math, sys
from OpenGL import GL as gl
import glfw

log = logging.getLogger(__name__)

@contextlib.contextmanager
def create_main_window():
    if not glfw.init():
        log.error('failed to initialize GLFW')
        sys.exit(1)
    try:
        log.debug('requiring modern OpenGL without any legacy features')
        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
        glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, True)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

        log.debug('opening window')
        title = 'Tutorial 1: Window'
        window = glfw.create_window(500, 400, title, None, None)
        if not window:
            log.error('failed to open GLFW window.')
            sys.exit(2)
        glfw.make_context_current(window)

        log.debug('set background to dark blue')
        gl.glClearColor(0, 0, 0.4, 0)

        yield window

    finally:
        glfw.terminate()

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    with create_main_window() as window:
        while (
            glfw.get_key(window, glfw.KEY_ESCAPE) != glfw.PRESS and
            not glfw.window_should_close(window)
        ):
            gl.glClear(gl.GL_COLOR_BUFFER_BIT)
            glfw.swap_buffers(window)
            glfw.poll_events()
