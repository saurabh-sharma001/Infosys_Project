import streamlit as st
from auth_db import create_users_table, register_user, validate_user

# ---------- PAGE CONFIG (MUST BE FIRST) ----------
st.set_page_config(page_title="Analytics", page_icon="🌎", layout="wide")

# ---------- CREATE USERS TABLE ----------
create_users_table()

# ---------- SESSION STATE ----------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "page" not in st.session_state:
    st.session_state.page = "login"


# ---------- PAGE SWITCH ----------
def switch_page(page):
    st.session_state.page = page
    st.rerun()


# ===============================
# ✅ CENTERED LOGIN PAGE (NO HTML)
# ===============================
def login_page():
    left, center, right = st.columns([2, 3, 2])

    with center:
        st.markdown("## 🔑 Login")

        st.markdown("---")

        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login", use_container_width=True):
            user = validate_user(username, password)
            if user:
                st.session_state.logged_in = True
                st.success("✅ Login Successful")
                st.rerun()
            else:
                st.error("❌ Invalid Username or Password")

        st.markdown("")

        st.info("Don't have an account?")
        if st.button("Go to Signup", use_container_width=True):
            switch_page("signup")


# ===============================
# ✅ CENTERED SIGNUP PAGE
# ===============================
def signup_page():
    left, center, right = st.columns([2, 3, 2])

    with center:
        st.markdown("## 📝 Signup")

        st.markdown("---")

        username = st.text_input("Create Username")
        password = st.text_input("Create Password", type="password")
        confirm = st.text_input("Confirm Password", type="password")

        if st.button("Signup", use_container_width=True):
            if password != confirm:
                st.error("❌ Passwords do not match")
            elif username.strip() == "" or password.strip() == "":
                st.error("❌ Fields cannot be empty")
            elif register_user(username, password):
                st.success("✅ Account Created Successfully!")
                switch_page("login")
            else:
                st.error("❌ Username Already Exists")

        if st.button("Back to Login", use_container_width=True):
            switch_page("login")


# ===============================
# ✅ LOGOUT
# ===============================
def logout():
    st.session_state.logged_in = False
    st.session_state.page = "login"
    st.rerun()


# ===============================
# ✅ AUTH GATE
# ===============================
if not st.session_state.logged_in:
    if st.session_state.page == "login":
        login_page()
    elif st.session_state.page == "signup":
        signup_page()
    st.stop()


# ===============================
# ✅ DASHBOARD AFTER LOGIN
# ===============================
st.title("✅ Welcome to Global Income Inequality Dashboard")
st.success("You are successfully logged in!")

import streamlit as st
import pandas as pd
import altair as alt
from datetime import date, timedelta
from streamlit_extras.metric_cards import style_metric_cards
import time

# ---------- IMPORT AUTH HELPERS ----------
from auth_db import create_users_table, register_user, validate_user

# ---------- CREATE USERS TABLE (IF NOT EXISTS) ----------
create_users_table()


# ---------- SESSION STATE ----------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "page" not in st.session_state:
    st.session_state.page = "login"


# ---------- PAGE SWITCH HELPER ----------
def switch_page(page: str):
    st.session_state.page = page
    st.rerun()


# ---------- LOGIN PAGE ----------
def login_page():
    st.title("🔐 Login to Global Income Inequality Dashboard")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        user = validate_user(username, password)
        if user:
            st.session_state.logged_in = True
            st.success("✅ Login Successful")
            st.rerun()
        else:
            st.error("❌ Invalid Username or Password")

    st.info("Don't have an account?")
    if st.button("Go to Signup"):
        switch_page("signup")


# ---------- SIGNUP PAGE ----------
def signup_page():
    st.title("📝 Create a New Account")

    username = st.text_input("Create Username")
    password = st.text_input("Create Password", type="password")
    confirm = st.text_input("Confirm Password", type="password")

    if st.button("Signup"):
        if password != confirm:
            st.error("❌ Passwords do not match")
        elif username.strip() == "" or password.strip() == "":
            st.error("❌ Username and password cannot be empty")
        elif register_user(username, password):
            st.success("✅ Account created successfully! Please login.")
            switch_page("login")
        else:
            st.error("❌ Username already exists. Try another.")

    if st.button("Back to Login"):
        switch_page("login")


