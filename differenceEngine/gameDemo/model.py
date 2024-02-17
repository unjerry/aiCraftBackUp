import numpy as np
import glm
import moderngl as mgl
import cv2
import pygame as pg


class Triangle:
    def __init__(self, app) -> None:
        self.app = app
        self.ctx = app.ctx
        self.vbo = self.get_vbo()
        self.shader_program = self.get_shader_program("default")
        self.vao = self.get_vao()
        self.pose = glm.vec3(0, 0, 0)
        self.m_model = self.get_model_matrix()
        self.tex = self.get_tex()
        self.on_init()

    def get_tex(self):

        rr = cv2.imread("./images/img4.png", cv2.IMREAD_UNCHANGED)
        print(rr[:2, :2, :])
        # rr=np.array(np.concatenate([rr,255*np.ones_like(rr[:,:,0:1])],axis=2))
        # print(rr[:2,:2,:])
        cv2.imwrite("./outputs/img4.png", rr)
        tex = self.ctx.texture((rr.shape[1], rr.shape[0]), 4)
        tex.filter = (mgl.NEAREST, mgl.NEAREST)
        tex.write(rr)
        tex.use(0)
        return tex

    def get_model_matrix(self):
        m_model = glm.translate(self.pose) * glm.scale(glm.mat4(), glm.vec3(0.3, 0.3, 1))
        return m_model

    def on_init(self):
        self.shader_program["m_proj"].write(self.app.camera.m_proj)
        self.shader_program["m_view"].write(self.app.camera.m_view)
        self.shader_program["m_model"].write(self.m_model)
        self.shader_program["texx"] = 0

    def get_vao(self):
        vao = self.ctx.vertex_array(
            self.shader_program, [(self.vbo, "3f 2f", "in_position", "uv")]
        )
        return vao

    def update(self):
        self.keyboard_control()
        # m_model = glm.rotate(self.m_model, self.app.time, glm.vec3(0, 1, 0))
        # self.shader_program["m_model"].write(m_model)

    def render(self):
        self.update()
        self.vao.render(mgl.TRIANGLE_STRIP)

    def destroy(self):
        self.vbo.release()
        self.shader_program.release()
        self.vao.release()

    def get_vertex_data(self):
        vertex_data = [
            (-1, -1, 0.0, 0, 1),
            (1, -1, 0.0, .6, 1),
            (-1, 1, 0.0, 0, 0),
            (1, 1, 0.0, .6, 0),
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

    # def mouse_control(self):
    #     mouse_dx, mouse_dy = pg.mouse.get_rel()
    #     if mouse_dx:
    #         self.rotate_yaw(delta_x=mouse_dx * MOUSE_SENSITIVITY)
    #     if mouse_dy:
    #         self.rotate_pitch(delta_y=mouse_dy * MOUSE_SENSITIVITY)

    def keyboard_control(self):
        PLAYER_SPEED = 1.0*0.3
        key_state = pg.key.get_pressed()
        vel = PLAYER_SPEED * self.app.dtime
        if key_state[pg.K_w] | key_state[pg.K_UP]:
            self.pose -= glm.vec3(0, vel, 0)
        if key_state[pg.K_s] | key_state[pg.K_DOWN]:
            self.pose += glm.vec3(0, vel, 0)
        if key_state[pg.K_d] | key_state[pg.K_RIGHT]:
            self.pose += glm.vec3(vel, 0, 0)
        if key_state[pg.K_a] | key_state[pg.K_LEFT]:
            self.pose -= glm.vec3(vel, 0, 0)
        if self.pose.x<0:
            self.pose.x+=1.0
        if self.pose.x>1.0:
            self.pose.x-=1.0
        if self.pose.y<0:
            self.pose.y+=1.0
        if self.pose.y>1.0:
            self.pose.y-=1.0
        # if key_state[pg.K_SPACE]:
        #     self.move_up(vel)
        # if key_state[pg.K_LSHIFT]:
        #     self.move_down(vel)
        print(self.pose)
        m_model = self.get_model_matrix()
        self.shader_program["m_model"].write(m_model)
