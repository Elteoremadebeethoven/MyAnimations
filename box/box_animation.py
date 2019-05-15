#from big_ol_pile_of_manim_imports import *
from manimlib.imports import *
from MyAnimations.box.box_object import *


class BoxAnimation(Scene):
    def construct(self):
        #Set objects
        box=Box()
        note=NoteBox()
        label=TexMobject("A",color=BLACK)
        #Set properties
        note.set_height(label.get_height()*2)
        note.move_to(box)
        label.move_to(note)

        self.play(DrawBorderThenFill(box))
        self.wait()
        self.play(FadeIn(note))
        note.add_updater(lambda d: d.move_to(box.box_center()))
        self.play(Write(label))
        label.add_updater(lambda d: d.move_to(note))


        self.play(box.shift,DOWN*3+LEFT*2,path_arc=PI/4)
        self.wait()
        self.play(open_box(box))

        self.play(box.shift,UP*4.5+RIGHT*4)
        self.wait()
        self.play(close_box(box))
        self.wait()
