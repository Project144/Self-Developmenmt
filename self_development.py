import streamlit as st
from fpdf import FPDF
import base64
import re

# --- PDF generation function ---
def remove_emojis_and_symbols(text):
    # Remove emojis and replace ₹ with Rs.
    text = text.replace("₹", "Rs.")
    text = re.sub(r'[^\x00-\x7F]+', '', text)  # remove all non-ASCII (emojis, etc.)
    return text

def create_pdf(data, total_general, total_growth, percent_growth):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Title (emoji removed)
    title = remove_emojis_and_symbols("Self-Investment Reflection Summary")
    pdf.cell(200, 10, txt=title, ln=True, align='C')
    pdf.ln(10)

    for label, value in data.items():
        label_clean = remove_emojis_and_symbols(label)
        value_clean = remove_emojis_and_symbols(str(value if value else 'Not filled'))
        display_text = f"{label_clean}: Rs. {value_clean}"
        pdf.multi_cell(0, 10, txt=display_text)

    pdf.ln(5)
    pdf.multi_cell(0, 10, txt=f"Total Spent on General Expenses: Rs. {total_general}")
    pdf.multi_cell(0, 10, txt=f"Total Spent on Self-Growth: Rs. {total_growth}")
    pdf.multi_cell(0, 10, txt=f"Personal Growth Investment: {percent_growth:.1f}% of your total spending")

    # Encode PDF to base64 for download
    pdf_output = pdf.output(dest='S').encode('latin-1')
    b64 = base64.b64encode(pdf_output).decode()
    href = f'<a href="data:application/octet-stream;base64,{b64}" download="Self_Investment_Summary.pdf">Download PDF</a>'
    return href

# --- Helper to safely parse inputs ---
def safe_int(val):
    try:
        return int(val)
    except:
        return 0

# --- Streamlit UI ---
st.set_page_config(page_title="Self-Investment Reflection", layout="centered")

st.markdown("<h1 style='text-align: center;'>📊 Where Are You Investing?</h1>", unsafe_allow_html=True)
st.markdown("""
<div style='text-align: center;'>🙏 <i>This quick reflection helps you understand your spending vs your growth investments.</i></div>
""", unsafe_allow_html=True)

st.markdown("---")
st.subheader("💸 General Spending")
education = st.text_input("🏫 School/College Education (₹)")
house = st.text_input("🏠 House & Car (₹)")
gadgets = st.text_input("📱 Mobiles & Laptops (₹)")
entertainment = st.text_input("🎥 Entertainment (₹)")
fashion = st.text_input("🧥 Clothing & Fashion (₹)")
travel = st.text_input("🏖️ Travel & Picnics (₹)")
investments = st.text_input("📈 Other Investments (₹)")

st.markdown("---")
st.subheader("📈 Personal Growth Investment")
books = st.text_input("📘 Books & Knowledge Resources (₹)")
fitness = st.text_input("🏋️ Gym/Yoga/Meditation (₹)")
training = st.text_input("👔 Training & Courses (₹)")

st.markdown("---")
st.subheader("✍️ Reflection")
reflection = st.text_area("🧠 What will you change about your investment approach going forward?")

# --- Collect responses ---
data = {
    "Education": education,
    "House & Car": house,
    "Mobiles & Laptops": gadgets,
    "Entertainment": entertainment,
    "Clothing & Fashion": fashion,
    "Travel & Picnics": travel,
    "Other Investments": investments,
    "Books & Resources": books,
    "Gym/Yoga": fitness,
    "Training & Courses": training,
    "Personal Reflection": reflection
}

if st.button("✅ Submit & View Summary"):
    # --- Calculate totals ---
    general_total = sum([
        safe_int(education), safe_int(house), safe_int(gadgets),
        safe_int(entertainment), safe_int(fashion), safe_int(travel), safe_int(investments)
    ])

    growth_total = sum([
        safe_int(books), safe_int(fitness), safe_int(training)
    ])

    overall_total = general_total + growth_total
    percent_growth = (growth_total / overall_total) * 100 if overall_total > 0 else 0

    # --- Display Summary ---
    st.success("🎯 Here's your reflection summary:")
    st.markdown(f"🧾 **General Spending Total**: ₹ {general_total}")
    st.markdown(f"📘 **Self-Growth Investment Total**: ₹ {growth_total}")
    st.markdown(f"📊 **You’ve invested {percent_growth:.1f}% in personal growth.**")

    if percent_growth < 10:
        st.warning("🚨 You're investing very little in yourself. Let's level that up!")
    elif percent_growth < 20:
        st.info("⚠️ Not bad, but there's room to grow!")
    else:
        st.success("💪 Great job! You're prioritizing self-investment.")

    st.markdown("---")
    pdf_link = create_pdf(data, general_total, growth_total, percent_growth)
    st.markdown(pdf_link, unsafe_allow_html=True)
