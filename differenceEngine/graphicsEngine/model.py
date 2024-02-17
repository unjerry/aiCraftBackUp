import numpy as np
import glm


class Triangle:
    def __init__(self, app) -> None:
        self.app = app
        self.ctx = app.ctx
        self.vbo = self.get_vbo()
        self.shader_program = self.get_shader_program("default")
        self.vao = self.get_vao()
        self.m_model = self.get_model_matrix()
        self.on_init()

    def get_model_matrix(self):
        m_model = glm.mat4()
        return m_model

    def on_init(self):
        self.shader_program["m_proj"].write(self.app.camera.m_proj)
        self.shader_program["m_view"].write(self.app.camera.m_view)
        self.shader_program["m_model"].write(self.m_model)

    def get_vao(self):
        vao = self.ctx.vertex_array(
            self.shader_program, [(self.vbo, "3f", "in_position")]
        )
        return vao

    def update(self):
        m_model = glm.rotate(self.m_model, self.app.time, glm.vec3(0, 1, 0))
        self.shader_program["m_model"].write(m_model)

    def render(self):
        self.update()
        self.vao.render()

    def destroy(self):
        self.vbo.release()
        self.shader_program.release()
        self.vao.release()

    def get_vertex_data(self):
        vertex_data = [
            (-1, -1, 1.0),
            (1, -1, 1.0),
            (0.0, 1, 1.0),
        ]
        vertex_data = np.array(vertex_data, dtype="f4")
        return vertex_data

    def get_vbo(self):
        vertex_data = self.get_vertex_data()
        vbo = self.ctx.buffer(vertex_data)
        return vbo

    def get_shader_program(self, shader_name):
        with open(f"shaders/{shader_name}.vert") as file:
            vertex_shader = file.read()
        with open(f"shaders/{shader_name}.frag") as file:
            fragment_shader = file.read()
        program = self.ctx.program(
            vertex_shader=vertex_shader, fragment_shader=fragment_shader
        )
        return program
