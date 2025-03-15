import os
from typing import List
from dotenv import load_dotenv
from autogen import ConversableAgent, GroupChat, GroupChatManager, UserProxyAgent, register_function

# Change the import to be relative since we're already in the app directory
from linkedin_tools import Linkedin

# Load env variables
load_dotenv()

# Load Linkedin Class
linkedin = Linkedin()
llm_config = {"api_type": "openai", "model": "gpt-4o-mini", "api_key": os.getenv("OPENAI_API_KEY")}

# Create a wrapper function for LinkedIn posting
def post_to_linkedin_wrapper(generated_content: str, visibility: str = "CONNECTIONS"):
    """
    Wrapper function for posting to LinkedIn
    
    Args:
        generated_content (str): The content to post
        visibility (str, optional): Post visibility. Defaults to "CONNECTIONS"
    
    Returns:
        dict: Response from LinkedIn API
    """
    print(f"post_to_linkedin_wrapper called with content: {generated_content[:50]}...")
    result = linkedin.post_to_linkedin(generated_content, visibility)
    print(f"LinkedIn posting result: {result}")
    return result

# Define Agents
def content_creator_assistant():
    with open("prompts/content_generation_prompt.txt", "r") as f:
        content_generation_prompt = f.read()

    content_generator_agent = ConversableAgent(
        name = "content_generator_agent",
        llm_config = llm_config,
        system_message= content_generation_prompt
    )

    return content_generator_agent

def post_to_linkedin_assistant():
    
    post_to_linkedin_agent = ConversableAgent(
        name = "post_to_linkedin_agent",
        llm_config = llm_config,
        system_message= """You are a LinkedIn posting assistant.
        Your job is to take approved content and post it to LinkedIn. You will do this only when the user approves the generated content.
        
        IMPORTANT: You MUST use the post_to_linkedin_wrapper function to post content to LinkedIn.
        To call the function, use the exact format:
        
        <function_call>
        post_to_linkedin_wrapper
        {
          "generated_content": "The full text of the approved LinkedIn post",
          "visibility": "CONNECTIONS"
        }
        </function_call>
        
        When you receive content from the content generator, you should:
        1. Acknowledge the content
        2. Call the post_to_linkedin_wrapper function with the content using the exact format shown above
        3. Report back the results of the posting
        
        Always confirm when a post has been successfully published or report any errors.
        """
    )

    return post_to_linkedin_agent

def user_proxy_assistant():
    
    user_proxy_agent = UserProxyAgent(
        name="user_proxy_agent",
        human_input_mode="ALWAYS",
        code_execution_config={
            "use_docker": False
        },
        system_message="""
        You will interact with the system as the user. Only pass on the generated content to the posting agent, if the user approves it. 
        """
    )
    
    return user_proxy_agent

# Tool Registration
def group_chat_manager(user_input: str):
    
    posting_agent = post_to_linkedin_assistant()
    user_proxy = user_proxy_assistant()
    content_creator_agent = content_creator_assistant()
    
    # Register the LinkedIn posting tool with the wrapper function
    register_function(
        post_to_linkedin_wrapper,
        caller=posting_agent,
        executor=user_proxy,
        description="Use this tool to post content to LinkedIn",
    )

    groupchat = GroupChat(
        agents = [user_proxy, content_creator_agent, posting_agent],
        speaker_selection_method="manual",
        messages=[]
    )
    
    manager = GroupChatManager(
        name="group_manager",
        groupchat = groupchat,
        llm_config=llm_config
    )
    
    response = user_proxy.initiate_chat(
        recipient=manager,
        message=user_input
    )
    
    return response


if __name__ == "__main__":
    user_input = "Create a short LinkedIn post about the benefits of networking on LinkedIn and then post it to my profile."
    response = group_chat_manager(user_input)

    
    