import streamlit as st
import re

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="Wayfind AI",
    page_icon="🧭",
    layout="wide"
)

# ==========================================================
# CLEAN CSS
# ==========================================================

st.markdown("""
<style>

    /* Page */
    .stApp {
        background-color: #f8fafc;
    }

    .block-container {
        max-width: 1100px;
        padding-top: 30px;
        padding-bottom: 60px;
    }

    /* Hide Streamlit branding */
    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    header {
        visibility: hidden;
    }

    /* Headings */
    h1 {
        color: #111827 !important;
        font-weight: 700 !important;
        letter-spacing: -1px;
    }

    h2, h3 {
        color: #111827 !important;
    }

    /* Normal text */
    p {
        color: #4b5563;
    }

    /* Buttons */
    .stButton > button {
        border-radius: 10px;
        height: 45px;
        font-weight: 600;
    }

    /* Inputs */
    .stTextInput input {
        border-radius: 10px;
    }

    /* Selectbox */
    div[data-baseweb="select"] {
        border-radius: 10px;
    }

    /* Cards made only with Streamlit containers */
    .result-header {
        font-size: 26px;
        font-weight: 700;
        color: #111827;
    }

    .small-text {
        color: #6b7280;
        font-size: 14px;
    }

    /* Metrics */
    div[data-testid="stMetric"] {
        background: white;
        border: 1px solid #e5e7eb;
        padding: 18px;
        border-radius: 12px;
    }

</style>
""", unsafe_allow_html=True)


# ==========================================================
# DEMO DATA
# ==========================================================

DEMO_PAGES = {

    "Dafinitiq AI Program": {
        "url": "https://example.com/dafinitiq-ai-program",

        "content": """
Dafinitiq AI Program

Applications are open until October 15, 2026 at 11:59 PM.

Applicants should submit an AI product idea that uses open-source tools.

The submission should include:
- Product description
- Motivation for choosing the idea
- Architecture diagram
- Working MVP link

No paid AI API is required for the prototype.
"""
    },

    "University Scholarship": {
        "url": "https://example.com/university-scholarship",

        "content": """
University Scholarship

Applications close on October 20, 2026.

Students must submit:
- Latest transcript
- CNIC copy
- Proof of enrollment
- Short personal statement

The application is submitted online.
"""
    },

    "Software Engineering Internship": {
        "url": "https://example.com/software-internship",

        "content": """
Software Engineering Internship

Applications are open until October 25, 2026.

Applicants should submit:
- Updated CV
- University transcript
- GitHub profile
- Short cover letter

Candidates should have experience with Python,
Git, and basic machine learning.
"""
    }
}


# ==========================================================
# SESSION STATE
# ==========================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "result" not in st.session_state:
    st.session_state.result = None


# ==========================================================
# LOGIN
# ==========================================================

if not st.session_state.logged_in:

    st.markdown("# 🧭 Wayfind AI")

    st.markdown(
        "### Make complicated websites easier to understand and act on."
    )

    st.write("")

    col1, col2, col3 = st.columns([1, 1.2, 1])

    with col2:

        st.subheader("Welcome")

        st.caption(
            "Use the demo account to explore the prototype."
        )

        email = st.text_input(
            "Email",
            value="demo@wayfind.ai"
        )

        password = st.text_input(
            "Password",
            value="WayfindDemo123",
            type="password"
        )

        if st.button(
            "Sign in",
            type="primary",
            use_container_width=True
        ):

            if (
                email == "demo@wayfind.ai"
                and password == "WayfindDemo123"
            ):

                st.session_state.logged_in = True
                st.rerun()

            else:

                st.error("Incorrect email or password.")

        st.info(
            "Demo credentials: demo@wayfind.ai / WayfindDemo123"
        )

    st.stop()


# ==========================================================
# NAVIGATION
# ==========================================================

left, right = st.columns([5, 1])

with left:

    st.markdown(
        "# 🧭 Wayfind AI"
    )

with right:

    if st.button("Log out"):

        st.session_state.logged_in = False
        st.session_state.result = None

        st.rerun()


# ==========================================================
# MAIN INTRO
# ==========================================================

st.markdown(
    "### Turn information overload into a clear action plan."
)

st.write(
    "Give Wayfind a webpage and tell it what you're trying to accomplish. "
    "It identifies the information that matters and organizes it into "
    "requirements, documents, deadlines and next steps."
)

st.divider()


# ==========================================================
# INPUT
# ==========================================================

st.subheader("What are you trying to accomplish?")

col1, col2 = st.columns([1, 1])


with col1:

    st.markdown("**1. Choose a webpage**")

    page_name = st.selectbox(
        "Webpage",
        list(DEMO_PAGES.keys()),
        label_visibility="collapsed"
    )

    page = DEMO_PAGES[page_name]

    st.caption(
        "Source: " + page["url"]
    )


with col2:

    st.markdown("**2. Tell Wayfind your goal**")

    intent = st.text_input(
        "Goal",
        value="I want to apply. What do I need to do?",
        label_visibility="collapsed"
    )


st.write("")

