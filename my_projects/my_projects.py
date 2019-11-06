from manimlib.imports import *
from my_projects.my_objects import *
from my_projects.my_animations import *

# Abstract scenes (no render this scenes)
# The "setup" method is always executed before the construct method
class GenericExample(Scene):
    def setup(self):
        text1 = Text("Hello world",font="Times").set_stroke(width=0)
        text2 = TexMobject(r"""
                    \oint_C \vec{B}\cdot d
                    \vec{l}=\mu_0\int_S \vec{J}
                    \cdot d \vec{s}+\mu_0
                    \epsilon_0\dfrac{d}{dt}
                    \int_S \vec{E}\cdot d \vec{s}"""
                )
        text3 = TextMobject("This is a example animation")
        self.text_group = VGroup(text1,text2,text3).arrange_submobjects(DOWN,buff=1)
        self.text_group.scale(1.4)
        self.add(self.text_group)

class GenericPaths(Scene):
    def setup(self):
        path1 = Square()
        path2 = Ellipse().scale(1.5)
        path3 = VMobject()
        path3.set_points_as_corners([LEFT*3,ORIGIN,UP,UP+RIGHT*3])
        self.path_group = VGroup(path1,path2,path3).arrange_submobjects(DL,buff=1)
        self.add(self.path_group)

class FormulaExample(Scene):
    def setup(self):
        self.tex_example = TexMobject(r"""
                    \oint_C \vec{B}\cdot d
                    \vec{l}=\mu_0\int_S \vec{J}
                    \cdot d \vec{s}+\mu_0
                    \epsilon_0\dfrac{d}{dt}
                    \int_S \vec{E}\cdot d \vec{s}"""
                )

#Scenes

class PassRectangleExample(GenericExample):
    def construct(self):
        t1,t2,t3 = self.text_group
        # PassRectangle: See my_animations.py line 4 -> 63
        self.play(
            PassRectangle(t1),
            PassRectangle(t2,color=TEAL),
            PassRectangle(t3,midle_color=ORANGE,color=RED)
            )
        self.wait()
        self.play(
            PassRectangle(t1,init_opacity=0.5,margin=0.5),
            PassRectangle(t2,init_opacity=0.1,max_opacity=1,rate_func=there_and_back),
            PassRectangle(t3,midle_color=ORANGE,color=RED,init_opacity=0.1,max_opacity=1)
            )
        self.wait(2)

class UnderlineIndicationExample(GenericExample):
    def construct(self):
        t1,t2,t3 = self.text_group
        # UnderlineIndication: See my_animations.py line 66
        self.play(
            UnderlineIndication(t1),
            UnderlineIndication(t2,line_type=DashedLine),
            )
        self.wait(2)

class DashedRectangleExample(GenericExample):
    def construct(self):
        t1,t2,t3 = self.text_group
        # DashedRectangle: See my_objects.py line 6
        dr1 = DashedRectangle(line_config={"stroke_opacity":0.5})
        # SurroundingDashedRectangle: See my_objects.py line 45
        dr2 = SurroundingDashedRectangle(t1)
        self.add(dr1,dr2)
        # RemarkDashedRectangle: See my_animations.py line 97
        self.play(
            RemarkDashedRectangle(t2),
            RemarkDashedRectangle(t3,line_config={"stroke_width":3},color=PURPLE,margin=0.5)
        )
        self.wait(2)

class FreeHandExample(GenericExample):
    def construct(self):
        t1,t2,t3 = self.text_group
        # FreehandRectangle: my_objects.py - line 81
        t1_fh = FreehandRectangle(t1)
        t2_fh = FreehandRectangle(t2,margin=0.2,color=RED,stroke_width=2)
        t3_fh = FreehandRectangle(t3,margin=0.2,color=RED,fill_opacity=1,fill_color=PURPLE,partitions=20)
        self.bring_to_back(t3_fh)
        self.play(
            *list(map(ShowCreation,[t1_fh,t2_fh])), #<- This is a way to play multiple animations:
            # *list(map(Animation,mobs)), # mobs can be a list or a VGroup
            DrawBorderThenFill(t3_fh),
            *list(map(Write,[t1,t2,t3])),
        )
        self.wait(2)

class FreeHandExample2(GenericPaths):
    def construct(self):
        p1,p2,p3 = self.path_group
        # FreehandDraw: my_objects.py - line 56
        p1_fh = FreehandDraw(p1,close=True)
        p2_fh = FreehandDraw(p2,close=True,color=RED,partitions=30,dx_random=2)
        p3_fh = FreehandDraw(p3,partitions=20,dx_random=1)
        fh_group = VGroup(p1_fh,p2_fh,p3_fh)
        self.wait()
        self.play(
            *[ReplacementTransform(mob1,mob2) for mob1,mob2 in zip(self.path_group,fh_group)]
        )
        self.wait(2)

class Zig(Scene):
    def construct(self):
        path = TextMobject("This is wrong").scale(2)
        # ZigZag: my_objects.py - line 110
        draw = ZigZag(path,color=RED,stroke_width=10)
        self.add(path)
        self.wait(1.5)
        self.play(ShowCreation(draw,run_time=1,rate_func=linear))
        self.wait(2)

