
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
		self.wait()
		self.pre_cuadrado()
		self.pos_cuadrado()
		self.tran_pre_pos_cuadrado()
		self.wait()

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
		
		
		titulo=TextMobject("\\sc Pythagorean proof.",color=WHITE).to_corner(UL)
		self.titulo=VGroup(titulo)
		self.play(Write(titulo,run_time=1),ShowCreation(cuadro,run_time=1),
			*[DrawBorderThenFill(triangulo)for triangulo in [t1,t2,t3,t4]],
			run_time=1
			)

		conjunto_pre_cuadrado=VGroup(cuadro,t1,t2,t3,t4)
		#self.add(cuadro,t1,t2,t3,t4,cuadrado_c)
		self.conjunto_pre_cuadrado=conjunto_pre_cuadrado
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


		conjunto_pos_cuadrado=VGroup(cuadro,t1,t2,t3,t4,cuadrado_a,cuadrado_b)
		conjunto_pos_cuadrado.to_edge(RIGHT,buff=1.7)
		self.conjunto_pos_cuadrado=conjunto_pos_cuadrado

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
		self.play(DrawBorderThenFill(self.cuadrado_c),DrawBorderThenFill(self.conjunto_pos_cuadrado[-2]),DrawBorderThenFill(self.conjunto_pos_cuadrado[-1]),run_time=1)


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
