#from big_ol_pile_of_manim_imports import *
from manimlib.imports import *

from MyAnimations.omega_creature.omega_creature_class import *


class OmegaDice(Scene):
    def construct(self):
        Ale=Alex().to_edge(DOWN)
        palabras_ale = TextMobject("Learn to do \\\\animations with me!!")
        self.add(Ale)
        self.play(OmegaCreatureSays(
            Ale, palabras_ale, 
            bubble_kwargs = {"height" : 4, "width" : 6},
            target_mode="speaking"
        ))
        self.wait()
        self.play(Blink(Ale))
        self.wait(1)
        self.play(Blink(Ale))
        self.wait(1)
        self.play(Blink(Ale))
        self.wait(1)
        self.play(Blink(Ale))
        self.wait(1)