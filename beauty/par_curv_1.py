from manimlib import *

class ManimScene(Scene):
    CONFIG = {
        "n_x": 9,
        "n_y": 5,
        "square_side": 0.9,
        "v_colors": [RED,YELLOW],
        "h_colors": [RED,PURPLE],
        "max_val": 2,
        "revolutions": 8,
        "run_time": 40,
        "circle_radius_proportion": 1.1,
        "mobile_dot_config": {"color": WHITE, "fill_opacity": 0.8, "radius": 0.05},
        "parametric_curve_config": {"stroke_width": 1}
    }
    def construct(self):
        R = self.revolutions
        x_g, y_g = self.get_grids()
        context = VGroup(x_g, y_g)
        context.set_height(FRAME_HEIGHT-0.5)
        context.move_to(ORIGIN)

        angular_freq_label = Tex("\\omega")
        angular_freq_label.move_to([y_g.get_x(),x_g.get_y(),0])

        H = context.get_height()
        W = context.get_width()

        x_c = self.get_edge_circles(x_g,self.circle_radius_proportion,self.h_colors)
        y_c = self.get_edge_circles(y_g,self.circle_radius_proportion,self.v_colors)

        x_d = self.get_dots_of_circles(x_c)
        x_d.set_color_by_gradient(*self.h_colors)
        y_d = self.get_dots_of_circles(y_c)
        y_d.set_color_by_gradient(*self.v_colors)

        x_p = 1 / (self.n_x - 1)
        y_p = 1 / (self.n_y - 1)

        x_vtrackers = [ValueTracker(0) for _ in range(self.n_x)]
        y_vtrackers = [ValueTracker(0) for _ in range(self.n_y)]

        x_trackers_target = [interpolate(1,self.max_val,i*x_p) for i in range(self.n_x)]
        y_trackers_target = [interpolate(1,self.max_val,i*y_p) for i in range(self.n_y)]

        af_x = VGroup(*[
            Tex("%.3f"%n)
                .set_height(cx.get_height()*0.2)
                .move_to(cx) 
            for n,cx in zip(x_trackers_target,x_c)
        ])
        af_y = VGroup(*[
            Tex("%.3f"%n)
                .set_height(cy.get_height()*0.2)
                .move_to(cy) 
            for n,cy in zip(y_trackers_target,y_c)
        ])

        v_lines = self.get_vertical_lines(context,H,x_d)
        v_lines.set_color_by_gradient(*self.h_colors)
        h_lines = self.get_horizontal_lines(context,W,y_d)
        h_lines.set_color_by_gradient(*self.v_colors)

        m_dots = VGroup(*[
            Dot(**self.mobile_dot_config) for _ in range(self.n_x*self.n_y)
        ])

        def update_tracker(c,t):
            def update_dot(mob):
                mob.move_to(c.point_from_proportion(t.get_value()%1))
            return update_dot

        def update_tracker_x(c,t):
            def update_dot(mob: Line):
                c_coord = c.point_from_proportion(t.get_value()%1)
                mob.set_x(c_coord[0])
                mob.put_start_and_end_on(c_coord, mob.get_end())
            return update_dot

        def update_tracker_y(c,t):
            def update_dot(mob: Line):
                c_coord = c.point_from_proportion(t.get_value()%1)
                mob.set_y(c_coord[1])
                mob.put_start_and_end_on(c_coord, mob.get_end())
            return update_dot

        def update_m_dot(l1,l2):
            def update_dot(mob):
                mob.move_to(self.get_intersection_between_lines(l1,l2))
            return update_dot

        for d,c,t in zip(x_d,x_c,x_vtrackers):
            d.add_updater(update_tracker(c,t))
            d.suspend_updating()

        for d,c,t in zip(y_d,y_c,y_vtrackers):
            d.add_updater(update_tracker(c,t))
            d.suspend_updating()

        for l,c,t in zip(v_lines, x_c, x_vtrackers):
            l.add_updater(update_tracker_x(c,t))
            l.suspend_updating()

        for l,c,t in zip(h_lines, y_c, y_vtrackers):
            l.add_updater(update_tracker_y(c,t))
            l.suspend_updating()
        
        count = 0
        for vl in v_lines:
            for hl in h_lines:
                m_dots[count].add_updater(update_m_dot(hl,vl))
                m_dots[count].suspend_updating()
                count += 1

        axes = VGroup(*[
            self.create_axes_using_2_circles(cx,cy)
            for cx in x_c
            for cy in y_c
        ])

        pcg = VGroup()
        count = 0
        for xt in x_trackers_target:
            for yt in y_trackers_target:
                pc = self.get_parametrict_curve(xt,yt,axes[count])
                pcg.add(pc)
                count += 1
        
        # ---- DRAW
        self.wait(0.3)
        self.play(
            LaggedStart(
                LaggedStart(*[
                    FadeIn(d,shift=UP)
                    for d in x_c
                ]),
                LaggedStart(*[
                    FadeIn(d,shift=LEFT)
                    for d in y_c
                ]),
                LaggedStartMap(Write, af_x),
                LaggedStartMap(Write, af_y),
                Write(angular_freq_label)
            ),
            run_time=2
        )
        self.play(
            LaggedStart(
                *[
                    AnimationGroup(
                        ShowCreation(l),
                        GrowFromCenter(p)
                    )
                    for l,p in zip(v_lines, x_d)
                ],
                *[
                    AnimationGroup(
                        ShowCreation(l),
                        GrowFromCenter(p)
                    )
                    for l,p in zip(h_lines, y_d)
                ],
                LaggedStartMap(GrowFromCenter,m_dots,lag_ratio=0)
            )
        )
        self.wait(0.5)
        for mob in [*x_d,*y_d,*v_lines,*h_lines,*m_dots]:
            mob.resume_updating()

        self.add(
            *pcg,
            *x_c,*y_c,
            *x_d,*y_d,
            *v_lines,*h_lines,
            *m_dots,
        )

        # -------- START ANIMATION
        self.bring_to_back(pcg)
        self.play(
            *[
                ApplyMethod(xvt.set_value, val*R)
                for xvt,val in zip(x_vtrackers, x_trackers_target)
            ],
            *[
                ApplyMethod(yvt.set_value, val*R)
                for yvt,val in zip(y_vtrackers, y_trackers_target)
            ],
            *[
                ShowCreation(pc)
                for pc in pcg
            ],
            run_time=self.run_time,
            rate_func=linear
        )
        self.wait(3)
        black_rect = Rectangle(3,3,fill_opacity=1,fill_color=BLACK,stroke_color=BLACK)\
            .set_width(FRAME_WIDTH,stretch=True)\
            .set_height(FRAME_HEIGHT,stretch=True)
        self.play(FadeIn(black_rect))
        self.wait(0.5)

    def get_grids(self):
        nx, ny = self.n_x, self.n_y

        x_r = VGroup(*[Square(self.square_side) for _ in range(nx+1)])
        y_r = VGroup(*[Square(self.square_side) for _ in range(ny+1)])

        for r,d in zip([x_r, y_r],[RIGHT,DOWN]):
            r.arrange(d,buff=0)
        
        x_r.to_edge(UP)
        y_r.align_to(x_r,LEFT)
        y_r.align_to(x_r,UP)

        x_r.remove(x_r[0])
        y_r.remove(y_r[0])

        return x_r, y_r

    def get_edge_circles(self, grp, p=0.8, colors=[RED,TEAL]):
        circles = VGroup(*[
            Circle(radius=self.square_side*p/2)
                .move_to(g.get_center())
                for g in grp
        ])
        circles.set_color_by_gradient(*colors)
        return circles

    def get_dots_of_circles(self, circles):
        return VGroup(*[
            Dot(c.point_from_proportion(0))
            for c in circles
        ])

    def get_vertical_lines(self, context, H, dots):
        lines = VGroup(*[
            Line(UP,DOWN)
                .set_height(H)
                .move_to(context)
            for _ in range(len(dots))
        ])

        return lines

    def get_horizontal_lines(self, context, W, dots):
        lines = VGroup(*[
            Line(LEFT,RIGHT)
                .set_width(W)
                .move_to(context)
            for _ in range(len(dots))
        ])
        return lines

    def get_intersection_between_lines(self, l1, l2):
        return line_intersection(
            [l1.get_start(),l1.get_end()],
            [l2.get_start(),l2.get_end()]
        )

    def create_axes_using_2_circles(self, cx: Circle, cy: Circle):
        return Axes(
            x_range=[-1,1,0.5],y_range=[-1,1,0.5],
            height=cx.get_height(),
            width=cx.get_width(),
        ).move_to([cx.get_x(),cy.get_y(),0])

    def get_parametrict_curve(self, xt, yt, axes: Axes):
        return axes.get_parametric_curve(
            lambda t: np.array([
                np.cos(self.revolutions*xt*t),
                np.sin(self.revolutions*yt*t),
                0
            ]),
            t_range=[0,2*PI,0.01],
            **self.parametric_curve_config
        )

class Scene1(ManimScene):
    CONFIG = {
        "n_x": 2,
        "n_y": 2,
        "square_side": 1.7,
        "max_val": 2,
        "revolutions": 1,
        "run_time": 15,
        "circle_radius_proportion": 1.2,
    }

class Scene2(ManimScene):
    CONFIG = {
        "n_x": 3,
        "n_y": 3,
        "square_side": 1.8,
        "max_val": 3,
        "revolutions": 1,
        "run_time": 15,
        "circle_radius_proportion": 0.92,
    }

class Scene3(ManimScene):
    CONFIG = {
        "n_x": 5,
        "n_y": 4,
        "square_side": 1.8,
        "max_val": 6,
        "revolutions": 12,
        "run_time": 70,
        "circle_radius_proportion": 0.7,
    }
