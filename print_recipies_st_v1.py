import os
import requests
import streamlit as st

def read_ingredients(file_name):
    try:
        with open(file_name, 'r') as file:
            ingredients = [line.strip() for line in file]
        return ingredients
    except FileNotFoundError:
        st.error("File not found. Please enter a valid file name.")
    except IOError:
        st.error("Error occurred while opening the file. Please try again.")

def generate_recipes_prompt(ingredients, cuisine):
    prompt = f"Generate recipes for {cuisine} cuisine using these ingredients:\n"
    for ingredient in ingredients:
        prompt += f"- {ingredient}\n"
    return prompt

def retrieve_recipes(prompt):
    api_key = os.getenv('OPENAI_API_KEY')
    endpoint = "https://api.openai.com/v1/engines/text-davinci-003/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    data = {
        "prompt": prompt,
        "max_tokens": 500,
        "n": 1,
        "stop": None,
        "temperature": 0.1
    }
    response = requests.post(endpoint, json=data, headers=headers)
    recipes = [choice['text'].strip() for choice in response.json()["choices"]]
    return recipes

def print_recipes(recipes):
    if not recipes:
        st.write("No recipes found.")
    else:
        st.subheader("Recipes:")
        for i, recipe in enumerate(recipes, 1):
            st.write(f"Recipe {i}:")
            st.write(recipe)
            st.write("---")

def main():
    st.title("Recipe Generator")

    # Ask for the API key and save it as an environment variable
    api_key = st.text_input("Enter your OpenAI API key:")
    os.environ['OPENAI_API_KEY'] = api_key

    file = st.file_uploader("Upload the file containing the list of ingredients:", type=["txt"])

    if file is not None:
        file_contents = file.read().decode("utf-8")
        ingredients = file_contents.splitlines()

        cuisine = st.text_input("Enter the cuisine choice:")

        with st.form("generate_form"):
            if st.form_submit_button("Find Recipes"):
                prompt = generate_recipes_prompt(ingredients, cuisine)

                with st.spinner("Generating recipes..."):
                    recipes = retrieve_recipes(prompt)

                st.success("Recipes generated successfully!")
                print_recipes(recipes)
            else:
                st.info("Click 'Find Recipes' to generate recipes.")

if __name__ == '__main__':
    main()