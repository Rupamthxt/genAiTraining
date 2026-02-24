import os
from google import genai
from google.genai import types

client = genai.Client(api_key="your_api_key_here")

def generate_response(instructions, question):
    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        config=types.GenerateContentConfig(
            system_instruction=instructions,
            temperature=0.2
        ),
        contents=question
    )

    return response.text

def main():
    print("Write your questions below......")
    instruction = "Your'e a professor of engineering college, answer accordingly"
    
    prompt = input("What do you want to know today?  ")

    result = generate_response(instruction, prompt)

    print("\n" + result)


if __name__ == "__main__":
    main()