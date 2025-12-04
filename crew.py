from crewai import Crew,Process
from agents import blog_researcher,blog_writer
from tasks import research_task,write_task
import streamlit as st


# Streamlit Blog Generation App:

# page configuration
st.set_page_config(
    page_title="YouTube → Blog Generator (CrewAI)",
    page_icon="📝",
    layout="wide",
)


# Simple custom styling
st.markdown(
    """
    <style>
    /* Global font + background tweak */
    body {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    }
    .main {
        background-color: #050816;
    }
    /* Center main container a bit */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1100px;
    }
    /* Card style for output */
    .blog-card {
        background: #064420;
        color: #f1f5f9;
        padding: 1.5rem 1.8rem;
        border-radius: 12px;
        border: 1px solid #22c55e33;
        box-shadow: 0 18px 30px rgba(0,0,0,0.45);
        font-size: 0.98rem;
        line-height: 1.6;
        white-space: pre-wrap;
    }
    .blog-title {
        font-weight: 700;
        font-size: 1.1rem;
        margin-bottom: 0.4rem;
        color: #bbf7d0;
    }
    .subtext {
        font-size: 0.88rem;
        color: #cbd5f5;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# Create and run the crew
crew = Crew(
    agents=[blog_researcher,blog_writer],
    tasks=[research_task,write_task],
    process=Process.sequential, # default sequential task
    memory=True,
    cache=True,
    max_rpm=100,
    share_crew=True
)


# UI Layout
st.title("📝 Blog Generation using CrewAI")
st.write(
    "Turn any **YouTube video** into a structured, long-form blog post powered by "
    "**CrewAI agents + YouTubeChannelSearchTool**."
)

st.markdown("---")


left, right = st.columns([1.3, 1])

with left:
    st.subheader("1️⃣ Enter the video / topic")

    video_query = st.text_input(
        "Name of the YouTube video (or topic) you want the blog for",
        placeholder="e.g. LangChain Krish Naik Hindi",
    )

    st.caption(
        "Tip: For best results, paste the **exact video title** or a "
        "very specific topic that clearly matches a video on the channel."
    )

    generate_button = st.button("🚀 Generate Blog", type="primary", use_container_width=True)

with right:
    st.subheader("ℹ️ How this works")
    st.markdown(
        """
        - Uses a **Crew** of two agents:
          - *Blog Researcher* → finds & analyzes the YouTube video  
          - *Blog Writer* → turns the research into a polished blog  
        - Behind the scenes it uses:
          - `YoutubeChannelSearchTool` to search the channel  
          - Sequential process: research → writing  
        - Output is a **long, detailed blog** ready for:
          - LinkedIn posts  
          - Medium articles  
          - Personal blogs / notes  
        """
    )

    st.markdown(
        "<span class='subtext'>Note: This is an experimental demo. "
        "Always skim the result against the real video if accuracy is critical.</span>",
        unsafe_allow_html=True,
    )

st.markdown("---")


# Run Crew on button click
if generate_button:
    if not video_query.strip():
        st.warning("Please enter a video title or topic before generating.")
    else:
        with st.spinner("🔍 Asking the Crew to research and write your blog..."):
            try:
                result = crew.kickoff(inputs={"topic": video_query.strip()})
                blog_text = str(result)

                # Optional: simple heuristic to split out a title (first line) from body
                # If you already return a structured dict, adapt this accordingly.
                lines = blog_text.splitlines()
                if lines:
                    inferred_title = lines[0].strip().strip("# ").strip()
                    body = "\n".join(lines[1:]).strip()
                else:
                    inferred_title = f"Blog for: {video_query.strip()}"
                    body = blog_text

                st.subheader("2️⃣ Generated Blog")

                st.markdown(
                    f"""
                    <div class="blog-card">
                        <div class="blog-title">
                            {inferred_title if inferred_title else f"Blog for: {video_query.strip()}"}
                        </div>
                        <div class="blog-body">
                            {body.replace("\n", "<br>")}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                # Download button so you can save the blog as a .txt file
                st.download_button(
                    label="📥 Download Blog as .txt",
                    data=blog_text,
                    file_name=f"blog_{video_query.strip().replace(' ', '_')}.txt",
                    mime="text/plain",
                    use_container_width=True,
                )

            except Exception as e:
                st.error("Something went wrong while generating the blog.")
                st.exception(e)

else:
    st.info("👆 Enter a YouTube video name/topic and click **Generate Blog** to get started.")