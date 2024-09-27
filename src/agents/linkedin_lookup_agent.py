import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.agents import create_react_agent, AgentExecutor
from langchain import hub
from langchain.memory import SimpleMemory
from langchain_core.prompts import PromptTemplate
from langchain_core.callbacks import BaseCallbackHandler
from src.tools.linkedin_tools import linkedin_tool  # Import the Tavily-powered tool

# Load environment variables from a .env file
load_dotenv()

# Get OpenAI API key from environment
openai_api_key = os.getenv("OPENAI_API_KEY")

if not openai_api_key:
    raise ValueError("OPENAI_API_KEY not found in environment variables.")


class PrintCallbackHandler(BaseCallbackHandler):
    """Custom callback to print each event."""

    def on_chain_start(self, run_id, inputs, **kwargs):
        print(f"Agent started with inputs: {inputs}")

    def on_chain_end(self, run_id, outputs, **kwargs):
        print(f"Agent finished with outputs: {outputs}")

    def on_chain_error(self, run_id, error, **kwargs):
        print(f"Error occurred: {error}")


def lookup(name: str) -> str:
    """
    Function that constructs a prompt to get the LinkedIn URL of a person given their full name,
    using the Tavily-powered search tool.
    """
    # Initialize OpenAI LLM
    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo", openai_api_key=openai_api_key)

    # Load the React agent prompt
    react_prompt = hub.pull("hwchase17/react")

    # Create the agent using tools and LLM
    agent = create_react_agent(llm=llm, tools=[linkedin_tool], prompt=react_prompt)

    # Setup memory for the agent
    memory = SimpleMemory()

    # Define callback handlers for logging and error handling
    callbacks = [PrintCallbackHandler()]

    # Create the PromptTemplate to dynamically generate the input prompt
    agent_input_template = PromptTemplate(
        template="Find the LinkedIn profile URL for {name_of_person}, using Tavily search.",
        input_variables=["name_of_person"]
    )

    # Prepare the input for the agent using the PromptTemplate
    input_for_agent = {
        "input": agent_input_template.format(name_of_person=name)
    }

    # Create the AgentExecutor with configurations
    agent_executor = AgentExecutor(
        agent=agent,
        tools=[linkedin_tool],  # Use the Tavily-powered LinkedIn search tool
        memory=memory,
        verbose=True,
        max_iterations=10,
        max_execution_time=30,
        return_intermediate_steps=True
    )

    # Execute the agent using `invoke`
    result = agent_executor.invoke(input_for_agent, callbacks=callbacks)

    # Return only the output URL from the result
    linkedin_url = result.get("output", "No LinkedIn URL found")
    return linkedin_url


if __name__ == "__main__":
    # Example usage
    name = "Eden Marco"
    linkedin_url = lookup(name)
    print(f"LinkedIn URL for {name}: {linkedin_url}")
