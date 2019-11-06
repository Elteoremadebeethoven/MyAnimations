from manimlib.imports import *


############# MY Mobjects ############
# DashedRectangle
class DashedRectangle(VGroup):
    CONFIG={
        "num_dashes": 30,
        "positive_space_ratio": 0.5,
        "width":5,
        "height":4,
        "line_config":{},
        "color":TEAL,
    }
    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        self.add(*self.get_dashed_rectangle(self.width,self.height))
        self.move_to(ORIGIN)

    def get_dashed_rectangle(self,width,height):
        h1=[ORIGIN,UP*height]
        w1=[UP*height,UP*height+RIGHT*width]
        h2=[UP*height+RIGHT*width,RIGHT*width]
        w2=[RIGHT*width,ORIGIN]
        alpha=width/height
        divs=self.num_dashes

        n_h=int(divs/(2*(alpha+1)))
        n_w=int(alpha*n_h)
        dashedrectangle=VGroup()
        for n,l in zip([n_w,n_h],[[w1,w2],[h1,h2]]):
            for side in l:
                line=VMobject()
                line.set_points_as_corners(side)
                dashedrectangle.add(
                    DashedVMobject(
                        line,
                        num_dashes=n,
                        positive_space_ratio=self.positive_space_ratio,
                        ).set_color(self.color).set_style(**self.line_config)
                    )
        return [dashedrectangle[0],dashedrectangle[3],dashedrectangle[1],dashedrectangle[2]]

#SurroundingDashedRectangle depends of DashedRectangle
class SurroundingDashedRectangle(DashedRectangle):
    CONFIG={
        "num_dashes": 100,
        "positive_space_ratio": 0.5,
    }
    def __init__(self, mob, margin=0.1, **kwargs):
        width = mob.get_width() + margin
        height = mob.get_height() + margin
        super().__init__(width=width,height=height,**kwargs)
        self.move_to(mob)

class FreehandDraw(VMobject):
    CONFIG = {
        "sign":1,
        "close":False,
        "dx_random":7,
        "length":0.06
    }
    def __init__(self,path,partitions=120,**kwargs):
        VMobject.__init__(self,**kwargs)
        coords = []
        for p in range(int(partitions)+1):
            coord_i = path.point_from_proportion((p*0.989/partitions)%1)
            coord_f = path.point_from_proportion((p*0.989/partitions+0.001)%1)
            reference_line = Line(coord_i, coord_f).rotate(self.sign*PI/2, about_point=coord_i)
            normal_unit_vector = reference_line.get_unit_vector()
            static_vector = normal_unit_vector*self.length
            random_dx = random.randint(0,self.dx_random)
            random_normal_vector = random_dx * normal_unit_vector / 100
            point_coord = coord_i + random_normal_vector + static_vector
            coords.append(point_coord)
        if self.close:
            coords.append(coords[0])
        self.set_points_smoothly(coords)

# FreehandRectangle depends of FreehandDraw
class FreehandRectangle(VMobject):
    CONFIG = {
        "margin":0.7,
        "partitions":120,
    }
    def __init__(self,texmob,**kwargs):
        VMobject.__init__(self,**kwargs)
        rect = Rectangle(
            width  = texmob.get_width() + self.margin,
            height = texmob.get_height() + self.margin
            )
        rect.move_to(texmob)
        w = rect.get_width()  
        h = rect.get_height()
        alpha = w / h
        hp = np.ceil(self.partitions / (2 * (alpha + 1)))
        wp = np.ceil(alpha * hp)
        sides = VGroup(*[
            Line(rect.get_corner(c1),rect.get_corner(c2))
            for c1,c2 in zip([UL,UR,DR,DL],[UR,DR,DL,UL])
            ])
        total_points = []
        for side,p in zip(sides,[wp,hp,wp,hp]):
            path = FreehandDraw(side,p).points
            for point in path:
                total_points.append(point)
        total_points.append(total_points[0])
        self.set_points_smoothly(total_points)