# ---------- LOGOUT ----------
def logout():
    st.session_state.logged_in = False
    st.session_state.page = "login"
    st.rerun()


# ---------- AUTH GATE ----------
if not st.session_state.logged_in:
    if st.session_state.page == "login":
        login_page()
    elif st.session_state.page == "signup":
        signup_page()
    st.stop()   # 🚫 Don't run dashboard until logged in 

#---------------dark mode-------------------

# ---------------- DARK MODE TOGGLE ----------------
st.sidebar.subheader("🌓 Theme")

if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

dark_toggle = st.sidebar.toggle("Enable Dark Mode")

st.session_state.dark_mode = dark_toggle

if st.session_state.dark_mode:
    st.markdown("""
    <style>
        .stApp {
            background-color: #0E1117;
            color: white;
        }
        h1, h2, h3, h4 {
            color: #FAFAFA;
        }
        .stSidebar {
            background-color: #161B22;
        }
        div[data-testid="metric-container"] {
            background-color: #161B22;
            border-left: 6px solid #00ffcc;
        }
    </style>
    """, unsafe_allow_html=True)



# ================== DASHBOARD STARTS AFTER THIS LINE ==================



# ---------------- ANIMATED KPI FUNCTION ----------------
def animated_metric(label, value, prefix="", suffix="", duration=1.2):
    placeholder = st.empty()
    steps = 50
    delay = duration / steps

    for i in range(steps + 1):
        current = int((value / steps) * i)
        placeholder.metric(
            label=label,
            value=f"{prefix}{current:,.0f}{suffix}"
        )
        time.sleep(delay)

# ---------------- SIDEBAR LOGO ----------------
st.sidebar.image("logo2.png")

# ---------------- TITLE ----------------
st.title("⏱ GLOBAL INCOME INEQUALITY DASHBOARD")

# ---------------- LOAD CSS ----------------
with open('style.css') as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ---------------- LOAD DATASET ----------------
df = pd.read_excel("Income_dataset.xlsx", sheet_name="Income_dataset")

# -------------------- SIDEBAR FILTERS --------------------
st.sidebar.header("🔍 Data Filters")

gender_filter = st.sidebar.multiselect(
    "Select Gender", df["Gender"].unique(), df["Gender"].unique()
)
country_filter = st.sidebar.multiselect(
    "Select Country", df["Country"].unique(), df["Country"].unique()
)
education_filter = st.sidebar.multiselect(
    "Select Education", df["Education"].unique(), df["Education"].unique()
)
industry_filter = st.sidebar.multiselect(
    "Select Industry", df["Industry"].unique(), df["Industry"].unique()
)
marital_filter = st.sidebar.multiselect(
    "Marital Status", df["Marital_Status"].unique(), df["Marital_Status"].unique()
)
insurance_filter = st.sidebar.multiselect(
    "Has Insurance?", df["Has_Insurance"].unique(), df["Has_Insurance"].unique()
)
income_bracket_filter = st.sidebar.multiselect(
    "Income Bracket", df["Income_Bracket"].unique(), df["Income_Bracket"].unique()
)

age_range = st.sidebar.slider(
    "Select Age Range",
    int(df["Age"].min()),
    int(df["Age"].max()),
    (int(df["Age"].min()), int(df["Age"].max()))
)

exp_range = st.sidebar.slider(
    "Select Experience (Years)",
    int(df["Experience_Years"].min()),
    int(df["Experience_Years"].max()),
    (int(df["Experience_Years"].min()), int(df["Experience_Years"].max()))
)

income_range = st.sidebar.slider(
    "Select Annual Income (USD)",
    int(df["Annual_Income_USD"].min()),
    int(df["Annual_Income_USD"].max()),
    (int(df["Annual_Income_USD"].min()), int(df["Annual_Income_USD"].max()))
)

credit_range = st.sidebar.slider(
    "Select Credit Score",
    int(df["Credit_Score"].min()),
    int(df["Credit_Score"].max()),
    (int(df["Credit_Score"].min()), int(df["Credit_Score"].max()))
)

