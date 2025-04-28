import streamlit as st
import re
import random
import string


st.set_page_config(
    page_title="Password Strength Meter",
    page_icon="🔒",
    layout="centered"
)

COMMON_PASSWORDS = [
    "password", "123456", "qwerty", "admin", "welcome",
    "password123", "abc123", "letmein", "monkey", "1234567890"
]

def check_password_strength(password):
    """
    Analyze password strength based on various criteria
    Returns score and feedback
    """
    score = 0
    feedback = []


    if password.lower() in COMMON_PASSWORDS:
        feedback.append("❌ This is a commonly used password and can be easily guessed.")
        return 0, feedback
    
    if len(password) >= 8:
        score += 1
    else:
        feedback.append("❌ Password should be at least 8 characters long.")


    #extra point for very long password
    if len(password) >= 12:
        score += 1


    #upper and lowercase check (1 point)
    if re.search(r"[A-Z]", password) and re.search(r"[a-z]", password):
        score += 1
    else:
        feedback.append("❌ Include both uppercase and lowercase letters.") 


    # Digit check (1 point)
    if re.search(r"\d", password):
        score += 1
    else:
        feedback.append("❌ Add at least one number (0-9).")


    #special character check (1 point)
    if re.search(r"[!@#$%^&*]", password):
        score += 1
    else:
        feedback.append("❌ Include at least one special character (!@#$%^&*).")


     #Check for sequential characters(penalty)
    if re.search(r"(abc|bcd|cde|def|efg|fgh|ghi|hij|ijk|jkl|klm|lmn|mno|nop|opq|pqr|qrs|rst|stu|tuv|uvw|vwx|wxy|xyz)", password.lower()):
        score -= 1
        feedback.append("❌ Avoid sequential letters (like 'abc').")


    #Check for sequential numbers(penalty)
    if re.search(r"(012|123|234|345|456|567|678|789)", password):
        score -= 1
        feedback.append("❌ Avoid sequential numbers (like '123').")


    #check for repeated characters (penalty)
    if re.search(r"(.)\1{2,}", password):
        score -= 1
        feedback.append("❌ Avoid repeating numbers (like 'aaa').")    


    #Ensure score is at least 0
    score = max(0, score)

    return score, feedback


def generate_password(length=12, include_upper=True, include_lower=True,
                      include_digits=True, include_special=True):
    

    """Generate a strong random password based o criteria"""
    chars = "" 


    if include_upper:
        chars += string.ascii_uppercase
    if include_lower:    
        chars += string.ascii_lowercase
    if include_digits:
        chars += string.digits
    if include_special:
        chars += "!@#$%^&*"


    #ensure we have at least some characters to choose from
    if not chars:
        chars = string.ascii_letters + string.digits


    #Generate password
    password = ''.join(random.choice(chars) for _ in range(length))

    return password



#Main App
st.title("🔒 Password Strength Meter")
st.markdown("Check how strong your password is and get suggestions to improve it.")

#Password input
password = st.text_input("Enter your Password:", value="", type="password", key="hidden_password")

#password strength check
if password:
    score, feedback = check_password_strength(password)


    #Display Strength rating
    if score >= 5:
        strength = "Strong"
        color = "green"
        emoji = "✅"

    elif score >= 3:
        strength = "Moderate"
        color = "orange"
        emoji = "⚠"

    else:
        strength = "Weak"
        color = "red"
        emoji = "❌" 

    st.markdown(f"### Password Strength: {color} {emoji} {strength}")
    st.progress(score / 5)   #visual Strength meter


#Display feedback
    if feedback: 
        st.subheader("Feedback:")
        for item in feedback:
            st.markdown(f"- {item}")
    else:
        st.success("✅ Excellent! Your password meets all security criteria.")

#Additional password statistics 
    st.header("Password Statistics:") 
    col1, col2 = st.columns(2)
    with col1:
        st.info(f"Length: {len(password)} characters")  
        st.info(f"Uppercase letters: {len(re.findall(r'[A-Z]', password))}")  
    with col2:
        st.info(f"Lowercase letters: {len(re.findall(r'[a-z]', password))}")  
        st.info(f"Special Characters: {len(re.findall(r'[!@#$%^&*]', password))}")


    #Estimated time to crack (very simplified)
    complexity = 0

    if re.search(r"[a-z]", password): complexity += 26            
    if re.search(r"[A-Z]", password): complexity += 26      
    if re.search(r"\d", password): complexity += 10 
    if re.search(r"[!@#$%^&*]", password): complexity += 8


    if complexity > 0:
        possible_combinations = complexity ** len(password)
        if possible_combinations < 1000000:
            crack_time = "Seconds to Minutes"
        elif possible_combinations < 10000000000:
            crack_time = "Hours to Days"    
        elif possible_combinations < 10000000000000:
            crack_time = "Months" 
        else:
            crack_time = "Years to Centuries" 


        st.warning(f"Estimated time to crack: {crack_time}")

#Password Generator Section 
st.markdown("---")
st.subheader("🔒Password Generator")
st.markdown("Need a strong password? Generate one below:")

col1, col2 = st.columns(2)
with col1:
    length = st.slider("Password Length", min_value=8, max_value=30, value=12)
    include_upper = st.checkbox("Include Uppercase Letters", value=True)
    include_lower = st.checkbox("Include Lowercase Letters", value=True)

with col2:
    include_digits = st.checkbox("Include Numbers", value=True)    
    include_special = st.checkbox("Include Special Characters", value=True)

if st.button("Generate Strong Password"):
    generated_password = generate_password(
        length, include_upper, include_lower, include_digits, include_special 
    )
    st.code(generated_password)


    #check the strength of generated password
    gen_score, gen_feedback = check_password_strength(generated_password)
    st.progress(gen_score / 5)

    if gen_score >= 5:
        st.success("✅ Generated a Strong Password!")  
    else:
        st.warning("⚠ Try adjusting the options to generate a strongest password.") 

#Educational section
st.markdown("---")
st.subheader("📚 Password Security Tips")
st.markdown("""
- Use a different password for each account
- Consider using a password manager
- Enable two-factor authentication when available            
- Change your passwords regularly             
- Never share your password with others
- Avoid using personal information in your passwords
            """)                     