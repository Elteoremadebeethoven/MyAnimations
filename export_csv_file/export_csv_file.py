#from manimlib.imports import *
from big_ol_pile_of_manim_imports import *

class ExportCSV(Scene):
    CONFIG={
    "camera_config":{"background_color": BLACK},
    "svg_type":"text",
    "text": TexMobject(""),
    "csv_name":"",
    "csv_number":None,
    "csv_complete":False,
    "csv_name_complete":"no_complete",
    "csv_range":None,
    "csv_desfase":[],
    "cvs_sobrantes":0,
    "file":"",
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
        self.file_directory=self.__class__.__module__.replace(".", os.path.sep)
        self.directory = os.path.join("csv_files",self.file_directory)
        CSV_DIR=self.directory
        print("\n")
        print("CSV directory at: ",CSV_DIR)

        if not os.path.exists(CSV_DIR):
            os.makedirs(CSV_DIR)

        self.create_csv()



    def create_csv(self):
        import csv
        self.imagen=self.text
        self.imagen.set_width(FRAME_WIDTH)
        if self.imagen.get_height()>FRAME_HEIGHT:
            self.imagen.set_height(FRAME_HEIGHT)
        self.imagen.scale(self.svg_scale)
        if self.show_numbers==True:
            pre_tex_string,tex_number = self.print_formula(self.imagen.copy(),
                self.numbers_scale,
                self.direction_numbers,
                self.remove,
                self.space_between_numbers,
                self.color_numbers)
        with open(self.directory+'/%s_%s.csv'%(self.__class__.__name__,self.csv_number),'w',newline='') as fp:
            a = csv.writer(fp, delimiter=',')
            tex_string=[]
            if len(self.csv_desfase)==0:
                tex_string=pre_tex_string
            else:
                tex_number_c=tex_number.copy()
                for i in self.remove:
                    tex_number_c.append("x")
                for i in  range(len(tex_number_c)):
                    if i in self.csv_desfase:
                        tex_string.append("DES")
                        tex_string.append(pre_tex_string[i])
                        i+=1
                    else:
                        tex_string.append(pre_tex_string[i])

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

