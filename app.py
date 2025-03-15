import streamlit as st
import google.generativeai as genai
import pandas as pd
import re
import chainladder as cl

# Configure the Gemini API
genai.configure(api_key="AIzaSyAY8kCHicriVcnnPnQK_0sh6B-8K6GCbZs")
model = genai.GenerativeModel("gemini-2.0-flash")

st.title("Actuarial Science Chatbot 🤖")

# Upload CSV File
uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

# User Query Input
query = st.text_area("Enter your actuarial science query:")

if st.button("Generate Code and Run"):
    if uploaded_file is not None and query:
        # Read CSV
        df = pd.read_csv(uploaded_file)
        csv_data = df.to_csv(index=False)

        # Prompt for the Gemini model
        prompt = f"""
        You are an expert in actuarial science and insurance analytics. Given the following loss dataset: {csv_data}
        {query}
        Give the python code to calculate the Incurred using Chainladder package.
        Reference Code:
        xyx = cl.Triangle(
            data=xyz_df,
            origin="AccidentYear",
            development="DevelopmentYear",
            columns=[],
            cumulative=True,
        )

        * Note: 
            1. Just give the simple code as given above; don't make it complex.
            2. Just print the output like xyz['**']
        """

        # Generate response from Gemini
        response = model.generate_content(prompt)

        # Extract Python code block
        match = re.search(r"```python(.*?)```", response.text, re.DOTALL)
        if match:
            python_code = match.group(1).strip()
            st.code(python_code, language="python")

            # Execute the Python code locally
            try:
                exec_globals = {"cl": cl, "pd": pd, "df": df}  # Import required modules
                exec(python_code, exec_globals)
                st.success("Executed Successfully!")
                st.write("Output:", exec_globals)  # Display execution output
            except Exception as e:
                st.error(f"Error executing code: {e}")
        else:
            st.warning("No Python code found in the response.")

    else:
        st.warning("Please upload a CSV file and enter a query.")

