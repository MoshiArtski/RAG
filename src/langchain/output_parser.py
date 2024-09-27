from langchain.output_parsers import StructuredOutputParser, ResponseSchema
from pydantic import BaseModel, Field
from typing import List, Any

# Define the output schema for parsing the summary response
class LinkedInSummary(BaseModel):
    summary: str = Field(description="A brief summary of the person's profile")
    interesting_facts: List[str] = Field(description="Two interesting facts about the person")

    def to_array(self) -> List[Any]:
        return [self.summary, self.interesting_facts]

# Define the output parser using the schema
def get_linkedin_summary_output_parser():
    # Create a list of response schemas
    response_schemas = [
        ResponseSchema(name="summary", description="A brief summary of the person's profile"),
        ResponseSchema(name="interesting_facts", description="Two interesting facts about the person")
    ]

    # Return the StructuredOutputParser with response schemas
    return StructuredOutputParser.from_response_schemas(response_schemas)


# Create the parser instance using the proper method
summary_parser = get_linkedin_summary_output_parser()
