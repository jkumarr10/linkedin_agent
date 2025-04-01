# Linkedin Content Generator & Poster Agent

A simple but powerful AI-driven application that generates LinkedIn content and posts it directly to your profile with your approval.

## Overview
This application combines OpenAI's Agents SDK with LinkedIn's API to:

• Generate professional, engaging LinkedIn content tailored to your specifications

• Present the content for your review and approval

• Post approved content directly to your LinkedIn profile

The system uses a framework with involving a set of specialized agents each responsible for handling a specific task involving content generation and posting.

## Acknowledgments
• Built with OpenAI's GPT model (gpt-4o-mini)

• Uses the LinkedIn API for posting functionality

• Streamlit for the user interface

## Setup and Installation

### Prerequisites

• Python 3.10+

• LinkedIn Developer Account with API access

• OpenAI API key


### Environment Variables
Create a .env file with the following variables:

```
OPENAI_API_KEY = your_openai_api_key
LINKEDIN_ACCESS_TOKEN = your_linkedin_access_token
LINKEDIN_AUTHOR=your_linkedin_person_id

```

### Installation

1. Clone the Repository:

```
git clone https://github.com/yourusername/linkedin_agent.git
cd linkedin_agent

```

2. Install dependencies:

```
poetry install

```

3. Run the application:

```
streamlit run app_openai/main.py

```

### Usage

1. Start the application

2. Enter your content request in the chat interface (e.g., "Create a post about the latest developments in LLMs")

3. Review the generated content

4. If you all is good, just approve the post and ask the agent to post the content to LinkedIn, or provide feedback for revisions if required. 

### Notes
• Your LinkedIn access token and author id grants posting permissions to your profile

• Your OpenAI API key allows you to call the OpenAI models

• Store credentials securely and never commit them to version control

