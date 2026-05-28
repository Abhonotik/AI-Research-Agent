import streamlit as st

from app.orchestrator import run_research_agent


st.set_page_config(
    page_title="AI Research Agent",
    page_icon="🔎",
    layout="wide"
)

st.title("🔎 AI Research Agent")

st.write(
    "Generate structured research using "
    "planning, retrieval, validation, "
    "and synthesis."
)

query = st.text_area(
    "Enter your research query",
    placeholder="Example: Compare top vector databases for RAG"
)

if st.button("Generate Research"):

    if not query.strip():

        st.warning("Please enter a query.")

    else:

        with st.spinner("Researching..."):

            try:

                response = run_research_agent(query)

                if not response:
                    st.error("Research failed.")
                    st.stop()

                data = response.model_dump()

                st.success("Research completed!")

                st.subheader("Short Answer")
                st.write(data.get("short_answer"))

                st.subheader("Key Findings")

                for finding in data.get(
                    "key_findings", []
                ):
                    st.write(f"• {finding}")

                st.subheader("Confidence")
                st.info(data.get("confidence"))

                st.subheader("Limitations")

                for limitation in data.get(
                    "limitations", []
                ):
                    st.write(f"• {limitation}")

                st.subheader(
                    "Suggested Next Steps"
                )

                for step in data.get(
                    "suggested_next_steps", []
                ):
                    st.write(f"• {step}")

                st.subheader("Sources Used")

                for source in data.get(
                    "sources_used", []
                ):
                    st.write(source)

            except Exception as e:

                st.error(
                    f"Something went wrong: {e}"
                )