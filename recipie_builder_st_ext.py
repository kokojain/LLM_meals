import streamlit as st
import openai

def read_ingredients(file):
    try:
        contents = file.read().decode("utf-8")
        ingredients = [line.strip() for line in contents.splitlines()]
        return ingredients
    except AttributeError:
        st.error("Please upload a file.")
    except IOError:
        st.error("Error occurred while opening the file. Please try again.")

def generate_recipes_prompt(ingredients, cuisine):
    prompt = f"Generate recipes for {cuisine} cuisine using these ingredients:\n"
    for ingredient in ingredients:
        prompt += f"- {ingredient}\n"
    return prompt

def retrieve_recipes(prompt):
    openai.api_key = get_openai_key()  # Get the API key from the stored file
    response = openai.Completion.create(
        engine='text-davinci-003',
        prompt=prompt,
        max_tokens=500,
        n=1,  # Number of recipes to generate
        stop=None,
        temperature=0.1
    )
    recipes = [choice['text'].strip() for choice in response.choices]
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

def get_openai_key():
    with open("api_key.txt", "r") as file:
        api_key = file.read().strip()
    return api_key

def main():
    st.title("Recipe Generator")
    file = st.file_uploader("Upload a file", type=["txt"])
    
    if file is not None:
        ingredients = read_ingredients(file)
        
        if ingredients:
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