class ZigZag(VMobject):
    CONFIG = {
        "margin":0.4,
        "sign":1
    }
    def __init__(self,path,partitions=10,**kwargs):
        VMobject.__init__(self,**kwargs)
        rect = Rectangle(
            width  = path.get_width() + self.margin,
            height = path.get_height() + self.margin
            )
        rect.move_to(path)
        w = rect.get_width()  
        h = rect.get_height()
        alpha = w / h
        hp = int(np.ceil(partitions / (2 * (alpha + 1))))
        wp = int(np.ceil(alpha * hp))
        sides = VGroup(*[
            Line(rect.get_corner(c1),rect.get_corner(c2))
            for c1,c2 in zip([UL,UR,DR,DL],[UR,DR,DL,UL])
            ])
        total_points = []
        for side,points in zip(sides,[wp,hp,wp,hp]):
            for p in range(points):
                total_points.append(side.point_from_proportion(p/points))
        total_points.append(total_points[0])
        middle = int(np.floor(len(total_points)/2))
        draw_points = []
        for p in range(2,middle):
            draw_points.append(total_points[-p*self.sign])
            draw_points.append(total_points[p*self.sign])
        self.set_points_smoothly(draw_points)

class MeasureDistance(VGroup):
    CONFIG = {
        "color":RED_B,
        "buff":0.3,
        "lateral":0.3,
        "invert":False,
        "dashed_segment_length":0.09,
        "dashed":True,
        "ang_arrows":30*DEGREES,
        "size_arrows":0.2,
        "stroke":2.4,
    }
    def __init__(self,mob,**kwargs):
        VGroup.__init__(self,**kwargs)
        if self.dashed==True:
            medicion=DashedLine(ORIGIN,mob.get_length()*RIGHT,dashed_segment_length=self.dashed_segment_length).set_color(self.color)
        else:
            medicion=Line(ORIGIN,mob.get_length()*RIGHT)
 
        medicion.set_stroke(None,self.stroke)
 
        pre_medicion=Line(ORIGIN,self.lateral*RIGHT).rotate(PI/2).set_stroke(None,self.stroke)
        pos_medicion=pre_medicion.copy()
 
        pre_medicion.move_to(medicion.get_start())
        pos_medicion.move_to(medicion.get_end())
 
        angulo=mob.get_angle()
        matriz_rotacion=rotation_matrix(PI/2,OUT)
        vector_unitario=mob.get_unit_vector()
        direccion=np.matmul(matriz_rotacion,vector_unitario)
        self.direccion=direccion
 
        self.add(medicion,pre_medicion,pos_medicion)
        self.rotate(angulo)
        self.move_to(mob)
 
        if self.invert==True:
            self.shift(-direccion*self.buff)
        else:
            self.shift(direccion*self.buff)
        self.set_color(self.color)
        self.tip_point_index = -np.argmin(self.get_all_points()[-1, :])
       
 
    def add_tips(self):
        linea_referencia=Line(self[0][0].get_start(),self[0][-1].get_end())
        vector_unitario=linea_referencia.get_unit_vector()
 
        punto_final1=self[0][-1].get_end()
        punto_inicial1=punto_final1-vector_unitario*self.size_arrows
 
        punto_inicial2=self[0][0].get_start()
        punto_final2=punto_inicial2+vector_unitario*self.size_arrows
 
        lin1_1=Line(punto_inicial1,punto_final1).set_color(self[0].get_color()).set_stroke(None,self.stroke)
        lin1_2=lin1_1.copy()
        lin2_1=Line(punto_inicial2,punto_final2).set_color(self[0].get_color()).set_stroke(None,self.stroke)
        lin2_2=lin2_1.copy()
 
        lin1_1.rotate(self.ang_arrows,about_point=punto_final1,about_edge=punto_final1)
        lin1_2.rotate(-self.ang_arrows,about_point=punto_final1,about_edge=punto_final1)
 
        lin2_1.rotate(self.ang_arrows,about_point=punto_inicial2,about_edge=punto_inicial2)
        lin2_2.rotate(-self.ang_arrows,about_point=punto_inicial2,about_edge=punto_inicial2)
 
 
        return self.add(lin1_1,lin1_2,lin2_1,lin2_2)
 
    def add_tex(self,text,scale=1,buff=-1,**moreargs):
        linea_referencia=Line(self[0][0].get_start(),self[0][-1].get_end())
        texto=TexMobject(text,**moreargs)
        ancho=texto.get_height()/2
        texto.rotate(linea_referencia.get_angle()).scale(scale).move_to(self)
        texto.shift(self.direccion*(buff+1)*ancho)
        return self.add(texto)
 
    def add_text(self,text,scale=1,buff=0.1,**moreargs):
        linea_referencia=Line(self[0][0].get_start(),self[0][-1].get_end())
        texto=TextMobject(text,**moreargs)
        ancho=texto.get_height()/2
        texto.rotate(linea_referencia.get_angle()).scale(scale).move_to(self)
        texto.shift(self.direccion*(buff+1)*ancho)
        return self.add(texto)
 
    def add_size(self,text,scale=1,buff=0.1,**moreargs):
        linea_referencia=Line(self[0][0].get_start(),self[0][-1].get_end())
        texto=TextMobject(text,**moreargs)
        ancho=texto.get_height()/2
        texto.rotate(linea_referencia.get_angle())
        texto.shift(self.direccion*(buff+1)*ancho)
        return self.add(texto)
 
    def add_letter(self,text,scale=1,buff=0.1,**moreargs):
        linea_referencia=Line(self[0][0].get_start(),self[0][-1].get_end())
        texto=TexMobject(text,**moreargs).scale(scale).move_to(self)
        ancho=texto.get_height()/2
        texto.shift(self.direccion*(buff+1)*ancho)
        return self.add(texto)
 
    def get_text(self, text,scale=1,buff=0.1,invert_dir=False,invert_texto=False,remove_rot=False,**moreargs):
        linea_referencia=Line(self[0][0].get_start(),self[0][-1].get_end())
        texto=TextMobject(text,**moreargs)
        ancho=texto.get_height()/2
        if invert_texto:
            inv=PI
        else:
            inv=0
        if remove_rot:
            texto.scale(scale).move_to(self)
        else:
            texto.rotate(linea_referencia.get_angle()).scale(scale).move_to(self)
            texto.rotate(inv)
        if invert_dir:
            inv=-1
        else:
            inv=1
        texto.shift(self.direccion*(buff+1)*ancho*inv)
        return texto
 
    def get_tex(self, tex,scale=1,buff=1,invert_dir=False,invert_texto=False,remove_rot=True,**moreargs):
        linea_referencia=Line(self[0][0].get_start(),self[0][-1].get_end())
        texto=TexMobject(tex,**moreargs)
        ancho=texto.get_height()/2
        if invert_texto:
            inv=PI
        else:
            inv=0
        if remove_rot:
            texto.scale(scale).move_to(self)
        else:
            texto.rotate(linea_referencia.get_angle()).scale(scale).move_to(self)
            texto.rotate(inv)
        if invert_dir:
            inv=-1
        else:
            inv=1
        texto.shift(self.direccion*(buff+1)*ancho)
        return texto
 
