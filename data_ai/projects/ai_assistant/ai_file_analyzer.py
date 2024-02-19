#!/usr/bin/env python
# ====================================================================
# Script Name    : openai_file_analyzer.py
# Script Version : 01
# Created        : 02/18/2024
# Modified       : 02/18/2024
# Author         : Samuel Georgiev
# Email          : samgeo.us@gmail.com
# Description    : Sends json file to OpenAI for analysis. Where analysis are based on content within script.
# Notes          : API key is needed to accsess OpenAI. You can define the API key as an environmental variable called "OPENAI_API_KEY"  
# Usage          : See below
#                  python openai_file_analyzer.py your_file_name.json
#                  openai_file_analyzer.py your_file_name.json
#                  ./openai_file_analyzer.py "C:\test\test1\exports\yourfile.json"
# ====================================================================

import openai
import sys
import os
import datetime

# --------------------------------------------------------------------
# Reads only .json files & returns their content
# def readDataFile(fileName):
# --------------------------------------------------------------------
def readDataFile(fileName):
    with open(fileName, "r") as file:
        data = file.read()
    return data


# --------------------------------------------------------------------


# --------------------------------------------------------------------
# Returns currenrt date and time
# --------------------------------------------------------------------
def retrieveDateandTimeime():
    # Get the current date and time
    currentDatetime = datetime.datetime.now()

    # Format the date and time as a string
    formattedDatetime = currentDatetime.strftime("%Y-%m-%d %H:%M:%S")

    # Print the formatted date and time
    return formattedDatetime


# --------------------------------------------------------------------


# --------------------------------------------------------------------
# sendDataToAi(aiRole, aiUserInput):
# --------------------------------------------------------------------
def sendDataToAi(aiRole, aiUserInput):
    resultData = ""
    completion = None
    if openai.api_key is None or openai.api_key == "":
        resultData = "[ERROR] : You have not provided API key."
        return resultData

    try:
        completion = openai.ChatCompletion.create(model="gpt-4-1106-preview", messages=[aiRole, aiUserInput])
    except Exception as err:
        resultData = f"[ERROR] : An error occured: {type(err).__name__}-{err}"
        return resultData

    resultData = completion.choices[0].message

    return resultData


# --------------------------------------------------------------------

# --------------------------------------------------------------------
# MAIN
# --------------------------------------------------------------------
def main():
    if len(sys.argv) != 2:
        print("[ERROR] : Please provide path to json file.")
        sys.exit(1)

    print("-----------------------------------------------")
    print(f"S T A R T - {retrieveDateandTimeime()}")
    print("-----------------------------------------------")

    jsonDataFile = sys.argv[1]
    print(f"[OK   ] : You provided file - {jsonDataFile}")

    if not os.path.exists(jsonDataFile):
        print(f"[ERROR] : File '{jsonDataFile}' does not exist.")
        sys.exit(1)
    else:
        print(f"[OK   ] : File '{jsonDataFile}' exist.")

    # Reads json file
    jsonData = readDataFile(jsonDataFile)

    aiRoleT = {
        "role": "system",
        "content": "Enter your promt here.",
    }

    aiUserInputT = {"role": "user", "content": f"json data - {jsonData}"}

    print(f"Your Result: {sendDataToAi(aiRoleT, aiUserInputT)}")

    print("-----------------------------------------------")
    print(f"D O N E - {retrieveDateandTimeime()}")
    print("-----------------------------------------------")


# --------------------------------------------------------------------


if __name__ == "__main__":
    main()