import streamlit as st
import math

# --- Calculator Logic ---

def calculate(num1, num2, operation):
    """Performs the selected arithmetic or scientific operation."""
    
    # 1. Handle unary operations (only num1 is required)
    unary_operations = ['sqrt', 'sin', 'cos', 'tan', 'log', 'exp']
    
    if operation in unary_operations:
        try:
            num1 = float(num1)
        except ValueError:
            return "Error: Invalid number input for scientific function."
            
        if operation == 'sqrt':
            if num1 < 0:
                return "Error: Cannot calculate square root of a negative number."
            return math.sqrt(num1)
        elif operation == 'sin':
            # Use math.radians to convert degrees (common calculator input) to radians
            return math.sin(math.radians(num1))
        elif operation == 'cos':
            return math.cos(math.radians(num1))
        elif operation == 'tan':
            # Convert to radians and handle potential division by zero near 90 or 270 degrees
            rad = math.radians(num1)
            # Check if input is close to odd multiple of 90 degrees
            if abs(math.cos(rad)) < 1e-9: 
                 return "Error: Tangent undefined (near 90° or 270°)."
            return math.tan(rad)
        elif operation == 'log':
            if num1 <= 0:
                return "Error: Logarithm input must be positive (using base 10)."
            return math.log10(num1) # Using log base 10
        elif operation == 'exp':
            return math.exp(num1)

    # 2. Handle binary operations (requires both num1 and num2)
    try:
        num1 = float(num1)
        num2 = float(num2)
    except ValueError:
        return "Error: Invalid number input for binary operation."

    if operation == '+':
        return num1 + num2
    elif operation == '-':
        return num1 - num2
    elif operation == '*':
        return num1 * num2
    elif operation == '/':
        if num2 == 0:
            return "Error: Cannot divide by zero."
        return num1 / num2
    elif operation == '^': # Power operation
        return num1 ** num2
    else:
        return "Error: Invalid operation."

# --- Streamlit UI Setup ---

st.set_page_config(
    page_title="Scientific Streamlit Calculator",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.title("🔬 Scientific Streamlit Calculator")

st.markdown(r"""
Perform basic arithmetic and scientific calculations. 
Note: For functions like $\sqrt{x}$, $\sin(x)$, $\log(x)$, etc., only the **First Number** (x) is used.
---
""")

# Input Fields using st.columns for responsive layout
col1, col2 = st.columns(2)

with col1:
    # Changed default value to 9 for easier sqrt testing
    number1 = st.text_input("First Number (x)", value="9", key="num1_input")
with col2:
    number2 = st.text_input("Second Number (y) - Optional for Unary Ops", value="2", key="num2_input")

# Operation Selector
# Added scientific operations and the power operator '^'
operation = st.selectbox(
    "Select Operation",
    ('+', '-', '*', '/', '^', 'sqrt', 'sin', 'cos', 'tan', 'log', 'exp'),
    index=0
)

# Determine if the operation is unary for result display formatting
is_unary = operation in ['sqrt', 'sin', 'cos', 'tan', 'log', 'exp']

# Calculate Button
if st.button("Calculate Result", key="calculate_button", type="primary"):
    # Perform calculation
    result = calculate(number1, number2, operation)

    # Display the result
    st.markdown("### Result:")
    
    if isinstance(result, str) and result.startswith("Error"):
        # Display error message 
        st.error(f"**Calculation Failed:** {result}")
    else:
        # Display success message and trigger balloons for visual flair
        try:
            # Format result to four decimal places for scientific precision
            display_result = f"{result:,.4f}" if isinstance(result, float) else str(result)
        except:
            display_result = str(result)

        st.balloons()
        
        # Format the equation based on whether it was a unary or binary operation
        if is_unary:
            # e.g., sqrt(9) = 3.0000
            equation_str = f"**{operation}({number1})**"
        elif operation == '^':
            # e.g., 9 ^ 2 = 81.0000
            equation_str = f"**{number1} ^ {number2}**"
        else:
            # e.g., 9 + 2 = 11.0000
            equation_str = f"**{number1} {operation} {number2}**"

        st.success(f"{equation_str} = **{display_result}**")

# App footer
st.markdown("""
---
*Note: Trigonometric functions ($\sin$, $\cos$, $\tan$) assume input is in **degrees**.*
""")
