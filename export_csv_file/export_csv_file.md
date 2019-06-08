# Create a list of the elements of a TeX
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


And a .csv that you can find at `/proyect_path/name_of_file.py/scene_name.csv`
In our example the diretory is: `my_projects/project/FormulaCSV.py`

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

So the change is affected in the .csv file too:

## Create a .csv file with pairs

Soupose that we can do this transformation:



Then, we have to write three formulas, and we have to use ReplacementTransform.

Copy [this](https://github.com/Elteoremadebeethoven/MyAnimations/blob/master/export_csv_file/export_csv_pairs.py) code in your project, and create a class for each formula, you can remove the empty elements:

```python3
class Formula1CSV(ExportCSVPairs):
    CONFIG={
    "csv_name":"Formula", # <- Name of the series of formulas, this name is the same for all formulas
    "csv_number":0,       # <- This is a formula number 0
    "text":TexMobject("a","x","^","2","+","b","x","+","c","=","0"),
    "remove":[2]
    }

class Formula2CSV(ExportCSVPairs):
    CONFIG={
    "csv_name":"Formula", # <- Name of the series of formulas, this name is the same for all formulas
    "csv_number":1,       # <- This is a formula number 1
    "text":TexMobject("a","x","^","2","+","b","x","=","-","c"),
    "remove":[2]
    }

class Formula3CSV(ExportCSVPairs):
    CONFIG={
    "csv_name":"Formula", # <- Name of the series of formulas, this name is the same for all formulas
    "csv_number":2,       # <- This is a formula number 2
    "text":TexMobject("x","^","2","+","{","b","\\over","a","}","x","=","-","{","c","\\over","a","}"),
    "remove":[1,4,7,11,15]
    }

class FormulaFiles(ExportCSVPairs):
    CONFIG={
    "csv_name":"Formula", # <- Name of the series of formulas, this name is the same for all formulas
    "csv_range":2, # This is the range of the formulas, start with the formula 0 and ends with formula 2
    "csv_complete":True   # <- Use this line to create the entire document
    }
```

If you render all scenes with `-as` then you create a scenes.png and .csv files:


You can delete the `_None.csv`file, in the `formula.csv` file you can see this:


And, with a little work you can organice the elements to do the ReplatementTransform thing:
