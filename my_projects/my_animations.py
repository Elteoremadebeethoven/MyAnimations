from manimlib.imports import *
from my_projects.my_objects import *

############# MY ANIMATIONS ############
class PassRectangleAbstract(UpdateFromAlphaFunc):
    CONFIG = {
        "run_time": 1.3,
        "remover": True,
        "margin":0.1,
        "max_opacity":0.6,
        "init_opacity":0.2,
        "color":YELLOW,
        "rectangle_kwargs":{
            "fill_opacity":1,
            "stroke_width":0,
        },
    }

    def __init__(self, mobject,midle_color=None,**kwargs):
        digest_config(self, kwargs)
        self.mobject = mobject
        self.rectangle_kwargs["color"] = self.color
        if midle_color == None:
            midle_color = self.rectangle_kwargs["color"]
        rectangle = Rectangle(
            height=mobject.get_height()+self.margin,
            width=mobject.get_width()+self.margin,
            **self.rectangle_kwargs
            )
        rectangle.move_to(mobject)
        reference_line_left = Line(rectangle.get_corner(UL),rectangle.get_corner(DL))
        reference_line_right = Line(rectangle.get_corner(UR),rectangle.get_corner(DR))
        rectangle.init_state = rectangle.copy()
        rectangle_width = rectangle.get_width()
        rest_opacity = 1 - self.init_opacity
        def return_updater(mob,alpha):
            dx = interpolate(-PI/2,PI/2,alpha)
            mob.become(mob.init_state)
            mob.set_width(rectangle_width*np.cos(dx),stretch=True)
            # dx should not be zero
            sign = -abs(dx)/(dx+0.00000000001)
            direction = LEFT*sign
            reference_line = Line(
                rectangle.init_state.get_corner(UP+direction),
                rectangle.init_state.get_corner(DOWN+direction)
            )
            mob.next_to(reference_line,-direction,buff=0)
            opacity = self.init_opacity + (self.max_opacity-self.init_opacity)*np.cos(dx)
            mob.set_style(fill_opacity=opacity)
            mob.set_color(interpolate_color(self.rectangle_kwargs["color"],midle_color,np.cos(dx)))

        super().__init__(
            rectangle,return_updater
        )

class PassRectangle(AnimationGroup):
    def __init__(self, mobject, **kwargs):
        digest_config(self, kwargs)
        super().__init__(
            PassRectangleAbstract(mobject,**kwargs),
            #The reason for this, is that mobject always be foreground
            Animation(mobject)
        )

# UnderlineIndication
class UnderlineIndication(AnimationGroup):
    CONFIG = {
        "line_config":{},
        "line_type":Line,
        "reverse":True,
        "run_time":1.5
    }
    def __init__(self, mobject,margin=0.1,buff=0.2,**kwargs):
        digest_config(self, kwargs)
        line = self.line_type(
            mobject.get_corner(DL)+margin*LEFT,
            mobject.get_corner(DR)+margin*RIGHT,
            **self.line_config
        )
        line.shift(buff*DOWN)
        if self.reverse:
            kwargs["rate_func"] = there_and_back
            kwargs["run_time"] = self.run_time*2
        if self.line_type == DashedLine:
            kwargs["run_time"] = self.run_time/2
            kwargs["rate_func"] = smooth
            kwargs["lag_ratio"] = 0.005
        super().__init__(self.return_animation(line,**kwargs))
    
    def return_animation(self,line,**kwargs):
        if self.line_type == Line:
            return ShowCreationThenDestruction(line,**kwargs)
        elif self.line_type == DashedLine:
            return LaggedStartMap(ShowCreationThenDestruction,line,**kwargs)

class RemarkDashedRectangle(LaggedStart):
    CONFIG = {
        "line_config":{},
        "line_kwargs":{},
        "run_time":1,
        "lag_ratio":0.02,
        "color":YELLOW,
        "margin":0.1
    }
    def __init__(self,mob,**kwargs):
        digest_config(self, kwargs)
        self.line_kwargs["margin"] = self.margin
        # SurroundingDashedRectangle: See my_objects.py line 44
        dr = SurroundingDashedRectangle(
            mob,
            color=self.color,
            line_config=self.line_config,
            **self.line_kwargs
        )
        super().__init__(
            *[ShowCreationThenDestruction(line) for d in dr for line in d],
            **kwargs)

class FadeInFromEdges(LaggedStart):
    def __init__(self, text , **kwargs):
        digest_config(self, kwargs)
        super().__init__(
            *[FadeInFromPoint(obj,point=self.get_vector_from(obj,dist=1.4))for obj in text],
            **kwargs
        )

    def get_vector_from(self,obj,point=ORIGIN,dist=2):
            vect=obj.get_center()-point
            return vect*dist


class FadeInFromDirections(LaggedStart):
    CONFIG = {
        "directions":[DL,DOWN,DR,RIGHT,UR,UP,UL,LEFT],
        "magnitude":1
    }
    def __init__(self, text , **kwargs):
        digest_config(self, kwargs)
        self.reverse_directions=it.cycle(list(reversed(self.directions)))
        super().__init__(
            *[FadeInFromPoint(obj,point=obj.get_center()+d*self.magnitude)
                for obj,d in zip(text,self.reverse_directions)],
            **kwargs
        )

class FadeInFromRandom(LaggedStart):
    CONFIG = {
        "directions":[DL,DOWN,DR,RIGHT,UR,UP,UL,LEFT],
        "magnitude":0.5,
        "lag_ratio":0
    }
    def __init__(self, text , **kwargs):
        digest_config(self, kwargs)
        super().__init__(
            *[FadeInFromPoint(obj,point=random.choice(self.directions)*self.magnitude)
                for obj in text],
            **kwargs
        )