def custom_time(t,partitions,start,end,func):
    duration = end - start
    fragment_time = 1 / partitions
    start_time = start * fragment_time
    end_time = end * fragment_time
    duration_time = duration * fragment_time
    def fix_time(x):
        return (x - start_time) / duration_time
    if t < start_time: 
        return func(fix_time(start_time))
    elif start_time <= t and t < end_time:
        return func(fix_time(t))
    else:
        return func(fix_time(end_time))

def Custom(partitions,start,end,func=smooth):
    return lambda t: custom_time(t,partitions,start,end,func)

class StartAnimationInTheMiddleOfAnother(Scene):
    def construct(self):
        c = Circle().scale(2)
        s = Square().scale(2)
        l = Line(DOWN,UP).scale(2)
        time = DecimalNumber(self.time).add_updater(lambda m: m.set_value(self.time))
        time.to_corner(DL)
        self.add(time)
        self.play(
            # 6 partitions, that is (total_time = 4):
            # ShowCreation starts at t=(0/6)*total_time=0s and end t=(5/6)*total_time=3.333s
            ShowCreation(c,  rate_func=Custom(6,0,5)),
            # FadeIn starts at t=(2/6)*total_time=1.3333s and end t=(4/6)*total_time=2.6666s
            FadeIn(s,        rate_func=Custom(6,2,4,func=there_and_back)),
            # GrowFromCenter starts at t=(4/6)*total_time=2.6666s and end t=(6/6)*total_time=4s
            GrowFromCenter(l,rate_func=Custom(6,4,6)),
            run_time=4 # <- total_time
            )
        self.wait()

class MeasureObject1(Scene):
    def construct(self):
        square=Square()
        measure_line=Line(square.get_corner(DL),square.get_corner(UL))
        # MeasureDistance: my_objects.py - line 143
        measure=MeasureDistance(measure_line).add_tips()
        measure_tex=measure.get_tex("x")
        self.add(square,measure,measure_tex)
        self.wait(2)

class MeasureObject2(Scene):
    def construct(self):
        triangle = RegularPolygon(n=3)
        #Vertices
        triangle.vertices_text = VMobject()
        triangle.vertices_text.add_updater(lambda mob: mob.become(self.get_triangle_vertices(triangle)))
        #Measure side
        triangle.measure1 = VMobject()
        triangle.measure1.add_updater(self.get_updater_side(triangle,0,1,"a"))
        triangle.measure2 = VMobject()
        triangle.measure2.add_updater(self.get_updater_side(triangle,1,2,"b",color=TEAL))
        #Sides
        self.add(triangle,triangle.vertices_text,triangle.measure1,triangle.measure2)
        self.wait()
        self.play(triangle.scale,[5,2,1])
        self.wait()
        self.play(triangle.scale,[0.7,2,1])
        self.wait(2)

    def get_triangle_vertices(self,mob,buff=0.3):
        vertices = mob.get_vertices()
        vertices_text = VGroup(*[
            Text(f"{v}",height=2,stroke_width=0,font="Times")\
            .move_to(mob.get_center()+(vert-mob.get_center())*(buff/get_norm(vert)+1))
            for v,vert in zip(range(len(vertices)),vertices)]
            )
        return vertices_text

    def get_measure_side(self,mob,vert1,vert2,tex,buff=2,**kwargs):
        vertices = mob.get_vertices()
        side = Line(vertices[vert2],vertices[vert1])
        return MeasureDistance(side,**kwargs).add_tips().add_letter(tex,buff=buff)

    def get_updater_side(self,*args,**kwargs):
        return lambda mob: mob.become(self.get_measure_side(*args,**kwargs))

class PatternExample(Scene):
    def construct(self):
        # RectanglePattern: my_objects.py - line 283
        pattern_1=RectanglePattern(4,2)
        pattern_2=RectanglePattern(3,add_rectangle=True)
        pattern_3=RectanglePattern(3,6,color=ORANGE)
        pg=VGroup(pattern_1,pattern_2,pattern_3).arrange(RIGHT)
        self.add(pg)
        self.wait()

class FadeInFromEdgesExample(FormulaExample):
    def construct(self):
        # if your TexMobject have one dimension, that is:
        # tex = TexMobject("SingleFormula")
        # Then you have to use FadeInFromEdges(tex[0])
        # If your TexMobject have multiple formulas, that is:
        # tex = TexMobject("Multiple","Formula")
        # Then you have to specify the number of array, that is:
        # FadeInFromEdges(tex[0]) or FadeInFromEdges(tex[1])
        # Same rules to FadeInFromDirections and FadeInFromRandom
        self.play(
            FadeInFromEdges(self.tex_example[0]),
            run_time=3
        )
        self.wait()

class FadeInFromDirectionsExample(FormulaExample):
    def construct(self):
        self.play(
            FadeInFromDirections(self.tex_example[0]),
            run_time=3
        )
        self.wait()

class FadeInFromRandomExample(FormulaExample):
    def construct(self):
        self.play(
            FadeInFromRandom(self.tex_example[0]),
            run_time=3
        )
        self.wait()