# -------------------- APPLY ALL FILTERS --------------------
df2 = df[
    (df["Gender"].isin(gender_filter)) &
    (df["Country"].isin(country_filter)) &
    (df["Education"].isin(education_filter)) &
    (df["Industry"].isin(industry_filter)) &
    (df["Marital_Status"].isin(marital_filter)) &
    (df["Has_Insurance"].isin(insurance_filter)) &
    (df["Income_Bracket"].isin(income_bracket_filter)) &
    (df["Age"].between(age_range[0], age_range[1])) &
    (df["Experience_Years"].between(exp_range[0], exp_range[1])) &
    (df["Annual_Income_USD"].between(income_range[0], income_range[1])) &
    (df["Credit_Score"].between(credit_range[0], credit_range[1]))
]

# -------------------- KPI SECTION (ANIMATED) --------------------
st.subheader("📌 Key Performance Indicators")

col1, col2, col3, col4 = st.columns(4)

with col1:
    animated_metric("👥 Total People", df2.shape[0])

with col2:
    animated_metric("💰 Total Annual Income", int(df2["Annual_Income_USD"].sum()), prefix="$")

with col3:
    animated_metric("📈 Highest Income", int(df2["Annual_Income_USD"].max()), prefix="$")

with col4:
    animated_metric("📉 Lowest Income", int(df2["Annual_Income_USD"].min()), prefix="$")

style_metric_cards(
    background_color="#FFFFFF",
    border_left_color="#FF5733",
    border_color="#2E86C1",
    box_shadow="#AF7AC5"
)

# ---------------- SECOND ROW KPIs ----------------
col5, col6, col7, col8 = st.columns(4)

with col5:
    animated_metric("💸 Avg Monthly Expense", int(df2["Monthly_Expenses_USD"].mean()), prefix="$")

with col6:
    animated_metric("🏦 Avg Savings", int(df2["Savings_USD"].mean()), prefix="$")

with col7:
    animated_metric("🏛 Avg Loan Amount", int(df2["Loan_Amount_USD"].mean()), prefix="$")

with col8:
    animated_metric("📊 Avg Credit Score", int(df2["Credit_Score"].mean()))

style_metric_cards(
    background_color="#F1F8E9",
    border_left_color="#FFD700",
    border_color="#2ECC71",
    box_shadow="#F4D03F"
)

# ---------------- INSURANCE KPIs ----------------
col9, col10 = st.columns(2)

insured_count = df2[df2["Has_Insurance"] == "Yes"].shape[0]
not_insured_count = df2[df2["Has_Insurance"] == "No"].shape[0]

with col9:
    animated_metric("✅ People With Insurance", insured_count)

with col10:
    animated_metric("❌ People Without Insurance", not_insured_count)

# ---------------- BAR GRAPHS (2x2 GRID) ----------------
chart_col1, chart_col2 = st.columns(2)

# 1️⃣ Avg Income by Country
with chart_col1:
    st.subheader("🌍 Average Income by Country")
    source = pd.DataFrame({
        "Average Income (USD)": df2.groupby("Country")["Annual_Income_USD"].mean(),
        "Country": df2.groupby("Country")["Annual_Income_USD"].mean().index
    })
    bar_chart = alt.Chart(source).mark_bar(color="#1f77b4").encode(
        x="Average Income (USD):Q",
        y=alt.Y("Country:N", sort="-x"),
        tooltip=["Country", alt.Tooltip("Average Income (USD)", format=",")]
    )
    st.altair_chart(bar_chart, use_container_width=True, theme=None)

# 2️⃣ Avg Savings by Country
with chart_col2:
    st.subheader("💰 Average Savings by Country")
    source = pd.DataFrame({
        "Average Savings (USD)": df2.groupby("Country")["Savings_USD"].mean(),
        "Country": df2.groupby("Country")["Savings_USD"].mean().index
    })
    bar_chart = alt.Chart(source).mark_bar(color="#2ECC71").encode(
        x="Average Savings (USD):Q",
        y=alt.Y("Country:N", sort="-x"),
        tooltip=["Country", alt.Tooltip("Average Savings (USD)", format=",")]
    )
    st.altair_chart(bar_chart, use_container_width=True, theme=None)

