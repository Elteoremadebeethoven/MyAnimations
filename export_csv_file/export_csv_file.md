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
