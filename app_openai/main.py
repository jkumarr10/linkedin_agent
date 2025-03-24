import streamlit as st
import asyncio
import nest_asyncio
from agents_openai import orchestrator
from agents import Runner

# Apply nest_asyncio to allow nested event loops
nest_asyncio.apply()

def main():
    # Initialize Orchestrator Agent
    if "orchestrator_agent" not in st.session_state:
        st.session_state.orchestrator_agent = orchestrator()
    
    # Initialize Title
    st.title("LinkedIn Content Generator & Poster Assistant")
    
    # Initialize Conversation History
    if "conversation_history" not in st.session_state:
        st.session_state.conversation_history = []
    
    # Display Conversation History on app rerun
    for message in st.session_state.conversation_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            
    # Initialize User Input
    user_input = st.chat_input("Ask Away")
    
    # React to User Input
    if prompt := user_input:
        # Display user message in chat message container
        st.chat_message("user").markdown(prompt)
        
        # Add user message to chat history
        st.session_state.conversation_history.append({"role": "user", "content": prompt})
        
        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            # Create new event loop and set it as the current one
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            # Format the input for the agent
            formatted_input = "\n".join([
                f"{m['role'].capitalize()}: {m['content']}"
                for m in st.session_state.conversation_history
            ])
            
            
            # Run the agent
            result = Runner.run_sync(
                st.session_state.orchestrator_agent,
                input=formatted_input
            )
            
            # Display the response
            response = result.final_output
            st.write(response)
    
        # Add assistant response to chat history
        st.session_state.conversation_history.append({"role": "assistant", "content": response})
    
    
if __name__ == "__main__":
    main()