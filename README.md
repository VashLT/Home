# Home

This repo holds those scripts and homework stored over time related to university and academic tasks.

## Notable scripts

### Whatsapp API

It's a Whatsapp web API based on `selenium webdriver` that allows messasing and sending files. This program aims to automate repetitive tasks such as sending either messages or images to whatsapp groups and contacts. In turn, the way contacts (or groups) are identified and inputted on the program make it highly automatizable to send data to different groups and contacts joinly.

The source code can be found [here](https://github.com/VashLT/Home/blob/master/Python/Scripts/Tutorer/wspp.py)

### Password manager

It's a CLI based script which uses `sqlite3` to store encrypted passwords and can be use by different users. It allows password search by labeling the passwords, implements a two-way hashing function, and more.

The source code can be found [here](https://github.com/VashLT/Home/tree/master/Python/Scripts/PW)

### Weight tracker

This program aims to make easier to keep track your daily weight and calories per day data. Based on inputed weight info (e.g. weight, current calories, etc) it connects to Google sheets (using `gspread` and OAuth API) and register the data in fancy styled tables. Since is intended to month-based diet and workout plans, creates new sheets named with the underlying month based on an initial date.

The source code can be found [here](https://github.com/VashLT/Home/tree/master/Python/Workout_ss)

### MyFitnessPAL autofiller

#### What is MyFitnessPAL?

MyFitnessPAL is a fitness application which allows to record your daily food in an ingredient-by-ingredient way, letting you know the amount of calories and macronutrients of the food you eat.

#### What does the script do?

Using `selenium webdriver` automate food registration in [myfitnesspal](www.myfitnesspal.com) through data dictionaries, which contain information about food and meal type. In turn, handles user logged in to the web page and the elimination of meals.

The source code can be found [here](https://github.com/VashLT/Home/tree/master/Python/Scripts/MyFitnessPAL)