if st.button(
    "🧭 Find My Way",
    type="primary",
    use_container_width=True
):

    with st.spinner(
        "Analyzing the webpage..."
    ):

        content = page["content"]
        lower = content.lower()


        # ==================================================
        # DEADLINE
        # ==================================================

        deadline = "Not detected"

        pattern = (
            r"(?:until|close[sd]? on|deadline)"
            r".{0,80}?"
            r"(January|February|March|April|May|June|July|"
            r"August|September|October|November|December)"
            r"\s+\d{1,2},\s+\d{4}"
        )

        match = re.search(
            pattern,
            content,
            re.IGNORECASE
        )

        if match:
            deadline = match.group(0)


        # ==================================================
        # DOCUMENTS
        # ==================================================

        document_map = {

            "product description":
                "Product description",

            "motivation":
                "Motivation",

            "architecture diagram":
                "Architecture diagram",

            "working mvp link":
                "Working MVP link",

            "latest transcript":
                "Latest transcript",

            "cnic copy":
                "CNIC copy",

            "proof of enrollment":
                "Proof of enrollment",

            "personal statement":
                "Personal statement",

            "updated cv":
                "Updated CV",

            "university transcript":
                "University transcript",

            "github profile":
                "GitHub profile",

            "short cover letter":
                "Short cover letter"
        }

        documents = []

        for key, value in document_map.items():

            if key in lower:
                documents.append(value)


        # ==================================================
        # REQUIREMENTS
        # ==================================================

        requirements = []

        if "open-source" in lower:
            requirements.append(
                "Use open-source tools"
            )

        if "ai product idea" in lower:
            requirements.append(
                "Submit an AI product idea"
            )

        if "python" in lower:
            requirements.append(
                "Python experience"
            )

        if "git" in lower:
            requirements.append(
                "Git experience"
            )

        if "machine learning" in lower:
            requirements.append(
                "Basic machine learning experience"
            )

        if "online" in lower:
            requirements.append(
                "Submit the application online"
            )


        # ==================================================
        # STEPS
        # ==================================================

        steps = [
            "Review the requirements",
            "Prepare the required materials",
            "Complete the application",
            "Review your submission",
            "Submit before the deadline"
        ]


        st.session_state.result = {
            "deadline": deadline,
            "documents": documents,
            "requirements": requirements,
            "steps": steps,
            "intent": intent,
            "page": page
        }


# ==========================================================
# RESULTS
# ==========================================================

if st.session_state.result:

    result = st.session_state.result
    page = result["page"]

    st.divider()

    st.markdown(
        "## 🧭 Your Wayfind plan"
    )

    st.caption(
        "Information organized around your goal."
    )

    st.write("")


    # ======================================================
    # OVERVIEW
    # ======================================================

    c1, c2, c3, c4 = st.columns(4)

    with c1:

        st.metric(
            "Deadline",
            result["deadline"]
        )

    with c2:

        st.metric(
            "Materials",
            len(result["documents"])
        )

    with c3:

        st.metric(
            "Requirements",
            len(result["requirements"])
        )

    with c4:

        st.metric(
            "Steps",
            len(result["steps"])
        )


    st.write("")


    # ======================================================
    # GOAL
    # ======================================================

    with st.container(border=True):

        st.subheader("🎯 Your goal")

        st.write(
            result["intent"]
        )


    st.write("")


    # ======================================================
    # REQUIREMENTS + DOCUMENTS
    # ======================================================

    left, right = st.columns(2)


    with left:

        with st.container(border=True):

            st.subheader("✓ Requirements")

            if result["requirements"]:

                for i, requirement in enumerate(
                    result["requirements"]
                ):

                    st.checkbox(
                        requirement,
                        key=f"req_{i}"
                    )

            else:

                st.write(
                    "No specific requirements detected."
                )


    with right:

        with st.container(border=True):

            st.subheader("📄 Documents & materials")

            if result["documents"]:

                for i, document in enumerate(
                    result["documents"]
                ):

                    st.checkbox(
                        document,
                        key=f"doc_{i}"
                    )

            else:

                st.write(
                    "No documents detected."
                )


    st.write("")


    # ======================================================
    # NEXT STEPS
    # ======================================================

    with st.container(border=True):

        st.subheader("🪜 What to do next")

        for i, step in enumerate(
            result["steps"],
            start=1
        ):

            st.write(
                f"**{i}.** {step}"
            )


    st.write("")


    # ======================================================
    # SOURCE
    # ======================================================

    with st.expander("🔎 View source evidence"):

        st.caption(
            "Source: " + page["url"]
        )

        st.write(
            page["content"].strip()
        )


    st.success(
        "Wayfind has converted the information into an actionable plan."
    )


else:

    # ======================================================
    # EMPTY STATE
    # ======================================================

    st.write("")

    st.subheader("How Wayfind works")

    c1, c2, c3 = st.columns(3)

    with c1:

        with st.container(border=True):

            st.markdown("### 01")

            st.markdown("**Understand**")

            st.write(
                "Identify the information relevant "
                "to what you're trying to accomplish."
            )


    with c2:

        with st.container(border=True):

            st.markdown("### 02")

            st.markdown("**Filter**")

            st.write(
                "Separate important requirements, "
                "documents and deadlines from everything else."
            )


    with c3:

        with st.container(border=True):

            st.markdown("### 03")

            st.markdown("**Act**")

            st.write(
                "Turn the information into a simple "
                "step-by-step plan."
            )


# ==========================================================
# FOOTER
# ==========================================================

st.divider()

st.caption(
    "🧭 Wayfind AI · Open-source-first MVP"
)