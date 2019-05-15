#from big_ol_pile_of_manim_imports import *
from manimlib.imports import *
from my_animations.chat.chat_code import *

class Chat(Scene):
    def construct(self):
        conversation = Conversation(self)
        conversation.add_bubble("Hola!")
        self.wait(2)
        conversation.add_bubble("Hola, qué tal?")
        self.wait(2)
        conversation.add_bubble("Esta es mi primera animación de\\\\ conversación.")
        self.wait(3) # 41
        conversation.add_bubble("Está muy bien!")
        self.wait(2) # 48
        conversation.add_bubble("Gracias! :D")
        self.wait(2)
        self.play(FadeOut(conversation.dialog[:]))
        self.wait()