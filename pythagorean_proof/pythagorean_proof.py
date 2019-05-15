#from big_ol_pile_of_manim_imports import *
from manimlib.imports import *

class Medicion(VGroup):
    CONFIG = {
        "color":RED_B,
        "buff":0.3,
        "laterales":0.3,
        "invertir":False,
        "dashed_segment_length":0.09,
        "dashed":False,
        "con_flechas":True,
        "ang_flechas":30*DEGREES,
        "tam_flechas":0.2,
        "stroke":2.4
    }
    def __init__(self,objeto,**kwargs):
        VGroup.__init__(self,**kwargs)
        if self.dashed==True:
            medicion=DashedLine(ORIGIN,objeto.get_length()*RIGHT,dashed_segment_length=self.dashed_segment_length).set_color(self.color)
        else:
            medicion=Line(ORIGIN,objeto.get_length()*RIGHT)

        medicion.set_stroke(None,self.stroke)

        pre_medicion=Line(ORIGIN,self.laterales*RIGHT).rotate(PI/2).set_stroke(None,self.stroke)
        pos_medicion=pre_medicion.copy()

        pre_medicion.move_to(medicion.get_start())
        pos_medicion.move_to(medicion.get_end())

        angulo=objeto.get_angle()
        matriz_rotacion=rotation_matrix(PI/2,OUT)
        vector_unitario=objeto.get_unit_vector()
        direccion=np.matmul(matriz_rotacion,vector_unitario)
        self.direccion=direccion

        self.add(medicion,pre_medicion,pos_medicion)
        self.rotate(angulo)
        self.move_to(objeto)

        if self.invertir==True:
            self.shift(-direccion*self.buff)
        else:
            self.shift(direccion*self.buff)
        self.set_color(self.color)
        self.tip_point_index = -np.argmin(self.get_all_points()[-1, :])
        

    def add_tips(self):
        linea_referencia=Line(self[0][0].get_start(),self[0][-1].get_end())
        vector_unitario=linea_referencia.get_unit_vector()

        punto_final1=self[0][-1].get_end()
        punto_inicial1=punto_final1-vector_unitario*self.tam_flechas

        punto_inicial2=self[0][0].get_start()
        punto_final2=punto_inicial2+vector_unitario*self.tam_flechas

        lin1_1=Line(punto_inicial1,punto_final1).set_color(self[0].get_color()).set_stroke(None,self.stroke)
        lin1_2=lin1_1.copy()
        lin2_1=Line(punto_inicial2,punto_final2).set_color(self[0].get_color()).set_stroke(None,self.stroke)
        lin2_2=lin2_1.copy()

        lin1_1.rotate(self.ang_flechas,about_point=punto_final1,about_edge=punto_final1)
        lin1_2.rotate(-self.ang_flechas,about_point=punto_final1,about_edge=punto_final1)

        lin2_1.rotate(self.ang_flechas,about_point=punto_inicial2,about_edge=punto_inicial2)
        lin2_2.rotate(-self.ang_flechas,about_point=punto_inicial2,about_edge=punto_inicial2)


        return self.add(lin1_1,lin1_2,lin2_1,lin2_2)

    def add_tex(self,texto,escala=1,buff=0.1,**moreargs):
        linea_referencia=Line(self[0][0].get_start(),self[0][-1].get_end())
        texto=TexMobject(texto,**moreargs)
        ancho=texto.get_height()/2
        texto.rotate(linea_referencia.get_angle()).scale(escala).move_to(self)
        texto.shift(self.direccion*(buff+1)*ancho)
        return self.add(texto)

    def add_text(self,text,escala=1,buff=0.1,**moreargs):
        linea_referencia=Line(self[0][0].get_start(),self[0][-1].get_end())
        texto=TextMobject(text,**moreargs)
        ancho=texto.get_height()/2
        texto.rotate(linea_referencia.get_angle()).scale(escala).move_to(self)
        texto.shift(self.direccion*(buff+1)*ancho)
        return self.add(texto)

    def add_size(self,texto,escala=1,buff=0.1,**moreargs):
        linea_referencia=Line(self[0][0].get_start(),self[0][-1].get_end())
        texto=TextMobject(texto,**moreargs)
        ancho=texto.get_height()/2
        texto.rotate(linea_referencia.get_angle())
        texto.shift(self.direccion*(buff+1)*ancho)
        return self.add(texto)

    def add_letter(self,texto,escala=1,buff=0.1,**moreargs):
        linea_referencia=Line(self[0][0].get_start(),self[0][-1].get_end())
        texto=TexMobject(texto,**moreargs).scale(escala).move_to(self)
        ancho=texto.get_height()/2
        texto.shift(self.direccion*(buff+1)*ancho)
        return self.add(texto)

    def get_text(self, text,escala=1,buff=0.1,invert_dir=False,invert_texto=False,elim_rot=False,**moreargs):
        linea_referencia=Line(self[0][0].get_start(),self[0][-1].get_end())
        texto=TextMobject(text,**moreargs)
        ancho=texto.get_height()/2
        if invert_texto:
            inv=PI
        else:
            inv=0
        if elim_rot:
            texto.scale(escala).move_to(self)
        else:
            texto.rotate(linea_referencia.get_angle()).scale(escala).move_to(self)
            texto.rotate(inv)
        if invert_dir:
            inv=-1
        else:
            inv=1
        texto.shift(self.direccion*(buff+1)*ancho*inv)
        return texto

    def get_tex(self, tex,escala=1,buff=0.1,invert_dir=False,invert_texto=False,elim_rot=False,**moreargs):
        linea_referencia=Line(self[0][0].get_start(),self[0][-1].get_end())
        texto=TexMobject(texto,**moreargs)
        ancho=texto.get_height()/2
        if invert_texto:
            inv=PI
        else:
            inv=0
        if elim_rot:
            texto.scale(escala).move_to(self)
        else:
            texto.rotate(linea_referencia.get_angle()).scale(escala).move_to(self)
            texto.rotate(inv)
        if invert_dir:
            inv=-1
        else:
            inv=1
        texto.shift(self.direccion*(buff+1)*ancho)
        return texto

