# Works in ManimCE 0.5.0

from manim import *

scripts = [
"""
This problem is equivalent to Zeno's paradox.
""",
"""
To simplify the problem, let's 
imagine a clock at 00:00.
""",
"""
We chose this state because it is easier to 
study, and both hands are crossed.
""",
"""It is evident that the hands take more than 
an hour to cross.""",
"""The problem starts here.""",
r"""
Now, if the minute hand \\
advances $5$ minutes, the\\ 
hour hand will advance\\
$\frac{5}{60}$ hours.
""",
r"""
In the same way, if the\\
minute hand advances $\frac{5}{60}$\\
minutes, the hour hand will\\
advance $\frac{5}{60\times 12}$, that is $\frac{1}{12^2}$.
""",
r"""
We can clearly see that there\\
is a series of sums equivalent\\
to Zenon's paradox, but instead\\
of being $\frac{1}{2^n}$ it is $\frac{1}{12^n}$.
""",
r"""
We solve the problem with:\\
$\displaystyle 60[{\rm min}] \times\sum_{i=0}^{\infty} \frac{1}{12^i} \approx 65.454545 [{\rm min}]$.
""",
]

class Clock(VGroup):
    def __init__(self, hh=0, mh=0, radius=3, color=WHITE,**kwargs):
        super().__init__(**kwargs)
        # Define body
        body = Circle(radius=radius,color=WHITE)
        body.flip()
        body.rotate(- 4 * 360/12 * DEGREES)
        self.body = body
        center_body = Dot(body.get_center())
        numbers = self.get_numbers(body)
        ticks = self.get_ticks(body)

        # Define hour
        hour = hh + mh / 60
        hour_tracker = ValueTracker(hour)
        self.ht = hour_tracker

        # Define hands
        minute_hand = self.get_minute_hand(body, hour_tracker.get_value()%1*60)
        hour_hand = self.get_hour_hand(body, hour_tracker.get_value())

        # Define dashed lines
        dashed_lines = self.get_dashed_lines(body, hour_hand, minute_hand)
        self.dl = dashed_lines

        self.hh = hour_hand
        self.mh = minute_hand

        self.add(
            body,
            ticks,
            numbers,
            minute_hand,
            hour_hand,
            dashed_lines,
            center_body,
        )

    def add_updaters(self):
        self.mh.add_updater(
            lambda mob: mob.become(
                self.get_minute_hand(self.body,self.ht.get_value()%1*60))
        )
        self.hh.add_updater(
            lambda mob: mob.become(
                self.get_hour_hand(
                    self.body,
                    self.ht.get_value()
                )
            )
        )
        self.dl.add_updater(
            lambda mob: mob.become(
                self.get_dashed_lines(self.body, self.hh, self.mh)
            )
        )

    def suspend_updaters(self):
        for mob in [self.mh,self.hh,self.dl]:
            mob.suspend_updating()

    def resume_updaters(self):
        for mob in [self.mh,self.hh,self.dl]:
            mob.resume_updating()

        
    def get_hour_hand(self, body: Circle, hour, a_prop=0.4):
        # print("Hour from class: " + str(hour))
        prop = hour / 12
        guide_line = Line(
            body.get_center(),
            body.point_from_proportion(prop%1)
        )
        hour_hand =  Arrow(
            body.get_center(),
            guide_line.point_from_proportion(a_prop),
            buff=0,
            color=RED
        )
        hour_hand.rotate(2*PI/12,about_point=body.get_center())
        return hour_hand

    def get_minute_hand(self, body: Circle, minutes, a_prop=0.7):
        prop = minutes / 60
        guide_line = Line(
            body.get_center(),
            body.point_from_proportion(prop%1)
        )
        hour_hand =  Arrow(
            body.get_center(),
            guide_line.point_from_proportion(a_prop),
            buff=0,
            color=BLUE
        )
        hour_hand.rotate(2*PI/12,about_point=body.get_center())
        return hour_hand

    def get_dashed_lines(self, body: Circle, hh: Arrow, mh: Arrow):
        hhv = hh.get_unit_vector()
        mhv = mh.get_unit_vector()

        hhd = Line(
            body.get_center(),
            body.get_center() + hhv * self.body.height*0.97 / 2,
            color=hh.get_color(),
            stroke_width=1
        )
        mhd = Line(
            body.get_center(),
            body.get_center() + mhv * self.body.height*0.97 / 2,
            color=mh.get_color(),
            stroke_width=1
        )
        return VGroup(hhd, mhd)

    def get_numbers(self, body: Circle, prop=0.85, scale=0.8):
        numbers = VGroup(*[Tex(f"{i}") for i in list(range(1,13))])
        for i,n in enumerate(numbers):
            point = body.point_from_proportion(i/12)
            guide_line = Line(body.get_center(),point)
            n.scale(scale)
            n.move_to(guide_line.point_from_proportion(prop))
        return numbers

    def get_ticks(self, body: Circle, size_prop=0.04, stroke_width=1):
        ticks = VGroup()
        for i in range(60):
            point = body.point_from_proportion(i/60)
            guide_line = Line(body.get_center(),point)
            size = size_prop*2 if i % 5 == 0 else size_prop
            tick = Line(
                guide_line.point_from_proportion(1-size),
                point
            )
            ticks.add(tick)
        return ticks

