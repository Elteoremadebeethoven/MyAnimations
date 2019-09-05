from manimlib.imports import *

class Surfaces(ThreeDScene):
    def construct(self):
        self.axes = ThreeDAxes()
        cylinder = ParametricSurface(
            lambda u, v: np.array([
                np.cos(TAU * v),
                np.sin(TAU * v),
                2 * (1 - u)
            ]),
            resolution=(6, 32)).fade(0.5)
        paraboloide = ParametricSurface(
            lambda u, v: np.array([
                np.cos(v)*u,
                np.sin(v)*u,
                u**2
            ]),v_max=TAU,
            checkerboard_colors=[PURPLE_D, PURPLE_E],
            resolution=(10, 32)).scale(2)
        phi=2
        hiper_para = ParametricSurface(
            lambda u, v: np.array([
                u,
                v,
                u**2-v**2
            ]),v_min=-phi,v_max=phi,u_min=-phi,u_max=phi,checkerboard_colors=[BLUE_D, BLUE_E],
            resolution=(15, 32)).scale(1)
        phi=2
        cono = ParametricSurface(
            lambda u, v: np.array([
                u*np.cos(v),
                u*np.sin(v),
                u
            ]),v_min=0,v_max=TAU,u_min=-phi,u_max=phi,checkerboard_colors=[GREEN_D, GREEN_E],
            resolution=(15, 32)).scale(1)
        phi=2
        hip_una_hoja = ParametricSurface(
            lambda u, v: np.array([
                np.cosh(u)*np.cos(v),
                np.cosh(u)*np.sin(v),
                np.sinh(u)
            ]),v_min=0,v_max=TAU,u_min=-phi,u_max=phi,checkerboard_colors=[YELLOW_D, YELLOW_E],
            resolution=(15, 32)).scale(1)
        elipsoide=ParametricSurface(
            lambda u, v: np.array([
                1*np.cos(u)*np.cos(v),
                2*np.cos(u)*np.sin(v),
                0.5*np.sin(u)
            ]),v_min=0,v_max=TAU,u_min=-PI/2,u_max=PI/2,checkerboard_colors=[TEAL_D, TEAL_E],
            resolution=(15, 32)).scale(2)
        sphere = ParametricSurface(
            lambda u, v: np.array([
                1.5*np.cos(u)*np.cos(v),
                1.5*np.cos(u)*np.sin(v),
                1.5*np.sin(u)
            ]),v_min=0,v_max=TAU,u_min=-PI/2,u_max=PI/2,checkerboard_colors=[RED_D, RED_E],
            resolution=(15, 32)).scale(2)
        curva1=ParametricFunction(
                lambda u : np.array([
                1.2*np.cos(u),
                1.2*np.sin(u),
                u/2
            ]),color=RED,t_min=-TAU,t_max=TAU,
            )
        curva2=ParametricFunction(
                lambda u : np.array([
                1.2*np.cos(u),
                1.2*np.sin(u),
                u
            ]),color=RED,t_min=-TAU,t_max=TAU,
            )
        #sphere.shift(IN)
        self.set_camera_orientation(phi=75 * DEGREES)
        self.begin_ambient_camera_rotation()
        ghost_sphere = sphere.copy()
        pieces = self.get_ghost_surface(sphere)
        random.shuffle(pieces.submobjects)
        for piece in pieces:
            piece.save_state()
        pieces.space_out_submobjects(2)
        pieces.fade(1)

        #self.add(ghost_sphere)
        self.play(LaggedStartMap(Restore, pieces))
        self.remove(pieces)
        self.add(sphere)
        self.wait(0.3)
        #self.play(ReplacementTransform(pieces,sphere))
        #self.wait()
        #'''
        self.play(ReplacementTransform(sphere,elipsoide))
        self.wait()
        self.play(ReplacementTransform(elipsoide,cono))
        self.wait()
        #'''
        self.play(ReplacementTransform(cono,hip_una_hoja))
        self.wait()
        self.play(ReplacementTransform(hip_una_hoja,hiper_para))
        self.wait()
        self.play(ReplacementTransform(hiper_para,paraboloide))
        self.wait()
        self.play(FadeOut(paraboloide))
        self.add_foreground_mobjects(self.axes)
        self.play(ShowCreation(curva1))
        self.play(Transform(curva1,curva2,rate_func=there_and_back))
        self.play(FadeOut(curva1))
        #self.play(Transform(curva2,curva1))
        
        #'''

    def get_ghost_surface(self, surface):
        result = surface.copy()
        #result.set_fill(RED_D, opacity=0.5)
        #result.set_stroke(RED_E, width=0.5, opacity=0.5)
        return result