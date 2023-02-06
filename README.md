# scrapeZalora

This project scrape every images and video of all SKU listed in "Question 1 Dataset.xlsx"

## Package download
package dependencies
- selenium
- requests
- pytube
- pandas
- openpyxl

Kindly install the package above in your virtual environment using pip install for example
` pip install selenium`

## Chrome drive download
Chrome driver installation

Kindly refer to the link below for chrome driver download
After installation, kindly copy the filepath for chromedriver

## Program run
parameter to run program
- driverPath (required)  Kindly provide absolute filepath of downloaded chromedriver
- n(optional) Based on user input, program download first n SKUs media listed in "Question 1 Dataset.xlsx"

Before running program, kindly check if you have downloaded the packages and chrome drivers mentioned above
To run the program, open terminal(MacOS) / WindowPowerShell(Window) / cmd, then run the command as below
`python main.py -driverPath /Users/wykeen/Downloads/chromedriver_mac64/chromedriver -n 100`

After running program, folder path of each folder with respective media will created in 
`.\Outputs\` as figure below
<img width="1277" alt="image" src="https://user-images.githubusercontent.com/124185359/217021458-af14e0f1-aa42-46a0-b713-80883954b2cc.png">

