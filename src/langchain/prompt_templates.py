from langchain_core.prompts import PromptTemplate
from src.langchain.output_parser import summary_parser

def get_summary_prompt_template() -> PromptTemplate:
    """
    Returns a summary prompt template with partial variables and format instructions.
    """
    # Define the template with format instructions
    summary_template = """
    You are an assistant that generates professional summaries of LinkedIn profiles. 
    Given the following information about a person: {information}, create:

    1. A concise summary of their professional background.
    2. Two interesting facts about them, focusing on their skills or unique achievements in bullet points.

    The summary should be well-structured, clear, and informative.

    {format_instructions}
    """

    # Create the prompt template with partial variables
    prompt_template = PromptTemplate(
        input_variables=["information"],  # Only the "information" part will be dynamic
        template=summary_template,
        partial_variables={
            "format_instructions": summary_parser.get_format_instructions(only_json=True)
        }
    )

    return prompt_template
