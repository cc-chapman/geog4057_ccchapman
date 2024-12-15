## Code Development
This code was developed by first exploring the data in a Jupyter Notebook following the guidence provided by Professor Wang. Then, once the basic code blocks were developed and tested, the code was copied into a Python file and executed to create the desired shapefiles in the ArcGIS project. Last, portions of the Python code were copied into a Python Tool within the ArcGIS project.

## How to Use this Code
This code can be executed one of three ways.

### Method 1: Jupyter Notebook
- After activating an ArcPyClone kernel, you can edit and execute this code directly from the Jupyter Notebook.

### Method 2: Python Code
- First, edit the code in the project1.py file to match your filepaths
- Using a Command Prompt terminal, you can then run `python project1.py notax_fc.shp` to create a new shapefile

### Method 3: ArcGIS Tool
- For this method, you do not need to use a code editor at all.
- Instead, copy project1.py, project1_json.pyt, and the contents of the data folder to your ArcGIS project folder.
- Then refresh your toolboxes in ArcGIS Pro and run the tool from the ArcGIS interface.