# 3️⃣ Avg Loan Amount by Country
with chart_col1:
    st.subheader("🏛 Average Loan Amount by Country")
    source = pd.DataFrame({
        "Average Loan (USD)": df2.groupby("Country")["Loan_Amount_USD"].mean(),
        "Country": df2.groupby("Country")["Loan_Amount_USD"].mean().index
    })
    bar_chart = alt.Chart(source).mark_bar(color="#FF5733").encode(
        x="Average Loan (USD):Q",
        y=alt.Y("Country:N", sort="-x"),
        tooltip=["Country", alt.Tooltip("Average Loan (USD)", format=",")]
    )
    st.altair_chart(bar_chart, use_container_width=True, theme=None)

# 4️⃣ Avg Credit Score by Country
with chart_col2:
    st.subheader("📊 Average Credit Score by Country")
    source = pd.DataFrame({
        "Average Credit Score": df2.groupby("Country")["Credit_Score"].mean(),
        "Country": df2.groupby("Country")["Credit_Score"].mean().index
    })
    bar_chart = alt.Chart(source).mark_bar(color="#9C27B0").encode(
        x="Average Credit Score:Q",
        y=alt.Y("Country:N", sort="-x"),
        tooltip=["Country", alt.Tooltip("Average Credit Score", format=".0f")]
    )
    st.altair_chart(bar_chart, use_container_width=True, theme=None)

# ---------------- PROGRESS BARS ----------------
# Insurance coverage
total_people = df2.shape[0]
insured_people = df2[df2["Has_Insurance"] == "Yes"].shape[0]
insurance_pct = int((insured_people / total_people) * 100) if total_people > 0 else 0

st.subheader("✅ Insurance Coverage Progress")
st.progress(insurance_pct)
st.caption(f"{insurance_pct}% of people have insurance coverage")

# Average savings vs max savings
max_savings = df["Savings_USD"].max()
avg_savings = df2["Savings_USD"].mean()
savings_pct = int((avg_savings / max_savings) * 100) if max_savings > 0 else 0

st.subheader("💰 Average Savings Progress")
st.progress(savings_pct)
st.caption(f"Average savings of filtered users is {savings_pct}% of the max savings")

# ---------------- ANIMATED COLUMN CHARTS ----------------
st.subheader("Column Charts")

left, right = st.columns(2)

with left:
    st.markdown("### 🌍 People Count by Country")
    placeholder_left = st.empty()

with right:
    st.markdown("### 🏭 People Count by Industry")
    placeholder_right = st.empty()

source_country = df2["Country"].value_counts().reset_index()
source_country.columns = ["Country", "Total People"]

source_industry = df2["Industry"].value_counts().reset_index()
source_industry.columns = ["Industry", "Total People"]

max_len = max(len(source_country), len(source_industry))

for i in range(1, max_len + 1):
    if i <= len(source_country):
        animated_country = alt.Chart(source_country.iloc[:i]).mark_bar().encode(
            x=alt.X("Country:N", sort="-y"),
            y="Total People:Q",
            tooltip=["Country", "Total People"]
        ).properties(width=300, height=300)
        placeholder_left.altair_chart(animated_country)

    if i <= len(source_industry):
        animated_industry = alt.Chart(source_industry.iloc[:i]).mark_bar().encode(
            x=alt.X("Industry:N", sort="-y"),
            y="Total People:Q",
            tooltip=["Industry", "Total People"]
        ).properties(width=300, height=300)
        placeholder_right.altair_chart(animated_industry)

    time.sleep(0.4)

# ---------------- EDUCATION RADIO SLICER (EXTRA) ------------------------------------------------------------
st.sidebar.subheader("🎓 Education")
education_filter = st.sidebar.radio(
    "Select Education",
    options=["All"] + list(df["Education"].unique())
)

if education_filter != "All":
    df2 = df2[df2["Education"] == education_filter]

# ---------------- SIDEBAR LOGOUT --------------------------------------------------------------------------
st.sidebar.button("🔒 Logout", on_click=logout)

st.subheader("📊 Gender Distribution & Savings vs Income")

left_col, right_col = st.columns(2)

