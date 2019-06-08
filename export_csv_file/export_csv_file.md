# ATTENTION - THIS METHOD CAN TO HAVE ERRORS IF YOU USE \sqrt

# Create a list of the elements of a TeX formula
Copy and paste [this](https://github.com/Elteoremadebeethoven/MyAnimations/blob/master/export_csv_file/export_csv_file.py) code in your project and use it with the next format:

```python3
class FormulaCSV(ExportCSV):
    CONFIG={
    "text":TexMobject(...)
    }
```
You have to render it with `-ps`

## For example:
```python3
# Proyect at : my_proyects/project.py
class FormulaCSV(ExportCSV):
    CONFIG={
    "text":TexMobject("a","x","^","2","+","b","x","+","c","=","0")
    }
```
The result is this image:

<p align="center"><img src ="/export_csv_file/images/im1.png" /></p>

And a .csv that you can find at `csv_files/proyect_path/name_of_file.py/scene_name.csv`

In our example the diretory is: `my_projects/project/FormulaCSV.py`

<p align="center"><img src ="/export_csv_file/images/im2.png" /></p>

## Remove elements
We can see in the example that the number 2 have a empty object, so we can remove it with:
```python3
# Proyect at : my_proyects/project.py
class FormulaCSV(ExportCSV):
    CONFIG={
    "text":TexMobject("a","x","^","2","+","b","x","+","c","=","0"),
    "remove":[2]
    }
```
Result:

<p align="center"><img src ="/export_csv_file/images/im3.png" /></p>

The change also affects the .csv file:

<p align="center"><img src ="/export_csv_file/images/im4.png" /></p>

## Create a .csv file with pairs

Suppose that we want to do this transformation:

<p align="center"><img src ="/export_csv_file/images/im5.gif" /></p>

Then, we have to write three formulas, and we have to use ReplacementTransform.

Copy [this](https://github.com/Elteoremadebeethoven/MyAnimations/blob/master/export_csv_file/export_csv_pairs.py) code in your project, and create a class for each formula, you can remove the empty elements:

```python3
class Formula1CSV(ExportCSVPairs):
    CONFIG={
    "csv_name":"Formula", # <- This name is the same for all ExportCSVParis scenes
    "csv_number":0,       # <- This is a formula number 0
    "text":TexMobject("a","x","^","2","+","b","x","+","c","=","0"),
    "remove":[2]
    }

class Formula2CSV(ExportCSVPairs):
    CONFIG={
    "csv_name":"Formula", # <- This name is the same for all ExportCSVParis scenes
    "csv_number":1,       # <- This is a formula number 1
    "text":TexMobject("a","x","^","2","+","b","x","=","-","c"),
    "remove":[2]
    }

class Formula3CSV(ExportCSVPairs):
    CONFIG={
    "csv_name":"Formula", # <- This name is the same for all ExportCSVParis scenes
    "csv_number":2,       # <- This is a formula number 2
    "text":TexMobject("x","^","2","+","{","b","\\over","a","}","x","=","-","{","c","\\over","a","}"),
    "remove":[1,4,8,12,16]
    }

class FormulaFiles(ExportCSVPairs):
    CONFIG={
    "csv_name":"Formula", # <- This name is the same for all ExportCSVParis scenes
    "csv_range":2, # This is the range of the formulas, start with the formula 0 and ends with formula 2
    "csv_complete":True   # <- Use this line to create the entire document
    }
```

If you render all scenes with `-as` then you create a scenes.png and .csv files:

<p align="center"><img src ="/export_csv_file/images/im_ex.png" /></p>

You can delete the `_None.csv` file, in the `Formula.csv` file you can see this:

<p align="center"><img src ="/export_csv_file/images/im6.png" /></p>

And, with a little work you can organice the elements to do the ReplatementTransform thing:

<p align="center"><img src ="/export_csv_file/images/im7.png" /></p>

<p align="center"><img src ="/export_csv_file/images/im8.png" /></p>


Once you have write the changes, then  you can write the scene:
```python3
class TransformFormulas(Scene):
    def construct(self):
        formula1=TexMobject("a","x","^","2","+","b","x","+","c","=","0")
        formula2=TexMobject("a","x","^","2","+","b","x","=","-","c")
        formula3=TexMobject("x","^","2","+","{","b","\\over","a","}","x","=","-","{","c","\\over","a","}")

        self.play(Write(formula1))

        changes1=[
        (   0,  1,  3,  4,  5,  6,  7,  8,  9,      ),
        (   0,  1,  3,  4,  5,  6,  8,  9,  7,  )   
        ]
        changes2=[
        (   0,  1,  3,  4,  5,  6,  7,  8,  9,  ),
        (   7,  0,  2,  3,  5,  9,  10, 11, 13, )
        ]

        # Changes 1
        self.play(
            *[
                ReplacementTransform(
                    formula1[pre_formula],formula2[pos_formula]
                    )
                for pre_formula,pos_formula in zip(changes1[0],changes1[1])
            ],
                FadeOut(formula1[10])
            )

        self.wait()
        # Changes 2

        self.play(
            *[
                ReplacementTransform(
                    formula2[pre_formula],formula3[pos_formula]
                    )
                for pre_formula,pos_formula in zip(changes2[0],changes2[1])
            ],
                ReplacementTransform(formula2[0].copy(),formula3[15]), # Copy
                *[Write(formula3[i])for i in [6,14]],
            )

        self.wait()
```

And this is the result is that we want to.
