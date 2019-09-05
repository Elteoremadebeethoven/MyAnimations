from manimlib.imports import *

NEW_BLUE = "#68a8e1"

class Thumbnail(GraphScene):
    CONFIG = {
        "y_max": 8,
        "y_axis_height": 5,
    }

    def construct(self):
        self.show_function_graph()

    def show_function_graph(self):
        self.setup_axes(animate=False)
        def func(x):
            return 0.1 * (x + 3-5) * (x - 3-5) * (x-5) + 5

        def rect(x):
            return 2.775*(x-1.5)+3.862
        recta = self.get_graph(rect,x_min=-1,x_max=5)
        graph = self.get_graph(func,x_min=0.2,x_max=9)
        graph.set_color(NEW_BLUE)
        input_tracker_p1 = ValueTracker(1.5)
        input_tracker_p2 = ValueTracker(3.5)

        def get_x_value(input_tracker):
            return input_tracker.get_value()

        def get_y_value(input_tracker):
            return graph.underlying_function(get_x_value(input_tracker))

        def get_x_point(input_tracker):
            return self.coords_to_point(get_x_value(input_tracker), 0)

        def get_y_point(input_tracker):
            return self.coords_to_point(0, get_y_value(input_tracker))

        def get_graph_point(input_tracker):
            return self.coords_to_point(get_x_value(input_tracker), get_y_value(input_tracker))

        def get_v_line(input_tracker):
            return DashedLine(get_x_point(input_tracker), get_graph_point(input_tracker), stroke_width=2)

        def get_h_line(input_tracker):
            return DashedLine(get_graph_point(input_tracker), get_y_point(input_tracker), stroke_width=2)
        # 
        input_triangle_p1 = RegularPolygon(n=3, start_angle=TAU / 4)
        output_triangle_p1 = RegularPolygon(n=3, start_angle=0)
        input_triangle_p2 = input_triangle_p1.copy()
        output_triangle_p2 = output_triangle_p1.copy()

        for triangle in input_triangle_p1, output_triangle_p1,input_triangle_p2, output_triangle_p2:
            triangle.set_fill(WHITE, 1)
            triangle.set_stroke(width=0)
            triangle.scale(0.1)
        
        # 
        x_label_p1 = TexMobject("a")
        output_label_p1 = TexMobject("f(a)")
        x_label_p2 = TexMobject("b")
        output_label_p2 = TexMobject("f(b)")
        v_line_p1 = get_v_line(input_tracker_p1)
        v_line_p2 = get_v_line(input_tracker_p2)
        h_line_p1 = get_h_line(input_tracker_p1)
        h_line_p2 = get_h_line(input_tracker_p2)
        graph_dot_p1 = Dot(color=WHITE)
        graph_dot_p2 = Dot(color=WHITE)

        # reposition mobjects
        x_label_p1.next_to(v_line_p1, DOWN)
        x_label_p2.next_to(v_line_p2, DOWN)
        output_label_p1.next_to(h_line_p1, LEFT)
        output_label_p2.next_to(h_line_p2, LEFT)
        input_triangle_p1.next_to(v_line_p1, DOWN, buff=0)
        input_triangle_p2.next_to(v_line_p2, DOWN, buff=0)
        output_triangle_p1.next_to(h_line_p1, LEFT, buff=0)
        output_triangle_p2.next_to(h_line_p2, LEFT, buff=0)
        graph_dot_p1.move_to(get_graph_point(input_tracker_p1))
        graph_dot_p2.move_to(get_graph_point(input_tracker_p2))

        #updaters


        #
        self.play(
            ShowCreation(graph),
        )
        # Animacion del punto a
        self.play(
            DrawBorderThenFill(input_triangle_p1),
            Write(x_label_p1),
            ShowCreation(v_line_p1),
            ShowCreation(h_line_p1),
            Write(output_label_p1),
            DrawBorderThenFill(output_triangle_p1),
            DrawBorderThenFill(input_triangle_p2),
            Write(x_label_p2),
            ShowCreation(v_line_p2),
            ShowCreation(h_line_p2),
            Write(output_label_p2),
            DrawBorderThenFill(output_triangle_p2),
            GrowFromCenter(graph_dot_p2),
            GrowFromCenter(graph_dot_p1),
            run_time=0.5
        )

        group = VGroup(
            input_triangle_p2,
            output_triangle_p2,
            x_label_p2,
            output_label_p2,
            v_line_p2,
            h_line_p2,
            graph_dot_p2,
            )

        def update_group(mob,alpha):
            it,ot,xl,yl,vl,hl,d = mob
            hl.become(get_h_line(input_tracker_p2)).fade(alpha)
            vl.become(get_v_line(input_tracker_p2)).fade(alpha)
            it.next_to(vl, DOWN, buff=0).fade(alpha)
            ot.next_to(hl, LEFT, buff=0).fade(alpha)
            xl.next_to(vl, DOWN).fade(alpha)
            yl.next_to(hl, LEFT).fade(alpha)
            d.move_to(get_graph_point(input_tracker_p2))

        ###################
        solpe_recta = self.get_secant_slope_group(
            1.9, recta, dx = 1.4,
            df_label = None,
            dx_label = None,
            dx_line_color = PURPLE,
            df_line_color= ORANGE,
            )
        grupo_sec = self.get_secant_slope_group(
            1.5, graph, dx = 2,
            df_label = None,
            dx_label = None,
            dx_line_color = "#942357",
            df_line_color= "#3f7d5c",
            secant_line_color = RED,
        )
        start_dx = grupo_sec.kwargs["dx"]
        start_x = grupo_sec.kwargs["x"]
        def update_slope(group, alpha):
            dx = interpolate(start_dx, 0.001, alpha)
            x = interpolate(start_x, 1.5, alpha)
            kwargs = dict(grupo_sec.kwargs)
            kwargs["dx"] = dx
            kwargs["x"] = x
            new_group = self.get_secant_slope_group(**kwargs)
            group.become(new_group)
            return group

        self.add(
            input_triangle_p2,
            graph_dot_p2,
            v_line_p2,
            h_line_p2,
            output_triangle_p2,
        )
        self.add_foreground_mobjects(grupo_sec)
        self.add_foreground_mobjects(graph_dot_p1,graph_dot_p2)
        self.play(FadeIn(grupo_sec))
        self.wait()

        self.play(
            input_tracker_p2.set_value,input_tracker_p1.get_value(),
            UpdateFromAlphaFunc(grupo_sec,update_slope),
            UpdateFromAlphaFunc(group,update_group),
            )

        kwargs = {
            "x_min" : 2,
            "x_max" : 8,
            "fill_opacity" : 0.75,
            "stroke_width" : 0.25,
        }
        self.graph=graph
        iteraciones=6


        self.rect_list = self.get_riemann_rectangles_list(
            graph, iteraciones,start_color=PURPLE,end_color=ORANGE, **kwargs
        )
        flat_rects = self.get_riemann_rectangles(
            self.get_graph(lambda x : 0), dx = 0.5,start_color=invert_color(PURPLE),end_color=invert_color(ORANGE),**kwargs
        )
        rects = self.rect_list[0]
        self.transform_between_riemann_rects(
            flat_rects, rects, 
            replace_mobject_with_target_in_scene = True,
            run_time=0.9
        )

        for j in range(4,6):
            for w in self.rect_list[j]:
                    color=w.get_color()
                    w.set_stroke(color,1.5)
        for j in range(1,6):
            self.transform_between_riemann_rects(
            self.rect_list[j-1], self.rect_list[j], dx=1,
            replace_mobject_with_target_in_scene = True,
            run_time=0.9
            )