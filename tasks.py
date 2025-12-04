from crewai import Task
from tools import yt_tool
from agents import blog_researcher,blog_writer


# Research Task
research_task = Task(
    description=(
        "Using the YouTubeChannelSearchTool, identify a YouTube video about {topic}."
        "from the configured YouTube channel and extract its key points, structure, and message."

    ),
    expected_output=(
    "A comprehensive 3-paragraph report based on the video content about {topic}, "
    "including: introduction, main explanation, and key takeaways."
    ),
    tools=[yt_tool],
    agent=blog_researcher,
)

# Writing task with language model configuration
write_task = Task(
    description=(
        "Using the research from the previous task and the YouTubeChannelSearchTool, "
        "write a clear, engaging blog post about {topic} as if summarizing that YouTube video."
    ),
    expected_output=(
        "A polished blog article (6–10 paragraphs) about {topic}, written for beginners, "
        "with a logical flow: hook, explanation, examples, and conclusion."
    ),
    tools=[yt_tool],
    agent=blog_writer,
    async_execution=False,
    output_file="new-blog-post.md" 
)