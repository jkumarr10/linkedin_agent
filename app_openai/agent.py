
import os
from dotenv import load_dotenv
from agents import Agent, Runner, function_tool

from linkedin_tools import Linkedin

# Load environment variables
load_dotenv()

# Initialize Linkedin Class
linkedin = Linkedin()

# Get Linkedin Access Token and Author ID from environment variables
access_token = os.getenv("LINKEDIN_ACCESS_TOKEN")
linkedin_author = os.getenv("LINKEDIN_AUTHOR")


@function_tool
def linkedin_poster_tool(generated_content: str):
    """
    This function posts content to LinkedIn.

    Args:
        text (str): The content to post.
        visibility (str, optional): The visibility of the post. Defaults to "CONNECTIONS".
    """
    
    result_successful = linkedin.post_to_linkedin(generated_content=generated_content)
    
    return result_successful

# Defing Linkedin Poster Agent
def linkedin_poster_agent():
    linkedin_poster_agent = Agent(
        name="linkedin_poster",
        instructions="You are a LinkedIn poster agent. You just take whatever you get and just post it to linkedin. If you are invoked, just post the content to Linkedin.",
        tools=[linkedin_poster_tool],
        model="gpt-4o-mini",
    )

    return linkedin_poster_agent

# Define Content Generation Agent
def content_generator():
    with open("prompts/content_generation_prompt.txt") as f:
        content_generation_prompt = f.read()
        
    content_generation_agent = Agent(
        name="content_generator",
        instructions=content_generation_prompt,
        model="gpt-4o-mini",
    )
    
    return content_generation_agent

# Define Orchestration Agent
def orchestrator():
    
    # Initialize agents
    linkedin_poster_variable = linkedin_poster_agent()
    content_generator_variable = content_generator()
    
    orchestration_agent = Agent(
        name="orchestrator",
        instructions="""You are an intelligent LinkedIn content orchestrator. Your responsibilities:

        1. CONTENT GENERATION: When a user requests LinkedIn content, use the content_generator tool to create professional, engaging posts.
        2. USER APPROVAL: Present the generated content to the user with a clear request for approval. For example: "Here's the LinkedIn post I've created. Would you like me to publish this to your LinkedIn profile?" If the user rejects it you will go back to content generator tool and refine or create new content based on the user's input.
        3. POSTING: Only use the linkedin_poster tool after receiving explicit user approval. The user must use the word "Approved" only then will you route to the posting agent.
        4. CLARITY: For non-LinkedIn content requests, politely explain that you're specialized in LinkedIn content management.

        Always maintain a professional, helpful tone and prioritize user satisfaction with the content before posting.
        """,
        model="gpt-4o-mini",
        tools=[
            linkedin_poster_variable.as_tool(
                tool_name="linkedin_poster",
                tool_description="This tool is used to post content to LinkedIn.",
            ),
            content_generator_variable.as_tool(
                tool_name="content_generator",
                tool_description="This tool  is used to generate LinkedIn content.",
            )
        ]
    )
    
    return orchestration_agent


if __name__ == "__main__":
    orchestrator_variable = orchestrator()
    
    print("LinkedIn Content Assistant (type 'exit' to quit)")
    print("------------------------------------------------")
    
    # Initialize conversation history as a string
    conversation_history = ""
    
    while True:
        # Get User Input
        user_input = input("\nYou: ")
        
        # Check if user wants to exit
        if user_input.lower() in ["exit", "quit", "bye"]:
            print("\nThank you for using LinkedIn Content Assistant. Goodbye!")
            break
        
        # Create a combined input with conversation history
        if conversation_history:
            combined_input = f"Previous Conversation:\n{conversation_history}\n\nCurrent Request: {user_input}"
            
        else:
            combined_input = user_input
            
        # Run the agent with user_input and previous context
        result = Runner.run_sync(
            orchestrator_variable,
            input = combined_input
        )
        
        # Store the response
        assistant_response = result.final_output
        
        # Update conversation history
        conversation_history += f"User: {user_input}\nAssistant: {assistant_response}\n\n"
        
        print(f"\nAssistant: {result.final_output}")