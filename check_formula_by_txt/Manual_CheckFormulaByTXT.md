# Format:
Copy the code from [here](https://github.com/Elteoremadebeethoven/MyAnimations/blob/master/check_formula_by_txt/check_formula_by_txt.py) and paste it in your code, and create an scene like this:
```python3
class CheckFormula(CheckFormulaByTXT):
    CONFIG={
      "text":TexMobject("...") # or TextMobject
    }
```
## Example:
```python3
class CheckFormula(CheckFormulaByTXT):
    CONFIG={
    "text":TexMobject(
        "\\sqrt{",
        "\\left(",
        "x",
        "+",
        "{",
        "b",
        "\\over",
        "2",
        "a",
        "}",
        "\\right)",
        "^",
        "2",
        "}",
        "=",
        "\\pm",
        "\\sqrt{",
        "{",
        "b",
        "^",
        "2",
        "-",
        "4",
        "a",
        "c",
        "\\over",
        "4",
        "a",
        "^",
        "{",
        ")",
        )
    }
```
The result is:
