from langchain_core.prompts import PromptTemplate
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.tools import Tool
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Assume Tavily API key is stored in .env file
tavily_api_key = os.getenv("TAVILY_API_KEY")
if not tavily_api_key:
    raise ValueError("TAVILY_API_KEY not found in environment variables.")

# Define the prompt template for Tavily search
linkedin_prompt_template = PromptTemplate(
    template="Given the name {name_of_person}, find their LinkedIn profile URL using Tavily. Return only the URL.",
    input_variables=["name_of_person"]
)

# Define the Tavily search tool using LangChain's Tavily integration
def linkedin_tool_func(name_of_person: str) -> str:
    """
    Function that uses the TavilySearchResults tool to search for LinkedIn URLs based on the name.
    """
    prompt = linkedin_prompt_template.format(name_of_person=name_of_person)

    # Use the TavilySearchResults tool to search for LinkedIn profiles
    search_tool = TavilySearchResults(api_key=tavily_api_key)
    result = search_tool.run(name_of_person)  # Assuming TavilySearchResults has a `run` method

    # Extract and return the first LinkedIn URL from the results (if available)
    linkedin_url = result[0]["url"] if result else "No LinkedIn URL found"
    return linkedin_url

# Create a Tool object for Tavily-based LinkedIn search
linkedin_tool = Tool(
    name="Tavily LinkedIn Profile Search",
    func=linkedin_tool_func,
    description="Uses TavilySearchResults to search for the LinkedIn profile URL based on a person's name."
)
