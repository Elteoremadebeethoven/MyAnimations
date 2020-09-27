from manimlib.imports import *
from io import *

def get_sign_from_even(n):
    return 1 if n % 2 == 0 else -1

def get_dim_from_vector(vector):
    for i, dim in enumerate(vector):
        if abs(dim) == 1:
            return i

def return_random_from_word(word):
    rango = list(range(len(word)))
    random.shuffle(rango)
    return rango

def return_random_direction(word):
    return [random.choice([UP,DOWN]) for _ in range(len(word))]

def get_random_coord(r_x,r_y,step_x,step_y):
    range_x = list(range(r_x[0],r_x[1],step_x))
    range_y = list(range(r_y[0],r_y[1],step_y))
    select_x = random.choice(range_x)
    select_y = random.choice(range_y)
    return np.array([select_x,select_y,0])

def return_random_coords(word,r_x,r_y,step_x,step_y):
    rango = range(len(word))
    return [word.get_center() + get_random_coord(r_x,r_y,step_x,step_y) for _ in rango]

class WriteRandom(LaggedStart):
    CONFIG = {
        "lag_ratio":0.1,
        "run_time":2.5,
        "anim_kwargs":{},
        "anim_type":Write
    }
    def __init__(self,text,**kwargs):
        digest_config(self, kwargs)
        super().__init__(*[
            self.anim_type(text[i],**self.anim_kwargs)
            for i in return_random_from_word(text)
        ])

class UnWriteRandom(WriteRandom):
    CONFIG = {
        "run_time": 2,
        "anim_kwargs": {
            "rate_func": lambda t: smooth(1-t)
        },
        "remover": True,
    }

class FadeOutRandom(WriteRandom):
    CONFIG = {
        "anim_type": FadeOut
    }


class FadeOutFromRandom(LaggedStart):
    CONFIG = {
        "lag_ratio": 0.08,
        "anim_type": FadeInFrom,
        "anim_kwargs": {}
    }
    def __init__(self,text,**kwargs):
        digest_config(self, kwargs)
        super().__init__(*[
            self.anim_type(text[i],d,**self.anim_kwargs)
            for i,d in zip(return_random_from_word(text),return_random_direction(text))
        ])


class KeyboardScene(Scene):
    CONFIG = {
        "lag": 0.07,
        "rate_factor": 0.03,
        "time_factor": 0.129,
        "lag_spaces": 0.2,
        "range_random": 4,
        "random_seed": 2,
    }
    def keyboard(self, text):
        def return_random():
            return random.randint(1, self.range_random)
        for i in range(len(text)):
            self.add_sound("typewriter/key%s"%return_random())
            text[i].set_fill(None, 1)
            self.play(LaggedStartMap(FadeIn, 
                        text[i], run_time=self.rate_factor*len(text[i]),
                        lag_ratio=self.lag/len(text[i])))
            self.wait(0.4*(random.uniform(1.25, 2.3))*self.time_factor)
            if i < len(text) - 1:
                pre_ty = text[i].get_center()[1]
                pre_tx = text[i].get_center()[0]
                pos_ty = text[i+1].get_center()[1]
                pos_tx = text[i+1].get_center()[0]
                pre_width = text[i].get_width() / 2
                pos_width = text[i+1].get_width() / 2
                pre_height = text[i].get_height() / 2
                pos_height = text[i+1].get_height() / 2
                dist_min_x = (pre_width + pos_width) * 1.6
                dist_min_y = (pre_height + pos_height) * 1.2
                if i == 0 or dist_max_x < dist_min_x:
                    dist_max_x = dist_min_x
                if i == 0 or dist_max_y < dist_min_y:
                    dist_max_y = dist_min_y
                if abs(pre_ty - pos_ty) > dist_max_y:
                    self.add_sound("keyboard/enter")
                    self.wait(self.time_factor)
                elif abs(pre_tx - pos_tx) > dist_max_x and abs(pre_ty - pos_ty) < dist_max_y:
                    self.add_sound("keyboard/space")
                    self.wait(self.time_factor)
            if i == len(text) - 1:
                self.add_sound("keyboard/enter")
                self.wait(self.time_factor)

