# gpa_calculator  🤓 ✌️  🌟 

A quick utility to check your GPA. Using this project you can check your GPA on the fly using a browser or through a CLI. Built and tested using Python ❤️ Jupyter Notebook ❤️ PyCharm  

### 1. Download the dependencies
Please use pip to download the Python dependencies for this project as well as the Chrome Web Driver. 
1. `pip install selenium`
2. `pip install click`
3. [Chrome Web Driver Download](https://chromedriver.chromium.org/downloads)

### 2. Create the files
##### 2.1 Create the `.grades` file
Please create the  .grades file and populate with your grades. Students from YU can simply copy the output from DPR (Degree Progress Report) and paste it into the .grades file. The .grades file should look like this:
```
FW2020    LE/EECS 1019 3.00    A    Major    Discrete Math for Computer Science
FW2020    LE/EECS 2001 3.00    B    Major    Intro. to the Theory of Computation
FW2020    LE/EECS 2021 4.00    B    Major    Computer Organization
FW2020    LE/EECS 2030 3.00    A+    Major   Advanced Object-Oriented Programming
FW2020    SC/MATH 1021 3.00    C+    Required for Major  Linear Algebra I
...
```
##### 2.2 create the `env.py` file
The env.py file contains the path to the Chrome Web Driver. Please configure it like so:
```
webdriver_location = r'C:\path\to\chromedriver'
```

### 3. Flags for gpa_calculator.py
The four Shell files (`cli_core.sh`, `cli_cumulative.sh`, `web_core.sh`, `web_cumulative.sh`) are preconfigured to run with the following flags
* `--cli`/`--web`:  Used for indicating the interface that the script runs on. If you'd like an interactive environment, use `--web`.  
* `--core`/`--cumulative`: Used for requesting a cumulative GPA or GPA of core subjects.

You can also simply run it like so `python gpa_calculator.py --cli --core`
