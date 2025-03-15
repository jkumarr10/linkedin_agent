import logging
import asyncio
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.base import TaskResult
from autogen_agentchat.conditions import ExternalTermination, TextMentionTermination

from autogen_agent import LinkedInAgent


async def main(user_input: str):
    logging.info("Starting the LinkedIn agent...")
    agent = LinkedInAgent()

    # Define a termination condition that stops the task if the critic approves.
    text_termination = TextMentionTermination("APPROVE")

    # Create agents - need to await these async functions
    content_agent = await agent.generate_content()  
    post_agent = await agent.post_to_linkedin()  
    critic_agent = await agent.critic_agent()
    
    # Create a team with the agents
    team = RoundRobinGroupChat(
        [content_agent, post_agent, critic_agent],
        max_turns=2,
        termination_condition=text_termination
    )
    # Run the team with the user input
    result = await team.run(task=user_input) 
    print(result)  # Print the result instead of the stream object
        

if __name__ == "__main__":
    while True:
        user_input = input("Enter a query (type 'exit' to quit): ")
        if user_input.lower() == 'exit':
            print("Exiting program...")
            break
        asyncio.run(main(user_input=user_input))