# ---------------- DONUT CHART ----------------
with left_col:
    st.markdown("### 👥 Gender Distribution")

    gender_count = df2["Gender"].value_counts().reset_index()
    gender_count.columns = ["Gender", "Total"]

    donut = alt.Chart(gender_count).mark_arc(innerRadius=70).encode(
        theta="Total:Q",
        color="Gender:N",
        tooltip=["Gender", "Total"]
    ).properties(height=350)

    st.altair_chart(donut, use_container_width=True)


# ---------------- SCATTER PLOT ----------------
with right_col:
    st.markdown("### 💸 Savings vs Annual Income")

    scatter = alt.Chart(df2).mark_circle(size=80).encode(
        x="Annual_Income_USD:Q",
        y="Savings_USD:Q",
        tooltip=["Country", "Annual_Income_USD", "Savings_USD", "Gender"]
    ).properties(height=350)

    st.altair_chart(scatter, use_container_width=True)


    import altair as alt
import time

st.subheader("📈 Life-Style Income Growth")

line_data = df2.groupby("Experience_Years")["Annual_Income_USD"].mean().reset_index()

placeholder = st.empty()

for i in range(2, len(line_data) + 1):
    animated_line = alt.Chart(line_data.iloc[:i]).mark_line(
        strokeWidth=4,
        point=True
    ).encode(
        x=alt.X("Experience_Years:Q", title="Years of Experience"),
        y=alt.Y("Annual_Income_USD:Q", title="Avg Income"),
        tooltip=["Experience_Years", "Annual_Income_USD"]
    ).properties(height=420)

    placeholder.altair_chart(animated_line, use_container_width=True)
    time.sleep(0.15)


st.subheader("💸 Savings Growth Pattern")

area_data = df2.groupby("Experience_Years")["Savings_USD"].mean().reset_index()

area_chart = alt.Chart(area_data).mark_area(
    opacity=0.6
).encode(
    x="Experience_Years:Q",
    y="Savings_USD:Q",
    tooltip=["Experience_Years", "Savings_USD"]
).properties(height=420)

st.altair_chart(area_chart, use_container_width=True)



#===================image=========================

# ===================== POWER BI DASHBOARD SECTION =====================

st.markdown("---")
st.subheader("📊 Power BI Dashboard")

st.info(
    "This is the Power BI version of the Global Income Inequality Dashboard. "
    "You can preview it below, download the PBIX file, or open it directly in Power BI Service."
)

# ---------------- DASHBOARD IMAGE PREVIEW ----------------
try:
    st.image(
        "Dashboard.jpg",  # ✅ Change name if your file is different
        caption="Power BI Dashboard Preview",
        use_container_width=True
    )
except:
    st.warning("⚠ Dashboard preview image not found. Please add 'powerbi_preview.png' to the project folder.")


powerbi_col1, powerbi_col2 = st.columns(2)

# ---------------- OPEN POWER BI ONLINE ----------------
with powerbi_col2:
    st.markdown("### 🌐 Open Power BI Online")

    st.link_button(
        "🚀 Open Dashboard in Power BI",
        "https://app.powerbi.com/"
    )

    st.caption("Login with your Microsoft account to upload & publish the dashboard.")


#--------------about us-----------------
# ===================== ABOUT US PAGE =====================

st.markdown("---")
st.subheader("👨‍💻 About Us")

st.markdown("""
### 📊 Global Income Inequality Dashboard

This project is developed as a **data analytics & visualization system** to analyze:

- Income Distribution  
- Savings & Loans  
- Credit Scores  
- Gender & Industry Trends  
- Insurance Coverage  
- Financial Behavior Across Countries  

---

### 🎯 Project Objective
To transform **raw financial data into meaningful insights** using:

- ✅ Python  
- ✅ Streamlit  
- ✅ Power BI  
- ✅ Data Visualization  
- ✅ Interactive Dashboards  

---

### 🚀 Developed By
**Saurabh Sharma**  
*MCA (Data Science & Analytics)*  
Aspiring Data Analyst | Power BI | Python | SQL | Dashboarding  

---

### 📩 Contact
- LinkedIn:*www.linkedin.com/in/saurabh-data-analytics*

---

✅ This application is built for **learning, analysis, and presentation purposes**.
""")
