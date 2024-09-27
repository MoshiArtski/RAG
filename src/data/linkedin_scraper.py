import os
import requests
import json
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Get Proxycurl API key from environment
proxycurl_api_key = os.getenv("PROXYCURL_API_KEY")

if not proxycurl_api_key:
    raise ValueError("PROXYCURL_API_KEY not found in environment variables.")

# Base URL for Proxycurl API
base_url = "https://nubela.co/proxycurl/api/v2/linkedin"


def fetch_linkedin_profile(linkedin_url: str, use_mock: bool = False):
    """
    Fetches LinkedIn profile data using Proxycurl API or loads from mock data if specified.

    Args:
        linkedin_url (str): The LinkedIn profile URL.
        use_mock (bool): If True, load data from mock.json instead of calling the API.

    Returns:
        dict: The JSON response containing profile information, either from Proxycurl API or mock data.
    """
    if use_mock:
        # Path to mock data
        mock_file_path = os.path.join('mock_linkedin_data.json')

        # Check if the mock file exists
        if os.path.exists(mock_file_path):
            with open(mock_file_path, 'r') as mock_file:
                mock_data = json.load(mock_file)
            print("Using mock data from mock.json.")
            return mock_data
        else:
            raise FileNotFoundError(f"Mock file not found at {mock_file_path}")

    # Make an API call to Proxycurl
    headers = {
        'Authorization': f'Bearer {proxycurl_api_key}',
    }

    params = {
        'url': linkedin_url
    }

    response = requests.get(base_url, headers=headers, params=params)

    # Check if the response is successful
    if response.status_code == 200:
        return response.json()
    else:
        # Handle errors
        raise Exception(f"Failed to fetch profile data. Status Code: {response.status_code}, Message: {response.text}")


def clean_profile_data(profile_data: dict):
    """
    Cleans and filters LinkedIn profile data to make it more suitable for generating summaries.
    Focuses on key elements: name, occupation, location, latest position, education, skills,
    accomplishments, birth date, gender, and industry. Removes any fields that are None or empty.

    Args:
        profile_data (dict): The LinkedIn profile data.

    Returns:
        dict: Cleaned and structured profile data for generating a summary.
    """
    # Extracting relevant fields, while filtering out None or empty values
    full_name = profile_data.get('full_name', 'N/A')
    occupation = profile_data.get('occupation', 'N/A')

    # Extract location details
    city = profile_data.get('city', 'N/A')
    state = profile_data.get('state', 'N/A')
    country = profile_data.get('country_full_name', 'N/A')

    # Extract latest experience (job)
    experiences = profile_data.get('experiences', [])
    latest_experience = experiences[0] if experiences else {}
    latest_job_title = latest_experience.get('title', 'N/A')
    latest_company = latest_experience.get('company', 'N/A')
    job_description = latest_experience.get('description', 'N/A')

    # Extract latest education (degree)
    education = profile_data.get('education', [])
    latest_education = education[0] if education else {}
    degree = latest_education.get('degree_name', 'N/A')
    institution = latest_education.get('school', 'N/A')

    # Extract skills (if available)
    skills = profile_data.get('skills', [])
    skills = ', '.join(skills) if skills else 'No skills provided.'

    # Extract languages spoken
    languages = profile_data.get('languages', [])
    languages = ', '.join(languages) if languages else 'No languages provided.'

    # Extract birth date, gender, and industry
    birth_date = profile_data.get('birth_date', 'N/A')
    gender = profile_data.get('gender', 'N/A')
    industry = profile_data.get('industry', 'N/A')

    # Extract accomplishments (if any)
    accomplishments = {
        "honors_awards": profile_data.get("accomplishment_honors_awards", []),
        "publications": profile_data.get("accomplishment_publications", []),
        "patents": profile_data.get("accomplishment_patents", []),
        "projects": profile_data.get("accomplishment_projects", []),
    }

    # Return cleaned data as a dictionary, filtering out None or empty fields
    cleaned_data = {
        "full_name": full_name,
        "occupation": occupation,
        "location": f"{city}, {state}, {country}" if city != "N/A" else None,
        "latest_job_title": latest_job_title if latest_job_title != 'N/A' else None,
        "latest_company": latest_company if latest_company != 'N/A' else None,
        "job_description": job_description if job_description != 'N/A' else None,
        "degree": degree if degree != 'N/A' else None,
        "institution": institution if institution != 'N/A' else None,
        "skills": skills if skills != 'No skills provided.' else None,
        "languages": languages if languages != 'No languages provided.' else None,
        "birth_date": birth_date if birth_date != 'N/A' else None,
        "gender": gender if gender != 'N/A' else None,
        "industry": industry if industry != 'N/A' else None,
        "accomplishments": {k: v for k, v in accomplishments.items() if v}
    }

    # Filter out None or empty values from the cleaned data
    return {k: v for k, v in cleaned_data.items() if v}