def return_tex_template(width):
    with open(TEMPLATE_TEX_FILE, "r") as infile:
        PRE_JUSTIFY_TEXT = infile.read()
        JUSTIFY_TEXT = PRE_JUSTIFY_TEXT.replace(
        TEX_TEXT_TO_REPLACE,
        "\\begin{tabular}{p{%s cm}}"%width + TEX_TEXT_TO_REPLACE + "\\end{tabular}")
        return JUSTIFY_TEXT

class TextJustify(TexMobject):
    CONFIG = {
        "alignment": "\\centering",
        "arg_separator": "",
        "text_width_line": 7
    }
    def __init__(self,tex_string, **kwargs):
        digest_config(self, kwargs)
        assert(isinstance(tex_string, str))
        self.tex_string = tex_string
        file_name = tex_to_svg_file(
            self.get_modified_expression(tex_string),
            return_tex_template(self.text_width_line)
        )
        SVGMobject.__init__(self, file_name=file_name, **kwargs)
        if self.height is None:
            self.scale(TEX_MOB_SCALE_FACTOR)
        if self.organize_left_to_right:
            self.organize_submobjects_left_to_right()

# Animations in


# Animations out

COLORS = it.cycle([RED, TEAL, BLUE, GREEN, PINK, PURPLE])
POLYGON_COLORS = it.cycle([TEAL,BLUE_B,YELLOW,RED_B])
SIDES_POLYGONS = it.cycle([3,4,5,6,7])


