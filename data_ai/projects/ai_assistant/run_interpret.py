import openai
import sys
import os
import datetime

def read_data_file(file_name):
    """Read and return the content of a JSON file."""
    with open(file_name, "r") as file:
        data = file.read()
    return data

def retrieve_date_and_time():
    """Return the current date and time formatted as a string."""
    current_datetime = datetime.datetime.now()
    return current_datetime.strftime("%Y-%m-%d %H:%M:%S")

def send_data_to_ai(api_key, ai_role, ai_user_input):
    """Send provided data to OpenAI for analysis and return the result."""
    openai.api_key = api_key
    try:
        completion = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[ai_role, ai_user_input]
        )
        return completion.choices[0].message
    except Exception as err:
        return f"[ERROR] : An error occurred: {type(err).__name__} - {err}"

def main():
    input_file = input("Input File = ")
    API_key = input("API Key = ")

    if not os.path.exists(input_file):
        print(f"[ERROR] : File '{input_file}' does not exist.")
        sys.exit(1)

    jsonData = read_data_file(input_file)

    ai_role = {"role": "system", "content": "Enter your prompt here."}
    ai_user_input = {"role": "user", "content": f"JSON data - {jsonData}"}

    print(f"Result: {send_data_to_ai(API_key, ai_role, ai_user_input)}")

if __name__ == "__main__":
    main()
