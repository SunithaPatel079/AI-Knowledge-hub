import streamlit as st

from database import (
    create_tables,
    add_user,
    get_user,
    add_knowledge,
    get_all_knowledge,
    search_knowledge
)

from ai_service import ask_ai


# -----------------------------
# PAGE CONFIGURATION
# -----------------------------

st.set_page_config(
    page_title="AI Knowledge Transfer System",
    page_icon="🤖",
    layout="wide"
)


# -----------------------------
# CREATE DATABASE TABLES
# -----------------------------

create_tables()


# -----------------------------
# SESSION STATE
# -----------------------------

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user_id" not in st.session_state:
    st.session_state.user_id = None

if "user_name" not in st.session_state:
    st.session_state.user_name = None


# -----------------------------
# LOGIN / REGISTER
# -----------------------------

if not st.session_state.logged_in:

    st.title("🤖 AI Knowledge Transfer System")
    st.write("Share company knowledge and ask AI questions.")

    option = st.radio(
        "Choose an option",
        ["Login", "Register"]
    )

    # -------------------------
    # REGISTER
    # -------------------------

    if option == "Register":

        st.subheader("Create Account")

        name = st.text_input("Name")
        email = st.text_input("Email")
        password = st.text_input(
            "Password",
            type="password"
        )

        if st.button("Register"):

            if not name or not email or not password:
                st.warning("Please fill all fields.")

            else:

                try:

                    add_user(
                        name,
                        email,
                        password
                    )

                    st.success(
                        "Registration successful! "
                        "Now login."
                    )

                except Exception:

                    st.error(
                        "Email already registered."
                    )

    # -------------------------
    # LOGIN
    # -------------------------

    else:

        st.subheader("Login")

        email = st.text_input("Email")
        password = st.text_input(
            "Password",
            type="password"
        )

        if st.button("Login"):

            user = get_user(
                email,
                password
            )

            if user:

                st.session_state.logged_in = True
                st.session_state.user_id = user["id"]
                st.session_state.user_name = user["name"]

                st.success("Login successful!")

                st.rerun()

            else:

                st.error(
                    "Invalid email or password."
                )


# -----------------------------
# MAIN APPLICATION
# -----------------------------

else:

    st.sidebar.title("🤖 AI Knowledge System")

    st.sidebar.write(
        f"Welcome, {st.session_state.user_name}"
    )

    page = st.sidebar.radio(
        "Menu",
        [
            "Dashboard",
            "Add Knowledge",
            "Ask AI",
            "Search Knowledge",
            "Logout"
        ]
    )


    # -------------------------
    # DASHBOARD
    # -------------------------

    if page == "Dashboard":

        st.title("📚 Company Knowledge")

        knowledge = get_all_knowledge()

        if knowledge:

            for item in knowledge:

                with st.expander(
                    item["title"]
                ):

                    st.write(
                        f"**Category:** "
                        f"{item['category']}"
                    )

                    st.write(
                        item["content"]
                    )

                    st.caption(
                        f"Author: {item['author']}"
                    )

        else:

            st.info(
                "No company knowledge available yet."
            )


    # -------------------------
    # ADD KNOWLEDGE
    # -------------------------

    elif page == "Add Knowledge":

        st.title("➕ Add Company Knowledge")

        title = st.text_input(
            "Knowledge Title"
        )

        category = st.text_input(
            "Category"
        )

        content = st.text_area(
            "Knowledge Content",
            height=250
        )

        if st.button("Save Knowledge"):

            if not title or not category or not content:

                st.warning(
                    "Please fill all fields."
                )

            else:

                add_knowledge(
                    title,
                    category,
                    content,
                    st.session_state.user_name
                )

                st.success(
                    "Knowledge added successfully!"
                )


    # -------------------------
    # ASK AI
    # -------------------------

    elif page == "Ask AI":

        st.title("🤖 Ask AI")

        question = st.text_area(
            "Ask something about the company knowledge"
        )

        if st.button("Ask AI"):

            if not question:

                st.warning(
                    "Please enter a question."
                )

            else:

                knowledge = get_all_knowledge()

                knowledge_text = ""

                for item in knowledge:

                    knowledge_text += f"""
Title: {item["title"]}
Category: {item["category"]}
Content: {item["content"]}
Author: {item["author"]}

"""

                if knowledge_text:

                    with st.spinner(
                        "AI is thinking..."
                    ):

                        answer = ask_ai(
                            question,
                            knowledge_text
                        )

                    st.subheader(
                        "AI Answer"
                    )

                    st.write(answer)

                else:

                    st.info(
                        "There is no company knowledge available yet."
                    )


    # -------------------------
    # SEARCH
    # -------------------------

    elif page == "Search Knowledge":

        st.title("🔎 Search Knowledge")

        keyword = st.text_input(
            "Enter keyword"
        )

        if st.button("Search"):

            results = search_knowledge(
                keyword
            )

            if results:

                for item in results:

                    with st.expander(
                        item["title"]
                    ):

                        st.write(
                            f"**Category:** "
                            f"{item['category']}"
                        )

                        st.write(
                            item["content"]
                        )

                        st.caption(
                            f"Author: {item['author']}"
                        )

            else:

                st.info(
                    "No matching knowledge found."
                )


    # -------------------------
    # LOGOUT
    # -------------------------

    elif page == "Logout":

        st.session_state.logged_in = False
        st.session_state.user_id = None
        st.session_state.user_name = None

        st.success("Logged out.")

        st.rerun()