class CenterTextScene(KeyboardScene, ThreeDScene):
    CONFIG = {
        "script_name": "manim_ends",
        "index_paragraphs": [0,1],
        # 1. Keyboard
        # 2. TransformFromPolygon
        # 3. FadeInFromBlackRectangle
        # 4. ShowFromDowm
        # 5. FadeInFrom3DCamera
        # 6. FadeInFrom3DRotate
        # 7. Write
        # 8. FadeIn
        # 9. FromOutCamera: left, right, down, left
        # 10. LineDelivery
        "animation_in": "FadeInFromBlackRectangle",
        # 1. Fall
        # 2. FadeOutRandom
        # 3. FadeOutToBlackRectangle
        # 4. FallWithAcceleration
        # 5. FadeOutFrom3DCamera
        # 6. FadeOutFrom3DRotate
        # 7. UnWriteAll
        # 8. FadeOut
        # 9. ToOutCamera: left, right, down, left
        # 10. StealLines
        "animation_out": "FadeOutToBlackRectangle",
        "animation_kwargs_in": {
            "direction": RIGHT,
            "phi": 0,
            "run_time": 1
        },
        "animation_kwargs_out": {"direction": RIGHT, "run_time": 3},
        "pause_at_start": 0.1,
        "middle_pauses": [2,2],
        "colored_text": [
            (0, [RED, 3, 4]),
            (1, [TEAL, 4, 6])
        ],
        "test_code": True,
        "align_text": {
            #"1": r"\flushleft "
        }
    }
    def setup(self):
        paragraph = open(f"guiones/{self.script_name}.txt","r")
        paragraph = paragraph.readlines()
        self.all_paragraph = paragraph
        ThreeDScene.setup(self)
        # MovingCameraScene.setup(self)

    def set_color_text(self):
        for color_settings in self.colored_text:
            formula = self.texts[color_settings[0]]
            color, start, end = color_settings[1]
            formula[start:end+1].set_color(color)

    def get_pre(self,i):
        try:
            align = self.align_text[str(i)]
            return align
        except:
            pre = fr"\tt {align}" if self.animation_in == "Keyboard" else ""
            return pre

    def construct(self):
        
        texts = VGroup(*[
            TextJustify(fr"{self.get_pre(i)}{self.all_paragraph[i]}")
            for i in self.index_paragraphs
        ]).arrange(DOWN,buff=0.5)
        texts.set_width(FRAME_WIDTH-1)
        self.texts = texts
        self.texts_0 = VGroup(*[mob[0] for mob in self.texts])
        self.signs = it.cycle([1,-1])
        self.group_black_rectangles = VGroup()
        self.all_words = VGroup(*[
            mob
            for submob in self.texts
            for mob in submob
        ])
        self.set_color_text()
        if not self.test_code:
            for i,paragraph in enumerate(texts):
                try:
                    phi = self.animation_kwargs_in["phi"]
                    if self.animation_kwargs_in == "FadeOutFrom3DCamera" and phi > 0:
                        try_break = True
                        sub_paragraph = self.all_word
                    else:
                        try_break = False
                        sub_paragraph = paragraph
                except:
                    sub_paragraph = paragraph
                    try_break = False
                self.show_text(sub_paragraph)
                try: 
                    self.wait(self.middle_pauses[i])
                except:
                    self.wait(min(*self.middle_pauses))
                if try_break:
                    break
            self.remove_text()
            self.wait()
        else:
            for paragraph in self.texts:
                self.show_numbers(paragraph)

    def show_text(self,paragraph):
        if self.animation_in == "Keyboard":
            self.keyboard_scene(paragraph,**self.animation_kwargs_in)
        elif self.animation_in == "TransformFromPolygon":
            self.transform_from_polygon(paragraph,**self.animation_kwargs_in)
        elif self.animation_in == "FadeInFromBlackRectangle":
            self.fade_in_from_black_rectangle(paragraph,**self.animation_kwargs_in)
        elif self.animation_in == "ShowFromDowm":
            self.show_from_down(paragraph,**self.animation_kwargs_in)
        elif self.animation_in == "FadeInFrom3DCamera":
            self.fade_in_from_3d_camera(paragraph,**self.animation_kwargs_in)
        elif self.animation_in == "FadeInFrom3DRotate":
            self.fade_in_from_3d_rotate(paragraph,**self.animation_kwargs_in)
        elif self.animation_in == "Write":
            self.write_one_by_one(paragraph,**self.animation_kwargs_in)
        elif self.animation_in == "FadeIn":
            self.fade_in_one_by_one(paragraph,**self.animation_kwargs_in)
        elif self.animation_in == "FromOutCamera":
            self.from_out_camera(paragraph,**self.animation_kwargs_in)
        elif self.animation_in == "LineDelivery":
            self.line_delivery(paragraph,**self.animation_kwargs_in)
        else:
            print("There is not animation in")

    # methods definitions in
    def keyboard_scene(self, paragraph, *args, **kwargs):
        self.keyboard(paragraph)

    def transform_from_polygon(self, paragraph, *args, scale=7,sides=SIDES_POLYGONS, cycle_colors=POLYGON_COLORS, **kwargs):
        polygons = VGroup(*[
            RegularPolygon(n,stroke_opacity=0,color=colors)
                .match_width(t)
                .scale(scale)
                .move_to(t)
            for t, n, colors in zip(paragraph,sides,cycle_colors)
        ])
        self.play(
            LaggedStart(*[
                TransformFromCopy(
                    c, t
                )
                for c, t in zip(polygons, paragraph)
            ]),
            **kwargs
        )

    def fade_in_from_black_rectangle(self, paragraph, *args, **kwargs):
        black_rectangles = VGroup(*[
            Rectangle(
                width=mob.get_width(),
                height=mob.get_height(),
                color=BLACK,
                fill_opacity=1,
                stroke_width=0
            ).next_to(mob,DOWN,buff=0)
            for mob in paragraph
        ])
        touple_mob = [*zip(paragraph, black_rectangles)]
        for t,rectangle in touple_mob:
            t.save_state()
            t.scale(0.9)
            t.move_to(rectangle)

        self.play(
            LaggedStart(*[
                AnimationGroup(
                    Restore(t),
                    Animation(rectangle)
                )
                for t, rectangle in touple_mob
            ]),
            **kwargs
        )
        self.group_black_rectangles.add(black_rectangles)

    def show_from_down(self, paragraph, *args, **kwargs):
        pass

    def fade_in_from_3d_camera(self, paragraph,*args, random_range=[-5,5], phi=0, **kwargs):
        for mob in paragraph:
            for submob in mob:
                submob.save_state()
                submob.set_z(random.randint(*random_range))

        if phi != 0:
            self.set_camera_orientation(phi=phi)
        self.play(
            FadeIn(paragraph),
            run_time=kwargs["run_time"]/2
        )
        self.move_camera(phi=0,added_anims=[
            AnimationGroup(*[
                Restore(mob)
                for mob in paragraph
            ],
            **kwargs
            )
        ])


    def fade_in_from_3d_rotate(self, paragraph, *args, **kwargs):
        for mob in paragraph:
            mob.save_state()
            mob.rotate(PI/2, axis=UP)
            mob.fade(1)
        
        self.play(
            LaggedStart(*[
                Restore(mob) 
                for mob in paragraph
            ]),
            **kwargs
        )

    def write_one_by_one(self, paragraph, *args, **kwargs):
        self.play(
            Write(paragraph),
            **kwargs
        )

    def fade_in_one_by_one(self, paragraph, *args, **kwargs):
        self.play(
            LaggedStart(*[
                Write(letter) for letter in paragraph
            ]),
            **kwargs
        )

    def from_out_camera(self, paragraph, *args, direction=UP,**kwargs):
        try:
            d = kwargs["direction"]
        except:
            d = direction

        camera_rectangle = Rectangle(
            width=FRAME_WIDTH,
            height=FRAME_HEIGHT
        )
        sign = next(self.signs)
        coord = get_dim_from_vector(d)
        paragraph.save_state()
        paragraph.set_coord(
            (camera_rectangle.get_edge_center(d)[coord] + paragraph.length_over_dim(coord) * d[coord] / 2) * sign,
            coord,
        )
        self.play(
            Restore(paragraph),**kwargs
        )

    def line_delivery(self, paragraph, *args, **kwargs):
        pass

    def remove_text(self):
        if self.animation_out == "Fall":
            self.fall(**self.animation_kwargs_out)
        elif self.animation_out == "FadeOutRandom":
            self.fade_out_random(**self.animation_kwargs_out)
        elif self.animation_out == "FadeOutToBlackRectangle":
            self.fade_out_from_black_rectangle(**self.animation_kwargs_out)
        elif self.animation_out == "FallWithAcceleration":
            self.fall_with_acceleration(**self.animation_kwargs_out)
        elif self.animation_out == "FadeOutFrom3DCamera":
            self.fade_out_from_3d_camera(**self.animation_kwargs_out)
        elif self.animation_out == "FadeOutFrom3DRotate":
            self.fade_out_from_3d_rotate(**self.animation_kwargs_out)
        elif self.animation_out == "UnWriteAll":
            self.unwrite_all(**self.animation_kwargs_out)
        elif self.animation_out == "FadeOut":
            self.fade_out_one_by_one(**self.animation_kwargs_out)
        elif self.animation_out == "ToOutCamera":
            self.to_out_camera(**self.animation_kwargs_out)
        elif self.animation_out == "StealLines":
            self.steal_lines(**self.animation_kwargs_out)
        else:
            print("There is not animation in")

    # methods definitions out
    def fall(self, *args, **kwargs):
        sigs = it.cycle([-1,1])
        self.play(
            LaggedStart(*[
                Rotate(paragraph,
                    - PI/2 * next(sigs),
                    run_time=2,
                    about_point=[next(sigs)*FRAME_X_RADIUS,-next(sigs)*FRAME_Y_RADIUS,0]
                )
                for paragraph in self.texts
                ],
                lag_ratio=0.2,
                **kwargs
            )
        )

    def fade_out_random(self, *args, **kwargs):
        self.play(
            FadeOutRandom(self.all_words),
            **kwargs
        )

    def fade_out_from_black_rectangle(self, *args, **kwargs):
        if len(self.group_black_rectangles) == 0:
            for paragraph in self.texts:
                black_rectangles = VGroup(*[
                    Rectangle(
                        width=mob.get_width(),
                        height=mob.get_height(),
                        color=BLACK,
                        fill_opacity=1,
                        stroke_width=0
                    ).next_to(mob,DOWN,buff=0)
                    for mob in paragraph
                    ])
                self.group_black_rectangles.add(black_rectangles)
        shuffle_letters, shuffle_rectangles = self.get_shuffle_lists_and_rectangles()
        self.play(*[
            LaggedStart(*[
                AnimationGroup(
                    ApplyFunction(
                        lambda mob: mob.next_to(mob,DOWN,buff=0).scale(0.9),
                        paragraph[i]
                    ),
                    Animation(rectangles[i])
                )
                for i in range(len(paragraph))
                ]
            )
            for paragraph, rectangles in zip(shuffle_letters, shuffle_rectangles)
            ],
            **kwargs
        )

    def fall_with_acceleration(self, *args, **kwargs):
        pass

    def fade_out_from_3d_camera(self, *args, random_range=[-5,5], **kwargs):
        shuffle_letters = self.get_shuffle_lists()
        for mob in shuffle_letters:
            for submob in mob:
                submob.generate_target()
                submob.target.set_z(random.randint(*random_range))
                submob.target.fade(1)

        self.play(
            LaggedStart(*[
                MoveToTarget(mob)
                for submob in shuffle_letters
                for mob in submob
            ]),
            **kwargs
        )


    def fade_out_from_3d_rotate(self, *args, **kwargs):
        paragraph = self.get_shuffle_lists()
        for mob in paragraph:
            for submob in mob:
                submob.generate_target()
                submob.target.rotate(PI/2, axis=UP)
                submob.target.fade(1)

        self.play(*[
            AnimationGroup(*[
                LaggedStart(*[
                        MoveToTarget(submob)
                        for submob in mob 
                    ])
                ])
                for mob in paragraph
            ],
            **kwargs
        )

    def unwrite_all(self, *args, **kwargs):
        shuffle_letters = self.get_shuffle_lists()
        self.play(
            LaggedStart(*[
                UnWriteRandom(paragraph) 
                for paragraph in shuffle_letters
            ]),
            **kwargs
        )

    def fade_out_one_by_one(self, *args, **kwargs):
        shuffle_letters = self.get_shuffle_lists()
        self.play(
            LaggedStart(*[
                FadeOutRandom(paragraph) 
                for paragraph in shuffle_letters
            ]),
            **kwargs
        )

    def to_out_camera(self,*args, direction=LEFT,**kwargs):
        try:
            d = kwargs["direction"]
        except:
            d = direction
        camera_rectangle = Rectangle(
            width=FRAME_WIDTH,
            height=FRAME_HEIGHT
        )

        coord = get_dim_from_vector(d)
        self.play(
            AnimationGroup(*[
                ApplyMethod(
                    paragraph.set_coord,
                    (camera_rectangle.get_edge_center(d)[coord] + paragraph.length_over_dim(coord) * d[coord] / 2) * get_sign_from_even(i),
                    coord,
                )
                for i, paragraph in enumerate(self.texts)
            ]),
            **kwargs
        )

    def steal_lines(self, *args, **kwargs):
        pass

    def show_numbers(self, text, height=0.15, buff=0):
            colors = it.cycle(COLORS)
            numbers = VGroup(*[
                Text(f"{i}", font="Arial", height=height)
                    .next_to(mob,DOWN,buff=buff)
                    .set_color(next(colors))
                for i,mob in enumerate(text)
            ])
            self.add(text, numbers)

    def get_shuffle_lists(self, rectangles=False):
        n_paragraphs = len(self.texts)
        shuffle_letters = VGroup()
        for paragraph in self.texts:
            paragraph_0 = paragraph
            array = [*range(len(paragraph_0))]
            random.shuffle(array)
            shuffle_letters.add(
                VGroup(*[paragraph_0[i] for i in array])
            )
        return shuffle_letters

    def get_shuffle_lists_and_rectangles(self):
        n_paragraphs = len(self.texts)
        shuffle_letters = VGroup()
        shuffle_rectangles = VGroup()
        for paragraph,rects in zip(self.texts,self.group_black_rectangles):
            array = [*range(len(paragraph))]
            random.shuffle(array)
            shuffle_letters.add(
                VGroup(*[paragraph[i] for i in array])
            )
            shuffle_rectangles.add(
                VGroup(*[rects[i] for i in array])
            )
        return shuffle_letters, shuffle_rectangles
