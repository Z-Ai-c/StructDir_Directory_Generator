# StructDir_Directory_Generator


## Requirements
-Windows OS _(tested on win11 & win10)_

### notes:
If you just want to use the code quickly i've compiled an executable file named **"StructDir_v3.2.exe"** via auto-py-to-exe, you can just run that, however i've included the python code as well as a jupyter notebook file if you'd like play with it and improve the functionality or customize it to your needs:)

## Main Description:
**StructDir** is a basic directory generator to help you create project directories quickly. After setting the directory structure you can save the structure as a json template which can easily be realoaded later when you have similar project. Once you've set your structure and are happy just click **"Create Directories"** and choose the location youd like to create the new project directory.

Overall this is a really basic tool, it could probably use some more error handling and some more features but for now this is what it is. Hopfully some folks find this helpful.

### Extra Details
- Basic  _"drag & drop"_ if you need to adjust a folder postion in your directory stucture.
- Accepts custom window icons: I have included a sample "icon.ico" However you are welcome to replace it with your own custom "icon.ico". The program is looking for the "icon.ico" file in the program root location, if it fails to find one it will handle the error and default to the stock tkinter feather icon.
- Implemented renaming function for items in existing structures.
- Implemented drop down menu @ top left of the window for saving and loading templates.
- 'save templates' function will start looking for templates in a folder called "templates" in the programs root directory, if one does not exist it will create one.
- 'load templates' function will start looking for templates in a folder called "templates" in the programs root directory if one does not exist it will disregard and continue allowing user selection from any location. 

## Main application view:
![StructDir_v3 2_Main](https://github.com/Z-Ai-c/StructDir_Directory_Generator/assets/130925500/7ae29c8e-fabd-4247-a55d-b80193112209)
![StructDir_v3 2_template_menu](https://github.com/Z-Ai-c/StructDir_Directory_Generator/assets/130925500/2543315e-0e60-4dd9-8147-386d629db21d)

## Example structure _(can be found in the templates folder)_.
![StructDir_v3 2_example](https://github.com/Z-Ai-c/StructDir_Directory_Generator/assets/130925500/46710c12-0bec-415f-b879-c235c524b542)

## Example of the actual directory created by the application:
![StructDir_3 2_exampledir](https://github.com/Z-Ai-c/StructDir_Directory_Generator/assets/130925500/7b53752c-6d61-4ea4-b3af-868e241eece8)
