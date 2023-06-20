# Ask for the API key and save it as an environment variable
api_key = st.text_input("Enter your OpenAI API key:")
os.environ['OPENAI_API_KEY'] = api_key

file_name = st.text_input("Enter the file name containing the list of ingredients:")

if file_name:
    ingredients = read_ingredients(file_name)

    if ingredients:
        cuisine = st.text_input("Enter the cuisine choice:")

        if st.button("Find Recipes"):
            prompt = generate_recipes_prompt(ingredients, cuisine)

            with st.spinner("Generating recipes..."):
                recipes = retrieve_recipes(prompt)

            st.success("Recipes generated successfully!")
            print_recipes(recipes)

            for recipe in recipes:
                total_calories = calculate_calories(recipe)
                fda_approval_status = check_fda_approval(recipe)

                st.write("Total Calories:", total_calories)
                st.write("FDA Approval Status:", "Approved" if fda_approval_status else "Not Approved")

else:
    st.info("Enter the file name to proceed.")