class DigitalIntenger(VGroup,DecimalNumber):
    """
    Same as DecimalNumber only changed the indicated lines
    """
    def __init__(
        self,
        number=0,
        num_decimal_places=0,
        include_sign=False,
        group_with_commas=True,
        digit_to_digit_buff=0.05,
        show_ellipsis=False,
        unit=None,  # Aligned to bottom unless it starts with "^"
        include_background_rectangle=False,
        edge_to_fix=LEFT,
        ceros_at_left=1, # <- New argument.
        **kwargs
    ):
        super().__init__(**kwargs)
        self.number = number
        self.num_decimal_places = num_decimal_places
        self.include_sign = include_sign
        self.group_with_commas = group_with_commas
        self.digit_to_digit_buff = digit_to_digit_buff
        self.show_ellipsis = show_ellipsis
        self.unit = unit
        self.include_background_rectangle = include_background_rectangle
        self.edge_to_fix = edge_to_fix

        self.initial_config = kwargs.copy()
        self.initial_config.update(
            {
                "num_decimal_places": num_decimal_places,
                "include_sign": include_sign,
                "group_with_commas": group_with_commas,
                "digit_to_digit_buff": digit_to_digit_buff,
                "show_ellipsis": show_ellipsis,
                "unit": unit,
                "include_background_rectangle": include_background_rectangle,
                "edge_to_fix": edge_to_fix,
            }
        )

        if isinstance(number, complex):
            formatter = self.get_complex_formatter()
        else:
            formatter = self.get_formatter()
        num_string = formatter.format(number)

        rounded_num = np.round(number, self.num_decimal_places)
        if num_string.startswith("-") and rounded_num == 0:
            if self.include_sign:
                num_string = "+" + num_string[1:]
            else:
                num_string = num_string[1:]
        # CHANGES HERE !!!----------------------------
        if ceros_at_left > 0:
            if not len(num_string) > 1:
                num_string = "0"*ceros_at_left + num_string
        # --------------------------------------------

        self.add(*[SingleStringMathTex("\\tt "+char, **kwargs) for char in num_string])

        # Add non-numerical bits
        if self.show_ellipsis:
            self.add(SingleStringMathTex("\\dots"))

        if num_string.startswith("-"):
            minus = self.submobjects[0]
            minus.next_to(self.submobjects[1], LEFT, buff=self.digit_to_digit_buff)

        if self.unit is not None:
            self.unit_sign = SingleStringMathTex(self.unit, color=self.color)
            self.add(self.unit_sign)

        self.arrange(buff=self.digit_to_digit_buff, aligned_edge=DOWN)

        # Handle alignment of parts that should be aligned
        # to the bottom
        for i, c in enumerate(num_string):
            if c == "-" and len(num_string) > i + 1:
                self[i].align_to(self[i + 1], UP)
                self[i].shift(self[i + 1].height * DOWN / 2)
            elif c == ",":
                self[i].shift(self[i].height * DOWN / 2)
        if self.unit and self.unit.startswith("^"):
            self.unit_sign.align_to(self, UP)
        #
        if self.include_background_rectangle:
            self.add_background_rectangle()

