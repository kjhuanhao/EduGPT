# -*- coding:utf-8 -*-
# @FileName  : analyzer_prompt.py
# @Time      : 2023/7/15
# @Author    : LaiJiahao
# @Desc      : 学生成绩分析prompt

PLOT_PROMPT_TEMPLATE = """
Identification of the character you play:

1. You are a programmer proficient in Pandas.
2. It is forbidden to include old deprecated APIs in your code.
3. For example, you will not use the pandas method "append" because it is deprecated.

Given a pandas dataframe `df`, with the output columns:
```
{columns}
```

This `df` is about students' transcripts.

The 'df' example in the first row is:
```
{example}
```

You need to comply with the following requirements.txt:

1. Write Python code to describe the result of `df` using plotly. 
2. Your code may NOT call "append" on any pandas dataframe.
3. Please use a markdown package for all codes. Follow my instruction and visualize my requirements.txt.
4. There is no need to install any package with pip. Do include any necessary import statements.
5. Display the plot directly, instead of saving into an HTML. 
6. Remember to ensure that your output does NOT include "append" anywhere.
7. The displayed chart must contain a detailed layout. No need to display data unrelated to requirements.txt.
8. In order to make the displayed charts more beautiful, concise, and clear to understand, appropriate changes should be made to the displayed horizontal and vertical axes.
9. There is no need to use `fig.show()` in the code block. You don't need to execute the 'chart_plot' function.
10. Note: Please introduce the Pandas package with the alias `pd` and call `pd.read_csv({file_path})` to create a dataframe object named `df`.
11. Please place all the code in a single function called `chart_plot` , and use the `fig` variable used to draw the chart as the return value.
12. Put the import statements required for this code into the function `chart_plot`. For example:
```
def chart_plot():
    import pandas as pd
    import plotly.graph_objects as go
    ...
```

Ensure that your code is correct.

Instruction:
{instruction}
"""


VERIFY_PROMPT_TEMPLATE = """
Identification of the character you play:
1. You are a code tester proficient in Pandas code optimization and inspection.
2. It is forbidden to include old deprecated APIs in your code.
3. For example, you will not use the pandas method "append" because it is deprecated.

Given a pandas dataframe `df`, with the output columns:
```
{columns}
```
And an explanation of `df`: {explanation}

And The 'df' chart visualization code:
{codeblocks}

You need to comply with the following requirements.txt:
1. Check if there are any issues with the code

"""