class PythagoreanProof(Scene):
	CONFIG={
	"color_triangulos":YELLOW,
	"color_rect_c":RED,
	"color_rect_b":ORANGE,
	"color_rect_a":ORANGE,
	"color_cuadrado_c":ORANGE,
	"opacidad_triangulos":0.6,
	"opacidad_cuadradro_a":0.6,
	"opacidad_cuadradro_b":0.6,
	"opacidad_cuadradro_c":0.6,
	"grosor_lineas":1,
	"l_a":5/5,
	"l_b":12/5,
	"l_c":13/5,
	}
	def construct(self):
		self.pre_cuadrado()
		self.pos_cuadrado()
		self.tran_pre_pos_cuadrado()

	def pre_cuadrado(self):
		cuadro=Square(side_length=self.l_a+self.l_b)
		coordenadas_esquinas=[]
		for punto in [DL,DR,UL,UR]:
			coordenadas_esquinas.append(cuadro.get_corner(punto))
		eii,eid,esi,esd=coordenadas_esquinas
		p_eii=Dot(eii)
		p_eid=Dot(eid)
		p_esi=Dot(esi)
		p_esd=Dot(esd)
		puntos_esquinas=VGroup(p_eii,p_eid,p_esi,p_esd)

		coordenadas_lados=[]
		#               lin 			liz					ls 				   ld
		for punto in [eid+LEFT*self.l_b,eii+UP*self.l_b,esi+RIGHT*self.l_b,esd+DOWN*self.l_b]:
			coordenadas_lados.append(punto)
		lin,liz,ls,ld=coordenadas_lados
		p_lin=Dot(lin)
		p_liz=Dot(liz)
		p_ls=Dot(ls)
		p_ld=Dot(ld)
		puntos_lados=VGroup(p_lin,p_liz,p_ls,p_ld)

		t1=Polygon(lin,eid,ld,color=self.color_triangulos).set_fill(self.color_triangulos,self.opacidad_triangulos).set_stroke(None,self.grosor_lineas)
		t2=Polygon(lin,eii,liz,color=self.color_triangulos).set_fill(self.color_triangulos,self.opacidad_triangulos).set_stroke(None,self.grosor_lineas)
		t3=Polygon(liz,esi,ls,color=self.color_triangulos).set_fill(self.color_triangulos,self.opacidad_triangulos).set_stroke(None,self.grosor_lineas)
		t4=Polygon(ld,esd,ls,color=self.color_triangulos).set_fill(self.color_triangulos,self.opacidad_triangulos).set_stroke(None,self.grosor_lineas)
		cuadrado_c=Polygon(*coordenadas_lados,color=self.color_cuadrado_c).set_fill(self.color_cuadrado_c,self.opacidad_cuadradro_c)

		self.cuadrado_c=cuadrado_c

		med_ia=Medicion(Line(eii,lin),invertir=True,dashed=True,buff=0.5).add_tips().add_tex("a",buff=-3.7,color=WHITE)
		med_ib=Medicion(Line(lin,eid),invertir=True,dashed=True,buff=0.5).add_tips().add_tex("b",buff=-2.7,color=WHITE)
		med_izb=Medicion(Line(eii,liz),invertir=False,dashed=True,buff=0.5).add_tips().add_tex("b",buff=1,color=WHITE)
		med_iza=Medicion(Line(liz,esi),invertir=False,dashed=True,buff=0.5).add_tips().add_tex("a",buff=2,color=WHITE)
		med_iza[-1].rotate(-PI/2)
		med_izb[-1].rotate(-PI/2)
		mediciones_1=VGroup(med_ia,med_ib,med_iza,med_izb)
		
		
		titulo=TextMobject("\\sc Pythagorean proof.",color=WHITE).to_corner(UL)
		self.titulo=VGroup(titulo)
		self.play(Write(titulo,run_time=1),ShowCreation(cuadro,run_time=1),
			*[DrawBorderThenFill(triangulo)for triangulo in [t1,t2,t3,t4]],
			*[GrowFromCenter(objeto)for objeto in [*mediciones_1]],run_time=1
			)

		conjunto_pre_cuadrado=VGroup(cuadro,t1,t2,t3,t4)
		#self.add(cuadro,t1,t2,t3,t4,cuadrado_c)
		self.conjunto_pre_cuadrado=conjunto_pre_cuadrado
		self.conjunto_pre_cuadrado.add(med_ia,med_ib,med_iza,med_izb)
		self.play(conjunto_pre_cuadrado.to_edge,LEFT,{"buff":1.7})
		cuadrado_c.move_to(cuadro)

	def pos_cuadrado(self):
		cuadro=Square(side_length=self.l_a+self.l_b)
		coordenadas_esquinas=[]
		for punto in [DL,DR,UL,UR]:
			coordenadas_esquinas.append(cuadro.get_corner(punto))
		eii,eid,esi,esd=coordenadas_esquinas
		p_eii=Dot(eii)
		p_eid=Dot(eid)
		p_esi=Dot(esi)
		p_esd=Dot(esd)
		puntos_esquinas=VGroup(p_eii,p_eid,p_esi,p_esd)

		coordenadas_lados=[]
		#               lin 				liz					ls 				   ld
		for punto in [eid+LEFT*self.l_b,eii+UP*self.l_a,esi+RIGHT*self.l_a,esd+DOWN*self.l_b,eii+self.l_a*(UP+RIGHT)]:
			coordenadas_lados.append(punto)
		lin,liz,ls,ld,centro=coordenadas_lados
		p_lin=Dot(lin)
		p_liz=Dot(liz)
		p_ls=Dot(ls)
		p_ld=Dot(ld)
		p_centro=Dot(centro)
		puntos_lados=VGroup(p_lin,p_liz,p_ls,p_ld,p_centro)

		t1=Polygon(lin,eid,ld,color=self.color_triangulos).set_fill(self.color_triangulos,self.opacidad_triangulos).set_stroke(None,self.grosor_lineas)
		t2=Polygon(lin,centro,ld,color=self.color_triangulos).set_fill(self.color_triangulos,self.opacidad_triangulos).set_stroke(None,self.grosor_lineas)
		t3=Polygon(esi,liz,centro,color=self.color_triangulos).set_fill(self.color_triangulos,self.opacidad_triangulos).set_stroke(None,self.grosor_lineas)
		t4=Polygon(centro,ls,esi,color=self.color_triangulos).set_fill(self.color_triangulos,self.opacidad_triangulos).set_stroke(None,self.grosor_lineas)
		cuadrado_a=Polygon(*[eii,liz,centro,lin],color=self.color_rect_a).set_fill(self.color_rect_a,self.opacidad_cuadradro_a)
		cuadrado_b=Polygon(*[centro,ls,esd,ld],color=self.color_rect_b).set_fill(self.color_rect_b,self.opacidad_cuadradro_b)

		med_ia=Medicion(Line(eii,lin),invertir=True,dashed=True,buff=0.5).add_tips().add_tex("a",buff=-3.7,color=WHITE)
		med_ib=Medicion(Line(lin,eid),invertir=True,dashed=True,buff=0.5).add_tips().add_tex("b",buff=-2.7,color=WHITE)
		med_iza=Medicion(Line(eii,liz),invertir=False,dashed=True,buff=0.5).add_tips().add_tex("a",buff=1.8,color=WHITE)
		med_izb=Medicion(Line(liz,esi),invertir=False,dashed=True,buff=0.5).add_tips().add_tex("b",buff=1,color=WHITE)
		med_iza[-1].rotate(-PI/2)
		med_izb[-1].rotate(-PI/2)
		mediciones_2=VGroup(med_ia,med_ib,med_iza,med_izb)

		conjunto_pos_cuadrado=VGroup(cuadro,t1,t2,t3,t4,cuadrado_a,cuadrado_b,mediciones_2)
		conjunto_pos_cuadrado.to_edge(RIGHT,buff=1.7)
		self.conjunto_pos_cuadrado=conjunto_pos_cuadrado

		self.mediciones_2=mediciones_2

		self.cuadrado_a=cuadrado_a
		self.cuadrado_b=cuadrado_b

	def tran_pre_pos_cuadrado(self):
		self.play(
			ReplacementTransform(
					self.conjunto_pre_cuadrado[0].copy(),self.conjunto_pos_cuadrado[0],
				),run_time=1
			)
		self.play(
					*[ReplacementTransform(
						self.conjunto_pre_cuadrado[i].copy(),self.conjunto_pos_cuadrado[i],
						)for i in range(1,5)],run_time=1
				)
		self.play(*[GrowFromCenter(objeto)for objeto in [*self.mediciones_2]],run_time=1)
		self.play(DrawBorderThenFill(self.cuadrado_c),DrawBorderThenFill(self.conjunto_pos_cuadrado[-3]),DrawBorderThenFill(self.conjunto_pos_cuadrado[-2]),run_time=1)


		t_a2=TexMobject("a^2",color=WHITE).move_to(self.cuadrado_a)
		t_b2=TexMobject("b^2",color=WHITE).move_to(self.cuadrado_b)
		t_c2=TexMobject("c^2",color=WHITE).move_to(self.cuadrado_c)

		self.play(*[Write(t_)for t_ in [t_a2,t_b2,t_c2]])

		teorema=TexMobject("c^2","=","a^2","+","b^2",color=BLUE).to_edge(DOWN)
		self.play(
					*[ReplacementTransform(
						t_.copy()[:],r_
						)for t_,r_ in zip([t_a2,t_b2,t_c2],[teorema[2],teorema[-1],teorema[0]])],
					Write(teorema[1]),Write(teorema[-2]),run_time=1
				)
		self.wait()
		self.play(
			self.titulo.shift,UP*3,
			teorema.shift,DOWN*3,
			self.conjunto_pos_cuadrado.shift,RIGHT*7,
			self.conjunto_pre_cuadrado.shift,LEFT*7,
			VGroup(t_a2,t_b2).shift,RIGHT*7,
			t_c2.shift,LEFT*5,
			self.cuadrado_c.shift,LEFT*7,
			)