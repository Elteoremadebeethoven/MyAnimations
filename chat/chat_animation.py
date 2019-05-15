#Only it works in previous versions of February 3, 2019

from big_ol_pile_of_manim_imports import *

from my_animations.chat.chat_code import *

class Chat(Scene):
    def construct(self):
        conversation = Conversation(self)
        conversation.add_bubble("Hi!")
        self.wait(2)
        conversation.add_bubble("Hi! Whats up!")
        self.wait(2)
        conversation.add_bubble("This is my first animation of chat")
        self.wait(3) # 41
        conversation.add_bubble("That's awesome")
        self.wait(2) # 48
        conversation.add_bubble("Thanks")
        self.wait(2)
        self.play(FadeOut(conversation.dialog[:]))
        self.wait()
