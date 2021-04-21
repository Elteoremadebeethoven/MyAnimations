from manim import *

class Grid(VGroup):
    def __init__(self, rows, columns, height=6, width=6,**kwargs):
        self.height_g = height
        self.width_g = width
        super().__init__(**kwargs)

        x_step = self.width_g / columns
        y_step = self.height_g / rows

        for x in np.arange(0, self.width_g + x_step, x_step):
            self.add(Line(
                [x - self.width_g / 2., -self.height_g / 2., 0],
                [x - self.width_g / 2., self.height_g / 2., 0],
            ))
        for y in np.arange(0, self.height + y_step, y_step):
            self.add(Line(
                [-self.width_g / 2., y - self.height_g / 2., 0],
                [self.width_g / 2., y - self.height_g / 2., 0]
            ))


class ScreenGrid(VGroup):
    def __init__(
            self,
            rows=8,
            columns=14,
            height=config.frame_height,
            width=14,
            grid_stroke=0.5,
            grid_color=WHITE,
            axis_color=RED,
            axis_stroke=2,
            labels_scale=0.25,
            labels_buff=0,
            number_decimals=2,
            **kwargs):
        self.height_g = height
        self.width_g = width
        self.grid_stroke = grid_stroke
        self.grid_color = grid_color
        self.axis_color = axis_color
        self.axis_stroke = axis_stroke
        self.labels_scale = labels_scale
        self.labels_buff = labels_buff
        self.number_decimals = number_decimals
        super().__init__(**kwargs)
        grid = Grid(width=self.width_g, height=self.height_g, rows=rows, columns=columns)
        grid.set_stroke(self.grid_color, self.grid_stroke)

        vector_ii = ORIGIN + np.array((- self.width_g / 2, - self.height_g / 2, 0))
        vector_si = ORIGIN + np.array((- self.width_g / 2, self.height_g / 2, 0))
        vector_sd = ORIGIN + np.array((self.width_g / 2, self.height_g / 2, 0))

        axes_x = Line(LEFT * self.width_g / 2, RIGHT * self.width_g / 2)
        axes_y = Line(DOWN * self.height_g / 2, UP * self.height_g / 2)

        axes = VGroup(axes_x, axes_y).set_stroke(self.axis_color, self.axis_stroke)

        divisions_x = self.width_g / columns
        divisions_y = self.height_g / rows

        directions_buff_x = [UP, DOWN]
        directions_buff_y = [RIGHT, LEFT]
        dd_buff = [directions_buff_x, directions_buff_y]
        vectors_init_x = [vector_ii, vector_si]
        vectors_init_y = [vector_si, vector_sd]
        vectors_init = [vectors_init_x, vectors_init_y]
        divisions = [divisions_x, divisions_y]
        orientations = [RIGHT, DOWN]
        labels = VGroup()
        set_changes = zip([columns, rows], divisions, orientations, [0, 1], vectors_init, dd_buff)
        for c_and_r, division, orientation, coord, vi_c, d_buff in set_changes:
            for i in range(1, c_and_r):
                for v_i, directions_buff in zip(vi_c, d_buff):
                    ubication = v_i + orientation * division * i
                    coord_point = round(ubication[coord], self.number_decimals)
                    label = Text(f"{coord_point}",font="Arial",stroke_width=0).scale(self.labels_scale)
                    label.next_to(ubication, directions_buff, buff=self.labels_buff)
                    labels.add(label)

        self.add(grid, axes, labels)


class CoordScreen(Scene):
    def construct(self):
        screen_grid = ScreenGrid()
        dot = Dot([1, 1, 0])
        self.add(screen_grid)
        self.play(FadeIn(dot))
        self.wait()
