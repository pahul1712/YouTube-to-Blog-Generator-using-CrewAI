from crewai import Agent
from tools import yt_tool
import os
from dotenv import load_dotenv
load_dotenv()

os.environ["OPENAI_API_KEY"] =  os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_MODEL_NAME"] = "gpt-5.1"


## Create a Senior Blog Content Researcher:

blog_researcher = Agent(
    role="Blog Researcher from youtube Videos",
    goal="Get the relevant video content for the topic {topic} from the Youtube channels",
    verbose=True,
    memory=True,
    backstory=(
        "An expert researcher who specializes in analyzing YouTube channel content."
    ),
    tools=[yt_tool],
    allow_delegation=True
)



## Creating a Senior Blog Writer Agent with YT Tool:

blog_writer = Agent(
    role="Writer",
    goal="Narrate complelling tech stories about the video {topic} from Youtube channels",
    verbose=True,
    memory=True,
    backstory=(
        "With a flair for simplyfying complex topics, you craft"
        "engaging narratives that captivate and educate, bringing new"
        "discoveries to light in an accessible manner."
    ),
    tools=[yt_tool],
    allow_delegation=False
)