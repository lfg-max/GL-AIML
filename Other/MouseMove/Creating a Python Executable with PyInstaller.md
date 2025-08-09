**Steps to Create an Executable with Dependencies Using PyInstaller**

1. **Install PyInstaller (if you haven't already):**  
   * Open your terminal or command prompt.  
   * Run the following command:  
     pip install pyinstaller

2. **Prepare Your Script and Data File(s):**  
   * Make sure your Python script (your\_script.py) and any data files (e.g., config.txt, image.png, etc.) are in the same directory, or that you know their exact paths.  
   * For this example, let's assume your\_script.py and config.txt are in the same directory.  
3. **Navigate to Your Script's Directory:**  
   * Use the cd command to change the current directory to the location of your Python script.  
   * Example:  
     cd /path/to/your/script

     (Replace /path/to/your/script with the actual path.)  
4. **Run PyInstaller with the \--add-data Option:**  
   * This is the crucial step where you create the executable and bundle your data file(s) in one command.  
   * Here's the basic command to include config.txt in the same directory as the executable:  
     pyinstaller \--onefile \--add-data "config.txt:config.txt" your\_script.py

   * **Explanation:**  
     * pyinstaller: The command to run PyInstaller.  
     * \--onefile: Creates a single executable file.  
     * \--add-data "config.txt:config.txt": This is where you specify the data file:  
       * config.txt: The path to your data file (in this case, relative to where you're running the command).  
       * config.txt: The destination path *within* the executable where the file will be placed. Using the same name here puts it in the same directory as the executable.  
     * your\_script.py: The name of your Python script.  
5. **More Complex Examples for \--add-data:**  
   * **Different Destination Directory**  
     * If you want to put the config file in a folder named "configuration"

   pyinstaller \--onefile \--add-data "config.txt:configuration" your\_script.py

   * **Multiple Data Files**  
     * To include multiple data files, separate each source:destination pair with a comma:

pyinstaller \--onefile \--add-data "config.txt:config.txt,image.png:image.png,data/info.csv:data" your\_script.py

6. **Adding Other Options:**  
   * You can combine \--add-data with other PyInstaller options:  
     * \--windowed or \-w: For GUI applications to prevent a console window from appearing.  
     * \--icon=your\_icon.ico: To add a custom icon to your executable.

Example:pyinstaller \--onefile \--windowed \--icon=myicon.ico \--add-data "config.txt:config.txt" your\_script.py

7. **Locate Your Executable:**  
   * PyInstaller places the output in a folder named dist, located in the same directory where you ran the command.  
   * Your executable will be inside the dist folder.  
8. **Run Your Executable:**  
   * **Windows:**  
     * Double-click the .exe file in the dist folder.  
     * Or, open a command prompt, navigate to the dist folder, and type the executable's name, then press Enter.  
   * **macOS/Linux:**  
     * Double-click the executable file in the dist folder.  
     * If you get a "permission denied" error:  
       * Open a terminal.  
       * Navigate to the dist folder: cd /path/to/dist (replace with the actual path).  
       * Make the executable runnable: chmod \+x your\_executable\_name (replace with the actual name).  
       * Run it: ./your\_executable\_name



       pyinstaller --onefile --add-data "config.txt:config.txt" mouse_move.py