def summarize_profile(cleaned_data: dict):
    """
    Summarizes the cleaned LinkedIn profile data into a brief, human-readable format.

    Args:
        cleaned_data (dict): The cleaned LinkedIn profile data.

    Returns:
        str: A summarized profile description.
    """
    # Extract fields safely, providing default values where needed
    full_name = cleaned_data.get("full_name", None)
    occupation = cleaned_data.get("occupation", None)
    location = cleaned_data.get("location", None)
    latest_job_title = cleaned_data.get("latest_job_title", None)
    latest_company = cleaned_data.get("latest_company", None)
    degree = cleaned_data.get("degree", None)
    institution = cleaned_data.get("institution", None)
    skills = cleaned_data.get("skills", None)
    languages = cleaned_data.get("languages", None)
    birth_date = cleaned_data.get("birth_date", None)
    gender = cleaned_data.get("gender", None)
    industry = cleaned_data.get("industry", None)

    # Ensure accomplishments is always a dictionary to avoid NoneType errors
    accomplishments = cleaned_data.get("accomplishments", {})

    # Start building the summary
    summary = ""

    # Add only fields that are not None or empty
    if full_name:
        summary += f"{full_name} is currently working"
        if latest_job_title and latest_company:
            summary += f" as a {latest_job_title} at {latest_company}."
        summary += "\n"

    if location:
        summary += f"They are based in {location}.\n"

    if degree and institution:
        summary += f"They hold a {degree} from {institution}.\n"

    if skills:
        summary += f"Their key skills include {skills}.\n"

    if languages:
        summary += f"They are fluent in {languages}.\n"

    if birth_date and gender and industry:
        summary += f"Born on {birth_date}, {gender}, {full_name} works in the {industry} industry.\n"

    # Add accomplishments (if any), only if they exist and are not empty
    if accomplishments.get("honors_awards"):
        summary += f"\nAccomplishments - Honors and Awards: {len(accomplishments['honors_awards'])} listed."
    if accomplishments.get("publications"):
        summary += f"\nPublications: {len(accomplishments['publications'])} listed."
    if accomplishments.get("patents"):
        summary += f"\nPatents: {len(accomplishments['patents'])} listed."
    if accomplishments.get("projects"):
        summary += f"\nProjects: {len(accomplishments['projects'])} listed."

    # Return the generated summary, stripping any extra spaces
    return summary.strip() if summary else "No relevant information available."


def fetch_linkedin_profile_and_clean(linkedin_url: str, use_mock: bool = False):
    """
    Fetches LinkedIn profile data, cleans it by removing unnecessary fields, and returns the cleaned data.

    Args:
        linkedin_url (str): The LinkedIn profile URL.
        use_mock (bool): If True, load data from mock.json instead of calling the API.

    Returns:
        dict: Cleaned LinkedIn profile data.
    """
    profile_data = fetch_linkedin_profile(linkedin_url, use_mock=use_mock)
    return clean_profile_data(profile_data)


def fetch_linkedin_profile_and_clean_and_summarize(linkedin_url: str, use_mock: bool = False):
    """
    Fetches LinkedIn profile data, cleans it by removing unnecessary fields, and returns a summary.

    Args:
        linkedin_url (str): The LinkedIn profile URL.
        use_mock (bool): If True, load data from mock.json instead of calling the API.

    Returns:
        str: A summarized LinkedIn profile.
    """
    cleaned_data = fetch_linkedin_profile_and_clean(linkedin_url, use_mock=use_mock)
    return summarize_profile(cleaned_data)


if __name__ == "__main__":
    # Example LinkedIn profile URL
    linkedin_url = "https://www.linkedin.com/in/some-profile/"

    # Set `use_mock` to True to use mock data instead of the live API call
    use_mock = True

    # Fetch, clean, and summarize profile data
    summary = fetch_linkedin_profile_and_clean_and_summarize(linkedin_url, use_mock=use_mock)
    print("Profile Summary:")
    print(summary)