class RectanglePattern(VGroup):
    CONFIG={
        "space":0.2,
        "color":RED,
        "add_rectangle":False,
        "rectangle_color":WHITE,
        "rectangle_width":4
    }
    def __init__(self,width,height=None,stroke_width=2,**kwargs):
        super().__init__(**kwargs)
        if height==None:
            height=width
        W=width
        H=height
        b=self.space
        n=1
        if H>=W:
            while -H/2+n*b<H/2+W:
                if -H/2+n*b<-H/2+W:
                    x_i=W/2-n*b
                    x_f=W/2
                if -H/2+W<=(-H)/2+n*b and (-H)/2+n*b<=H/2:
                    x_i=-W/2
                    x_f=W/2
                if H/2<=(-H)/2+n*b and (-H)/2+n*b<H/2+W:
                    x_i=-W/2
                    x_f=H+W/2-n*b
                pat=FunctionGraph(lambda x : x-W/2-H/2+n*b, 
                                    color = self.color,
                                    stroke_width = stroke_width,
                                    x_min = x_i,
                                    x_max = x_f
                                    )
                self.add(pat)
                n+=1
        else:
            while n*b-H/2<W+H/2:
                if n*b-H/2<H/2:
                    x_i=W/2-n*b
                    x_f=W/2
                if H/2<=n*b-H/2 and n*b-H/2<W-H/2:
                    x_i=W/2-n*b
                    x_f=H+W/2-n*b
                if W-H/2<=n*b-H/2 and n*b-H/2<W+H/2:
                    x_i=-W/2
                    x_f=H+W/2-n*b
                pat=FunctionGraph(lambda x : x-W/2+n*b-H/2, 
                                    color = self.color,
                                    stroke_width = stroke_width,
                                    x_min = x_i,
                                    x_max = x_f
                                    )
                self.add(pat)
                n+=1
        if self.add_rectangle:
            self.add(
                Rectangle(
                    width=width,
                    height=height,
                    color=self.rectangle_color,
                    stroke_width=self.rectangle_width
                )
            )