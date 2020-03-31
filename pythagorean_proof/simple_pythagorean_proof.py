
class PythagoreanProof(Scene):
    CONFIG = {
        "square_scale": 2,
    }
    def construct(self):
        left_square, right_square =  Square(), Square()
        VGroup(left_square,right_square)\
                .scale(self.square_scale)\
                .arrange_submobjects(RIGHT,buff=2)
        # FORMULAS
        theorem = TexMobject("c^2","=","a^2","+","b^2",color=BLUE).to_edge(DOWN)
        # FIRST SQUARE SETTINGS
        dots = [left_square.point_from_proportion(i * 1/4 + 1/16) for i in range(4)]
        dots_corners = [left_square.point_from_proportion(i * 1/4) for i in range(4)]
        triangles = VGroup(*[
            Polygon(
                dots[i],
                dots_corners[i],
                dots[i-1],
                stroke_width=0,
                fill_opacity=0.7
            )
            for i in range(4)
        ])
        # RIGHT SQUARE SETTINGS
        dots2 = [
                right_square.point_from_proportion(i * 1/4 + j * 1/16)
                for i,j in zip(range(4),[1,3,3,1])
        ]
        dots_corners2 = [right_square.point_from_proportion(i * 1/4) for i in range(4)]
        middle = np.array([dots2[0][0],dots2[1][1],0])

        all_rectangles = VGroup(*[
            Polygon(
                dots_corners2[i],
                dots2[i],
                middle,
                dots2[i-1],
            )
            for i in range(4)
        ])
        # rectancles: rectangles of the triangles
        rectangles = all_rectangles[0::2]
        # Big and small squares
        squares = all_rectangles[1::2]
        # IMPORTANT
        # use total_points = 3 if you are using the 3/feb release
        # use total_points = 4 if you are using the most recent release
        total_points = 3
        rect_dot = [
            [
                rectangles[i].points[total_points*j]
                for j in range(4)
            ]
            for i in range(2)
        ]
        triangles2 = VGroup(*[
            Polygon(
                rect[i+1],
                rect[i],
                rect[i-1],
                fill_opacity=0.7
            )
            for rect in rect_dot
            for i in [0,2]
        ])
        parts_theorem = VGroup(
            TexMobject("a^2").move_to(left_square),
            TexMobject("b^2").move_to(squares[0]),
            TexMobject("c^2").move_to(squares[1])
        )
        #print(len(triangles2))

        self.play(
            *list(map(DrawBorderThenFill,[left_square,right_square,triangles.copy()]))
        )
        #"""
        self.play(
            *[
                ApplyMethod(triangles[i].move_to,triangles2[i].get_center())
                for i in range(len(triangles))
            ]
        )
        self.play(
                Rotate(triangles[1],-PI/2),
                Rotate(triangles[2],PI/2),
        )
        self.play(
            ShowCreation(squares),
            Write(parts_theorem)
        )
        #"""

        self.play(
                *[
                    ReplacementTransform(
                        t_.copy()[:],r_,
                        run_time=4
                    )
                    for t_,r_ in zip(parts_theorem,[theorem[2],theorem[-1],theorem[0]])
                ],
                Write(theorem[1]),Write(theorem[-2])
            )


        self.wait(3)