class CrossedClockHands(ZoomedScene):
    def __init__(self, **kwargs):
        super().__init__(
            zoom_factor=0.3,
            zoomed_display_height=3,
            zoomed_display_width=6,
            image_frame_stroke_width=10,
            zoomed_camera_config={
                "default_frame_stroke_width": 3,
                },
            **kwargs
        )
    def construct(self):
        clock = Clock(0)
        clock.scale(0.9)
        clock.to_edge(UP)

        p = VGroup(*[Paragraph(scripts[i]) for i in range(5)])
        p[1].to_edge(DOWN)
        p[2].to_edge(DOWN)
        p[3].to_edge(DOWN)
        p[4].to_edge(DOWN)
        t = VGroup(*[
            Tex(scripts[i],tex_environment="flushleft").to_corner(DR)
            for i in range(5,8)
        ])
        t.add(Tex(scripts[-1]).to_corner(DR))
        self.play(Write(p[0]))
        self.wait(2)
        self.play(FadeTransform(p[0],p[1]))
        self.wait()
        self.play(Write(clock))
        self.wait()
        self.play(FadeTransform(p[1],p[2]))
        self.wait(3)
        self.play(FadeTransform(p[2],p[3]))
        clock.add_updaters()
        self.play(
            clock.ht.animate.set_value(1),
            run_time=4,
            rate_func=linear
        )
        self.wait(0.5)
        self.play(FadeTransform(p[3],p[4]))
        self.wait()
        clock.suspend_updaters()
        self.play(
            clock.animate
                .scale(1.2)
                .to_corner(UL),
            FadeTransform(p[4],t[0])
        )

        digital_hour = VGroup(Dot(),Dot(),Dot())

        def get_update_digital(ht,first_time=True):
            def update_digital(vg):
                h,d,m = vg
                vg_c = vg.copy()
                h.become(DigitalIntenger(np.floor(ht.get_value())%12))
                m.become(DigitalIntenger(np.floor(ht.get_value()%1*60)%60))
                vg.become(
                    VGroup(h,Tex(":"),m)
                        .arrange(RIGHT)
                        .scale(1.5)
                        .next_to(clock,DOWN)
                )
                if not first_time:
                    hc,dc,mc = vg_c
                    h.align_to(hc,LEFT)
                    d.move_to(dc)
                    m.align_to(mc,LEFT)
            return update_digital

        get_update_digital(clock.ht)(digital_hour)
        self.play(Write(digital_hour))
        digital_hour.add_updater(get_update_digital(clock.ht,False))
        # Create arc
        dl = clock.dl
        def get_dl_updater(dl_):
            def dl_updater(mob):
                start = dl_[0].get_end()
                end = dl_[1].get_end()
                angle = dl_[1].get_angle() - dl_[0].get_angle()
                sign = np.sign(angle)
                if angle > (65+5/12) / 60 * DEGREES:
                    mob.become(ArcBetweenPoints(start, end, sign * abs(angle), color=YELLOW))
                    mob.last_angle = angle
                else:
                    dx = interpolate(0,1,angle/mob.last_angle)
                    mob.become(ArcBetweenPoints(start, end, sign * abs(angle), color=YELLOW))
                    mob.set_stroke(opacity=dx)
            return dl_updater

        arc = VMobject().add_updater(get_dl_updater(dl))
        self.play(FadeIn(arc))

        zoomed_camera = self.zoomed_camera
        zoomed_display = self.zoomed_display
        frame = zoomed_camera.frame
        zoomed_display_frame = zoomed_display.display_frame

        frame.move_to(dl[0].get_end())
        frame.fade()
        zoomed_display_frame.fade()

        self.play(Create(frame))
        zd_rect = BackgroundRectangle(zoomed_display, fill_opacity=0, buff=MED_SMALL_BUFF)
        self.add_foreground_mobject(zd_rect)
        zd_rect.shift(LEFT*2)
        unfold_camera = UpdateFromFunc(zd_rect, lambda rect: rect.replace(zoomed_display))
        self.activate_zooming()

        self.play(self.get_zoomed_display_pop_out_animation(), unfold_camera)

        frame.add_updater(lambda mob: mob.move_to(dl[0].get_end()))
        self.play(
            clock.ht.animate.set_value(65.0005/60),
            run_time=5,
            rate_func=linear
        )
        self.wait()
        self.play(FadeTransform(t[0],t[1]))
        self.wait(2.5)
        self.play(
            frame.animate.scale(0.2),
            # Decrease the stroke of the lines in the zoomed camera
            self.decrease_cairo_stroke(0.4)
        )
        self.wait()
        dl_c = dl.copy()
        dl_c.clear_updaters()
        dl_c.set_color(GREY)
        self.bring_to_back(dl_c)
        self.play(
            clock.ht.animate.set_value((65 + 5/12 + 0.0001)/60),
            run_time=3,
            rate_func=linear
        )
        self.remove(dl_c)
        self.wait(2)
        self.play(FadeTransform(t[1],t[2]))
        self.wait(5)
        self.play(FadeTransform(t[2],t[3]))
        self.wait(2)
        self.play(
            clock.ht.animate.set_value(65.4545454545/60),
            run_time=3,
            rate_func=linear
        )

        self.wait(4)
        self.play(*list(map(FadeOut,self.mobjects)))
        self.wait(15)

    def decrease_cairo_stroke(self, proportion):
        start = self.zoomed_camera.cairo_line_width_multiple
        end = start * proportion
        def update(mob,alpha):
            v = interpolate(start, end, alpha)
            self.zoomed_camera.cairo_line_width_multiple = v
        return UpdateFromAlphaFunc(Mobject(), update)
