from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
import os
from src.langchain.prompt_templates import get_summary_prompt_template
from src.data.linkedin_scraper import fetch_linkedin_profile_and_clean_and_summarize
from src.tools.linkedin_tools import linkedin_tool  # Import LinkedIn tool for fetching LinkedIn URL
from src.langchain.output_parser import summary_parser  # Import the output parser

# Load environment variables from a .env file
load_dotenv()

# Get OpenAI API key from environment
openai_api_key = os.getenv("OPENAI_API_KEY")

if not openai_api_key:
    raise ValueError("OPENAI_API_KEY not found in environment variables.")


def fetch_linkedin_url(name: str) -> str:
    """
    Fetch the LinkedIn profile URL for a given name using the Tavily-powered search tool.
    """
    linkedin_url = linkedin_tool.func(name)  # Call the tool function to get the LinkedIn URL
    if linkedin_url == "No LinkedIn URL found":
        raise ValueError(f"Could not find a LinkedIn profile for {name}")
    return linkedin_url


def summarize_profile(name: str):
    """
    Fetches LinkedIn URL using the tool, scrapes and cleans the profile, and then summarizes the data.
    Returns an array with [summary, interesting_facts].
    """
    # Fetch the LinkedIn profile URL
    linkedin_url = fetch_linkedin_url(name)

    print(f"LinkedIn URL: {linkedin_url}")

    # Fetch and clean the LinkedIn profile data
    linkedin_data = fetch_linkedin_profile_and_clean_and_summarize(linkedin_url, True)

    # Initialize the OpenAI language model
    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo", openai_api_key=openai_api_key)

    # Get the summary prompt template
    summary_prompt_template = get_summary_prompt_template()

    # Invoke the chain with the cleaned LinkedIn profile data
    chain = summary_prompt_template | llm | summary_parser
    res = chain.invoke(input={"information": linkedin_data})

    # Parse the result to return separate summary and facts
    summary_result = res['summary']
    interesting_facts = res['interesting_facts']

    # If interesting_facts is returned as a single string, split it by periods
    if isinstance(interesting_facts, str):
        # Attempt to split on common sentence delimiters
        interesting_facts = interesting_facts.split('. ')

    # Ensure there are exactly two interesting facts, limit to the first two if there are more
    interesting_facts = [fact.strip() for fact in interesting_facts if len(fact.strip()) > 0]

    if len(interesting_facts) > 2:
        interesting_facts = interesting_facts[:2]
    elif len(interesting_facts) < 2:
        raise ValueError(f"Expected 2 interesting facts, but found {len(interesting_facts)}")

    # Return the summary and the interesting facts
    return summary_result, interesting_facts


if __name__ == "__main__":
    # Example usage: input a person's name
    person_name = "Mohamed Ahmed Elbeskeri, PhD"  # You can replace this with any name you want to summarize

    try:
        summary, facts = summarize_profile(person_name)
        print("Summary:", summary)

        # Print each interesting fact
        print("Interesting Fact 1:", facts[0])
        print("Interesting Fact 2:", facts[1])

    except ValueError as e:
        print(f"Error: {e}")
