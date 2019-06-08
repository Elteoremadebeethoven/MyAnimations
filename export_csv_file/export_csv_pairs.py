#from manimlib.imports import *    
from big_ol_pile_of_manim_imports import *

class ExportCSVPairs(Scene):
    CONFIG={
    "camera_config":{"background_color": BLACK},
    "svg_type":"text",
    "text": TexMobject(""),
    "csv_name":"",
    "csv_number":None,
    "csv_complete":False,
    "csv_name_complete":"complete",
    "csv_range":None,
    "file":"",
    "directory":"",
    "svg_scale":0.9,
    "angle":0,
    "flip_svg":False,
    "fill_opacity": 1,
    "remove": [],
    "stroke_color": WHITE,
    "fill_color": WHITE,
    "stroke_width": 3,
    "numbers_scale":0.5,
    "show_numbers": True,
    "animation": False,
    "direction_numbers": UP,
    "color_numbers": RED,
    "space_between_numbers":0,
    "show_elements":[],
    "color_element":BLUE,
    "set_size":"width",
    "remove_stroke":[],
    "show_stroke":[],
    "warning_color":RED,
    "stroke_":1
    }
    def construct(self):
        CSV_DIR = os.path.join(self.directory)

        if not os.path.exists(CSV_DIR):
            os.makedirs(CSV_DIR)

        if not self.csv_complete:
            self.create_csv()
        else:
            self.create_complete_csv()



    def create_csv(self):
        self.imagen=self.text
        if self.set_size=="width":
            self.imagen.set_width(FRAME_WIDTH)
        else:
            self.imagen.set_height(FRAME_HEIGHT)
        self.imagen.scale(self.svg_scale)
        if self.show_numbers==True:
            tex_string,tex_number = self.print_formula(self.imagen.copy(),
                self.numbers_scale,
                self.direction_numbers,
                self.remove,
                self.space_between_numbers,
                self.color_numbers)
        with open(self.directory+'%s_%s.csv'%(self.csv_name,self.csv_number),'w',newline='') as fp:
            a = csv.writer(fp, delimiter=',')
            data = [
                        tex_number,
                        tex_string
                    ]
            a.writerows(data)

    def print_formula(self,text,inverse_scale,direction,exception,buff,color):
        tex_string=[]
        tex_number=[]
        text.set_color(self.warning_color)
        self.add(text)
        c = 0
        for j in range(len(text)):
            permission_print=True
            for w in exception:
                if j==w:
                    permission_print=False
            if permission_print:
                self.add(text[j].set_color(self.stroke_color))
        c = c + 1

        c=0
        for j in range(len(text)):
            permission_print=True
            element = TexMobject("%d" %c,color=color)
            element.scale(inverse_scale)
            element.next_to(text[j],direction,buff=buff)
            for w in exception:
                if j==w:
                    permission_print=False
            if permission_print:
                self.add_foreground_mobjects(element)
                tex_string.append(text[j].get_tex_string())
                tex_number.append(j)
            c = c + 1 
        return tex_string,tex_number

    def create_complete_csv(self):
        def rango(n):
            return range(n+1)
        def add_quote(row):
            new_row=[]
            for r in row:
                r+=','
                new_row.append(r)
            return new_row
        def es_par(n):
            if n%2==0:
                return True
            else:
                return False


        rows=[]
        list_0=list(range(self.csv_range))
        list_1=list_0.copy()

        list_1.append(self.csv_range)
        list_1.pop(0)

        for f_i,f_f in zip(list_0,list_1):
            for string in range(f_i,f_f+1):
                pre_rows=[]
                with open(self.directory+'%s_%s.csv'%(self.csv_name,string), 'r') as f:
                    reader = csv.reader(f,delimiter=',')
                    for row in reader:
                        pre_rows.append(row)
                    if string==f_i:
                        rows.append(['Step: %s'%(f_i+1)])
                        rows.append(['\t']+['N']+add_quote(pre_rows[0])+['),'])
                        rows.append(['\t']+['[%s]'%f_i]+pre_rows[1])
                    else:
                        rows.append(['\t']+['[%s]'%f_f]+pre_rows[1])
                        rows.append(['\t']+['N']+add_quote(pre_rows[0])+[')'])
                        rows.append("\n")
                        rows.append(['pre_fade:']+['('])
                        rows.append(['pre_write:']+['('])
                        rows.append(['pre_copy:']+['('])
                        rows.append("\n")
                        rows.append(['pre_form:']+['('])
                        rows.append(['pos_form:']+['('])
                        rows.append("\n")
                        rows.append(['pos_copy:']+['('])
                        rows.append(['pos_fade:']+['('])
                        rows.append(['pos_write:']+['('])
                        rows.append("\n")
                        rows.append(['run_fade:']+['('])
                        rows.append(['run_write:']+['('])
                        rows.append("\n")
                        rows.append(['---------']*50)
                        rows.append("\n")




        with open(self.directory+'%s.csv'%self.csv_name,'w',newline='') as fp:
            a = csv.writer(fp, delimiter=',')
            data = [
                      *rows
                    ]
            a.writerows(data)
