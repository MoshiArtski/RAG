import requests
import os
import json

# API details
api_key = 'B-XM7F4YN9-eNrXp-mcMpg'
headers = {'Authorization': 'Bearer ' + api_key}
api_endpoint = 'https://nubela.co/proxycurl/api/v2/linkedin'

# Parameters for the API call
params = {
    'linkedin_profile_url': 'https://www.linkedin.com/in/mohamed-ahmed-elbeskeri-phd-64a52b104/',
    'extra': 'include',
    'github_profile_id': 'include',
    'facebook_profile_id': 'include',
    'twitter_profile_id': 'include',
    'personal_contact_number': 'include',
    'personal_email': 'include',
    'inferred_salary': 'include',
    'skills': 'include',
    'use_cache': 'if-present',
    'fallback_to_cache': 'on-error',
}

# Make the request to Proxycurl API
response = requests.get(api_endpoint, params=params, headers=headers)

# Check if the response is successful
if response.status_code == 200:
    profile_data = response.json()

    # Define the path to the directory and the output file
    directory = os.path.join('src', 'data')
    output_path = os.path.join(directory, 'mock_linkedin_data.json')

    # Ensure the directory exists, if not, create it
    os.makedirs(directory, exist_ok=True)

    # Save the data to a JSON file
    with open(output_path, 'w') as outfile:
        json.dump(profile_data, outfile, indent=4)

    print(f"Data successfully saved to {output_path}")
else:
    # Handle errors
    print(f"Failed to fetch data. Status Code: {response.status_code}, Message: {response.text}")
