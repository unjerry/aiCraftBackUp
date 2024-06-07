import ctypes
import pyglet.gl as gl


class Shader_error(Exception):
    def __init__(self, message, *args: object) -> None:
        super().__init__(*args)
        self.message = message


def create_shader(target, source_path):
    # read shader source
    source_file = open(source_path, "rb")
    source = source_file.read()
    source_file.close()

    source_length = ctypes.c_int(len(source) + 1)
    source_buffer = ctypes.create_string_buffer(source)

    buffer_pointer = ctypes.cast(
        ctypes.pointer(ctypes.pointer(source_buffer)),
        ctypes.POINTER(ctypes.POINTER(ctypes.c_char)),
    )
    # compile shader
    gl.glShaderSource(target, 1, buffer_pointer, ctypes.byref(source_length))
    gl.glCompileShader(target)
    # handle potential errors
    log_length = gl.GLint(0)
    gl.glGetShaderiv(target, gl.GL_INFO_LOG_LENGTH, ctypes.byref(log_length))

    log_buffer = ctypes.create_string_buffer(log_length.value)
    gl.glGetShaderInfoLog(target, log_length, None, log_buffer)
    if log_length:
        raise Shader_error(str(log_buffer.value))


class Shader:
    def __init__(self, vertex_path, frag_path) -> None:
        self.program = gl.glCreateProgram()
        # create vertex shader
        self.vertex_shader = gl.glCreateShader(gl.GL_VERTEX_SHADER)
        create_shader(self.vertex_shader, vertex_path)
        gl.glAttachShader(self.program, self.vertex_shader)
        # create fragment shader
        self.frag_shader = gl.glCreateShader(gl.GL_FRAGMENT_SHADER)
        create_shader(self.frag_shader, frag_path)
        gl.glAttachShader(self.program, self.frag_shader)
        # link program and clean up
        gl.glLinkProgram(self.program)
        gl.glDeleteShader(self.vertex_shader)
        gl.glDeleteShader(self.frag_shader)

    def __del__(self):
        gl.glDeleteProgram(self.program)

    def find_uniform(self, name):
        return gl.glGetUniformLocation(self.program, ctypes.create_string_buffer(name))

    def uniform_matrix(self, location, matrix):
        gl.glUniformMatrix4fv(
            location, 1, gl.GL_FALSE, (gl.GLfloat * 16)(*sum(matrix.data, []))
        )

    def use(self):
        gl.glUseProgram(self.program)
