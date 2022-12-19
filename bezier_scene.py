from numpy import dot
from manimlib import *

class Dot(Dot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scale(0.7)

MY_CODE = """import numpy as np

# This is a comment
print("Hello world")

class MyClass(Scene):
    def construct(self, n):
        self.t = n

    def method(self, t):
        t = lambda x: x + 1
        c = Circle()
        c.move_to(RIGHT*3 + UP*2)
        c.shift(direction=UP)
"""

class Code1(Scene):
    def construct(self):
        code = Code(MY_CODE)
        # code[1].set_color(RED)
        self.add(code)


def coord(x,y,z=0):
    return np.array([x,y,z])

def simple_cubic_bezier(x1,y1,x2,y2):
    return lambda t: bezier([
        coord(0,0),
        coord(x1,y1),
        coord(x2,y2),
        coord(1,1)
    ])(t)[1]

def smooth_simple_cubic_bezier(*args):
    return lambda t: simple_cubic_bezier(*args)(smooth(t))

def bezier_grow_up(t):
    return smooth_simple_cubic_bezier(1,1.9,1,1.9)(t)

class GrowUp(GrowFromCenter):
    def __init__(self, *args, rate_func=bezier_grow_up,**kwargs):
        super().__init__(*args, rate_func=rate_func, **kwargs)

class BezierScene(Scene):
    def pause(self, n=1.5):
        self.wait(n)

    def construct(self):
        # self.play(FadeIn(Dot(),scale=0.2))
        axes = Axes(
            x_range=[-1,2,1],
            y_range=[-1,2,1],
            width=2,
            height=2,
            axis_config={"include_ticks":False}
        ).to_edge(DL)

        p1 = Dot(LEFT*2)
        p1_tex = Tex("{\\bf P}_1").next_to(p1,LEFT)
        p2 = Dot(RIGHT*2+UP*0.7)
        p2_tex = Tex("{\\bf P}_2").next_to(p2,RIGHT)

        l1 = Line(p1.get_center(),p2.get_center())

        vt = ValueTracker(0.5)

        t_tex = Tex("t=")
        tn = DecimalNumber(0.5)\
            .next_to(t_tex,RIGHT,aligned_edge=DOWN)

        tn.add_updater(lambda m: m.set_value(vt.get_value()))

        p = Dot()
        p.add_updater(lambda m: m.move_to(l1.point_from_proportion(tn.get_value())))
        p_tex = Tex("{\\bf Q}")
        p_tex.add_updater(lambda m: m.next_to(p,DOWN))

        tg = VGroup(t_tex,tn)
        tg.add_updater(lambda m: m.next_to(p,UP,buff=0.3))

        v1 = Arrow(axes.get_origin(),p1.get_center(),buff=0)
        v2 = Arrow(axes.get_origin(),p2.get_center(),buff=0)
        v21 = Arrow(p1.get_center(),p2.get_center(),buff=0)

        v1c = "#3E9"
        v2c = "#3AF"
        v21c = average_color("#3E9","#3AF")

        v1.set_color(v1c)
        v2.set_color(v2c)
        v21.set_color(v21c)

        t21_tex = Tex("t","(","{\\bf P}_2","-","{\\bf P}_1",")")\
            .next_to(v21,UP,buff=0)
        t21_tex[2].set_color(v2c)
        t21_tex[-2].set_color(v1c)


        # self.add(
        #     # axes,
        #     p1,p2,
        #     p1_tex,p2_tex,
        #     l1,
        #     p,p_tex,
        #     tg,
        # )
        self.play(FadeIn(p1,scale=0.2),Write(p1_tex))
        self.pause()
        self.play(FadeIn(p2,scale=0.2),Write(p2_tex))
        self.pause()
        self.play(ShowCreation(l1))
        self.pause()
        self.play(FadeIn(p,scale=0.2),Write(p_tex))
        self.pause()
        self.play(Write(tg))
        self.pause()
        self.play(
            vt.animate.set_value(0),
            run_time=2
        )
        self.pause()
        self.play(
            vt.animate.set_value(1),
            run_time=3
        )
        self.pause()
        self.play(
            tg.animate.fade(1),
            p_tex.animate.fade(1),
            p.animate.fade(1),
            l1.animate.fade(1),
        )

        self.pause()
        self.play(
            GrowFromEdge(axes.x_axis,LEFT),
            GrowFromEdge(axes.y_axis,DOWN),
        )
        # Line.put_start_and_end_on
        self.pause()
        self.play(GrowArrow(v1),FadeToColor(p1_tex,v1c),FadeToColor(p1,v1c))
        self.pause()
        self.play(GrowArrow(v2,run_time=2),FadeToColor(p2_tex,v2c),FadeToColor(p2,v2c))
        self.pause()
        self.play(GrowArrow(v21),FadeIn(t21_tex[2:-1],shift=UP))
        self.pause()
        self.play(Write(VGroup(t21_tex[:2],t21_tex[-1])),p_tex.animate.set_opacity(1))
        self.pause()
        v21.add_updater(lambda m: m.put_start_and_end_on(v21.get_start(),p.get_center()))
        v2.add_updater(lambda m: m.put_start_and_end_on(v2.get_start(),p.get_center()))
        l1.set_opacity(1).set_stroke(width=1)
        p.set_opacity(1)#.set_stroke(width=1)
        t21_tex.add_updater(lambda m: m.next_to(v21,UP,buff=0))
        self.bring_to_back(p)
        self.bring_to_back(l1)
        self.add(v2,v21,t21_tex)
        self.play(
            vt.animate.set_value(0.7),
            run_time=2
        )
        self.pause()
        self.play(
            vt.animate.set_value(0.3),
            run_time=2
        )
        self.pause()
        self.play(
            vt.animate.set_value(0.6),
            run_time=2
        )
        self.pause()

        f1 = Tex("{\\bf Q}","(t)","=","{\\bf P}_1","+","t","(","{\\bf P}_2","-","{\\bf P}_1",")")
        f1.to_edge(DOWN)
        self.play(
            ReplacementTransform(p_tex[0].copy(),f1[0]),run_time=1.5
        )
        self.play(Write(f1[1:3]),run_time=1.5)
        self.play(
            ReplacementTransform(p1_tex[0].copy(),f1[3].set_color(v1c)),run_time=1.5
        )
        self.play(Write(f1[4]),run_time=1.5)
        f1[-4].set_color(v2c)
        f1[-2].set_color(v1c)
        self.play(
            ReplacementTransform(t21_tex[:].copy(),f1[5:]),run_time=1.5
        )
        self.pause()
        #         0           1    2      3         4   5   6       7        8      9         10
        #    Tex("{\\bf P}","(t)","=","{\\bf P}_1","+","t","(","{\\bf P}_2","-","{\\bf P}_1",")")
        #         0           1    2      3         4   5      6         7   8      9
        f2 = Tex("{\\bf Q}","(t)","=","{\\bf P}_1","+","t","{\\bf P}_2","-","t","{\\bf P}_1")
        f2[6].set_color(v2c)
        f2[9].set_color(v1c)
        f2[3].set_color(v1c)
        # [7,8,9,4,5,6] [4,5,6,7,8,9]
        #         0           1    2      3         4   5      6         7   8      9
        f3 = Tex("{\\bf Q}","(t)","=","{\\bf P}_1","-","t","{\\bf P}_1","+","t","{\\bf P}_2")
        f3[3].set_color(v1c)
        f3[6].set_color(v1c)
        f3[9].set_color(v2c)
        # [7,8,9,3,4,5,6],[9,10,11,8,5,6,8]
        #         0           1    2   3   4   5   6   7        8       9  10   11
        f4 = Tex("{\\bf Q}","(t)","=","(","1","-","t",")","{\\bf P}_1","+","t","{\\bf P}_2")
        f4[8].set_color(v1c)
        f4[11].set_color(v2c)
        f2.align_to(f1,DL)
        f3.align_to(f1,DL)
        f4.align_to(f1,DL)

        self.play(
            *[
                ReplacementTransform(f1[i],f2[j])
                if type(i) is int else
                ReplacementTransform(f1[int(i[1:])].copy(),f2[j])
                for i,j in zip(
                    [3,4,5,"r5",7,8,9],
                    [3,4,5,8   ,6,7,9],
                )
            ],
            FadeOut(f1[10]),
            FadeOut(f1[6]),
            run_time=1.5
        )
        self.play(
            *[
                ReplacementTransform(f2[i],f3[j])
                for i,j in zip([7,8,9,4,5,6],[4,5,6,7,8,9])
            ],
            run_time=2
        )
        self.remove(f1[3])
        self.remove(f2[3])
        self.remove(f3[3])
        self.play(
            *[
                ReplacementTransform(f3[i],f4[j])
                for i,j in zip([7,8,9,3,4,5,6],[9,10,11,8,5,6,8])
            ],
            Write(f4[3]),
            Write(f4[4]),
            Write(f4[7]),
            run_time=2
        )
        lerp1 = Tex("{\\tt lerp}","\\tt (","{\\bf P}_1",",","{\\bf P}_2",",t","\\tt )").next_to(f4,UP)
        lerp1[0].set_color(RED)
        lerp1[2].set_color(v1c)
        lerp1[-3].set_color(v2c)
        self.pause()
        self.play(
            LaggedStart(
                FadeTransformPieces(f4[:3].copy(),lerp1[0]),
                Write(lerp1[1]),
                *[
                    ReplacementTransform(f4[i].copy(),lerp1[j])
                    for i,j in zip([8,11],[3-1,5-1])
                ],
                Write(lerp1[3]),
                Write(lerp1[-2:])
            ),
            run_time=2
        )
        self.play(
            # FadeIn(lerp1,UP),
            ShowCreationThenDestruction(
                    Rectangle(color=YELLOW).surround(VGroup(lerp1,f4),stretch=True,buff=0.2)
            ),
            run_time=2
        )
        for mob in self.mobjects:
            mob.clear_updaters()
        self.pause(2)
        self.play(
            FadeOut(axes),
            FadeOut(v1),
            FadeOut(v2),
            FadeOut(v21),
            FadeOut(l1),
            FadeOut(p),
            FadeOut(p_tex),
            FadeOut(lerp1),
            FadeOut(f4),
            FadeOut(f1[:3]),
            FadeOut(t21_tex),
        )
        self.pause()
        #  PART QUADRATIC BEZIER
        # --------------------------------
        p2_grp = VGroup(p2,p2_tex)
        v3c = "#B38"
        p3 = Dot(RIGHT*5+DOWN*0.7,color=v3c)
        p3_tex = Tex("{\\bf P}_3",color=v3c).next_to(p3,DOWN)


        self.add(p2,p2_tex)
        self.play(
            p2_grp.animate.arrange(UP).shift(p2_grp.get_center()+UL+LEFT+UP*1.5),
            p1_tex.animate.next_to(p1,DOWN),
            Write(p3),Write(p3_tex)
        )
        l12 = Line(p1.get_center(),p2.get_center()).set_color(color=[v1c,v2c])
        # l12c = CurvesAsSubmobjects(l12).set_color(color=[RED,TEAL])
        l23 = Line(p2.get_center(),p3.get_center()).set_color(color=[v2c,v3c])
        vt = ValueTracker(0.5)
        q1 = always_redraw(
            lambda: Dot(
                l12.point_from_proportion(vt.get_value()),
                color=interpolate_color(v1c,v2c,vt.get_value())
            )
        )
        q2 = always_redraw(
            lambda: Dot(
                l23.point_from_proportion(vt.get_value()),
                color=interpolate_color(v2c,v3c,vt.get_value())
            )
        )
        # q1
        q1_tex = Tex("{\\bf Q}_1(t)")
        q1_tex.add_updater(lambda m: m.next_to(q1,LEFT,buff=0.2).match_color(q1))
        # q2
        q2_tex = Tex("{\\bf Q}_2(t)")
        q2_tex.add_updater(lambda m: m.next_to(q2,RIGHT,buff=0.2).match_color(q2))
        t_tex = Tex("t=").to_corner(UL,buff=2)
        tn = DecimalNumber(vt.get_value())\
            .next_to(t_tex,RIGHT,aligned_edge=DOWN)
        del tg
        tg = VGroup(t_tex,tn)

        lq1q2 = Line(q1.get_center(),q2.get_center()).set_color(color=[q1.get_color(),q1.get_color()])
        lq1q2.add_updater(
            lambda m: m.put_start_and_end_on(q1.get_center(),q2.get_center()).set_color(color=[q1.get_color(),q2.get_color()])
        )
        q = always_redraw(
            lambda: Dot(
                lq1q2.point_from_proportion(vt.get_value()),
                color=interpolate_color(q1.get_color(),q2.get_color(),vt.get_value())
            )
        )
        q_tex = Tex("{\\bf Q}(t)").add_background_rectangle()
        q_tex.add_updater(lambda m: m.move_to(q.get_center()+rotate_vector(lq1q2.get_unit_vector(),PI/2)*0.6))
        q_tex.add_updater(lambda m: m[1:].match_color(q))

        tn.add_updater(lambda m: m.set_value(vt.get_value()))

        bezier_t = bezier([p1.get_center(),p2.get_center(),p3.get_center()])
        pc = ParametricCurve(bezier_t,t_range=[0,1,0.001])
        pc.set_color(color=[v1c,v2c,v3c])
        self.pause()
        self.bring_to_back(l12)
        self.play(
            ShowCreation(l12)
        )
        self.pause()
        self.play(
            FadeIn(q1,scale=0.3),
            Write(q1_tex),
            LaggedStart(Write(t_tex),Write(tn))
        )
        self.pause()
        self.bring_to_back(l23)
        self.play(
            ShowCreation(l23)
        )
        self.pause()
        self.play(
            FadeIn(q2,scale=0.3),
            Write(q2_tex),
        )
        self.pause()
        self.play(
            ShowCreation(lq1q2)
        )
        self.pause()
        self.play(
            FadeIn(q,scale=0.3),
            Write(q_tex),
        )
        self.pause()
        self.play(
            vt.animate.set_value(0),
            run_time=2
        )
        self.pause(1)
        # self.bring_to_back(pc)
        self.play(
            vt.animate.set_value(1),
            ShowCreation(pc),
            run_time=10
        )
        self.pause()
        qbc = TexText("Quadratic Bézier Curve",color=YELLOW)\
            .next_to(pc,DOWN,buff=-0.6)

        self.play(
            pc.animate.set_stroke(width=8,color=YELLOW),
            Write(qbc,stroke_color=YELLOW)
        )
        self.pause()
        self.play(
            pc.animate.set_stroke(width=3,color=YELLOW),
            vt.animate.set_value(0.5),
            run_time=3
        )
        self.pause()
        q1_lerp = Tex("{\\bf Q}_1(t)","=","{\\tt lerp}","(","{\\bf P}_1",",","{\\bf P}_2",",t)")
        q1_lerp[0].match_color(q1)
        q1_lerp[-4].set_color(v1c)
        q1_lerp[-2].set_color(v2c)
        q1_lerp[2].set_color(RED)
        q2_lerp = Tex("{\\bf Q}_2(t)","=","{\\tt lerp}","(","{\\bf P}_2",",","{\\bf P}_3",",t)")
        q2_lerp[0].match_color(q2)
        q2_lerp[-4].set_color(v2c)
        q2_lerp[-2].set_color(v3c)
        q2_lerp[2].set_color(RED)
        qbc_f = Tex("{\\bf Q}(t)","=","{\\tt lerp}","(","{\\bf Q}_1(t)",",","{\\bf Q}_2(t)",",t)")
        qbc_f[0].match_color(q)
        qbc_f[-4].match_color(q1)
        qbc_f[-2].match_color(q2)
        qbc_f[2].set_color(RED)

        qbc_fx = Tex("{\\bf Q}(t)","=","{\\tt lerp}","(","{\\tt lerp}","(","{\\bf P}_1",",","{\\bf P}_2",")",",","{\\tt lerp}","(","{\\bf P}_2",",","{\\bf P}_3",")",")")
        qbc_f.to_edge(DOWN)

        lerps = VGroup(q1_lerp,q2_lerp,qbc_f).arrange(DOWN,aligned_edge=LEFT).to_edge(DOWN).to_edge(LEFT)

        # self.add(lerps)
        self.play(
            AnimationGroup(
                ReplacementTransform(q1_tex[0].copy(),q1_lerp[0]),
                Write(q1_lerp[1:-4]),
                ReplacementTransform(p1_tex[0].copy(),q1_lerp[-4]),
                Write(q1_lerp[-3]),
                ReplacementTransform(p2_tex[0].copy(),q1_lerp[-2]),
                Write(q1_lerp[-1]),
                # lag_ratio=0.55,
                run_time=4
            )
        )
        self.pause()
        self.play(
            AnimationGroup(
                ReplacementTransform(q2_tex[0].copy(),q2_lerp[0]),
                Write(q2_lerp[1:-4]),
                ReplacementTransform(p2_tex[0].copy(),q2_lerp[-4]),
                Write(q2_lerp[-3]),
                ReplacementTransform(p3_tex[0].copy(),q2_lerp[-2]),
                Write(q2_lerp[-1]),
                # lag_ratio=0.55,
                run_time=4
            )
        )
        self.pause()
        self.play(
            AnimationGroup(
                FadeTransform(q_tex[1:][:].copy(),qbc_f[0]),
                Write(qbc_f[1:-4]),
                ReplacementTransform(q1_lerp[0].copy(),qbc_f[-4]),
                Write(qbc_f[-3]),
                ReplacementTransform(q2_lerp[0].copy(),qbc_f[-2]),
                Write(qbc_f[-1]),
                # lag_ratio=0.55,
                run_time=4
            )
        )
        brace_right = Brace(lerps,RIGHT)
        brace_tex = Tex("{\\bf Q}(t)","=(1-t)^2","{\\bf P}_1","+(1-t)","{\\bf P}_2","+t^2","{\\bf P}_3")\
            .scale(0.8)\
            .next_to(brace_right,RIGHT)
        brace_tex[0].match_color(q)
        brace_tex[2].set_color(v1c)
        brace_tex[4].set_color(v2c)
        brace_tex[6].set_color(v3c)
        self.pause()
        self.play(
            GrowFromCenter(brace_right),
            Write(brace_tex)
        )
        self.pause()
        for m in self.mobjects:
            m.clear_updaters()
        self.play(
            FadeOut(lerps),
            FadeOut(brace_right),
            FadeOut(brace_tex),
            FadeOut(qbc),
            FadeOut(q),
            FadeOut(q_tex),
            FadeOut(q1),
            FadeOut(q1_tex),
            FadeOut(q2),
            FadeOut(q2_tex),
            FadeOut(lq1q2),
            FadeOut(pc),
        )
        self.pause()
        v4c = "#a04"
        p4 = Dot(RIGHT*2+DOWN*2,color=v4c)
        p4_tex = Tex("{\\bf P}_4",color=v4c).next_to(p4,DOWN)
        self.play(
            tg.animate.to_edge(LEFT).set_y(0),
            p3_tex.animate.next_to(p3,RIGHT),
            FadeIn(p4,scale=0.1),
            Write(p4_tex),
            run_time=2,
            # VGroup(p1,p1_tex,p2,p2_tex,p3,p3_tex,l12,l23).animate.shift(LEFT*2).set_y(0)
        )
        l34 = Line(p3.get_center(),p4.get_center(),color=[v3c,v4c])
        self.pause()
        self.play(ShowCreation(l34))
        self.pause()
        def generate_dot(d1,d2):
            return always_redraw(
                lambda:
                    Dot(
                        Line(d1.get_center(),d2.get_center()).point_from_proportion(vt.get_value()),
                        color=interpolate_color(d1.get_color(),d2.get_color(),vt.get_value())
                    )
            )
        # -------
        def generate_line(p1: Dot(),p2: Dot()):
            return always_redraw(
                lambda:
                    Line(p1.get_center(),p2.get_center())
                        .set_color(color=[p1.get_color(),p2.get_color()])
            )
        q1 = generate_dot(p1,p2)
        q2 = generate_dot(p2,p3)
        q3 = generate_dot(p3,p4)

        lq1q2 = generate_line(q1,q2)
        lq2q3 = generate_line(q2,q3)

        r1 = generate_dot(q1,q2)
        r2 = generate_dot(q2,q3)

        ls = generate_line(r1,r2)
        s = generate_dot(r1,r2)

        self.play(
            *list(map(lambda mob: FadeIn(mob,scale=0.2),[q1,q2,q3]))
        )
        self.pause()
        self.play(
            *list(map(lambda mob: ShowCreation(mob),[lq1q2,lq2q3]))
        )
        self.pause()
        self.play(
            *list(map(lambda mob: FadeIn(mob,scale=0.2),[r1,r2]))
        )
        self.pause()
        self.play(
            *list(map(lambda mob: ShowCreation(mob),[ls]))
        )
        self.pause()
        self.play(
            *list(map(lambda mob: FadeIn(mob,scale=0.2),[s]))
        )
        self.pause()
        tn.add_updater(lambda m: m.set_value(vt.get_value()))
        self.play(
            vt.animate.set_value(0),run_time=1.5
        )
        del pc,bezier_t
        bezier_t = bezier([p1.get_center(),p2.get_center(),p3.get_center(),p4.get_center()])
        pc = ParametricCurve(bezier_t,t_range=[0,1,0.001])
        pc.set_color(color=[v1c,v2c,v3c,v4c])
        self.pause()
        self.bring_to_front(pc)
        self.play(
            vt.animate.set_value(1),
            ShowCreation(pc),
            run_time=16
        )
        self.pause()
        pbc = TexText("Cubic Bézier Curve")
        pbc_f = Tex("\mathbf{Q}(t)=(1-t)^{3}","\mathbf {P} _{1}","+3(1-t)^{2}t","\mathbf {P} _{2}","+3(1-t)t^{2}","\mathbf {P} _{3}","+t^{3}","\mathbf {P} _{4}")
        pbc_f.to_edge(DOWN)
        pbc.next_to(pbc_f,UP,aligned_edge=LEFT).set_color(YELLOW)
        pbc_f[1].set_color(v1c)
        pbc_f[3].set_color(v2c)
        pbc_f[5].set_color(v3c)
        pbc_f[7].set_color(v4c)
        self.play(
            pc.animate.set_color(YELLOW),
            Write(pbc),
            vt.animate.set_value(0.5),
            run_time=3
        )
        self.pause()
        self.play(
            Write(pbc_f),
            run_time=2
        )
        self.pause()


