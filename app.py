import streamlit as st

# Initialize session state for sum if not already present
if "total" not in st.session_state:
    st.session_state.total = 0

st.title("Simple Addition App")

# User input for a number
num = st.number_input("Enter a number:", value=0, step=1)

# Add button
if st.button("Add to Total"):
    st.session_state.total += num

# Display the total sum
st.subheader(f"Running Total: {st.session_state.total}")
