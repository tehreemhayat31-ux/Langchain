# app.py
import streamlit as st
import os
from dotenv import load_dotenv
from chains import generate_service_info, get_conversation_history, clear_conversation_history, get_session_summary

# Load environment variables
load_dotenv()

# Check if API key is available
if not os.getenv("GOOGLE_API_KEY"):
    st.error("❌ GOOGLE_API_KEY not found in .env file. Please add your Gemini API key.")
    st.stop()

# Initialize session state for LangChain memory
if 'conversation_started' not in st.session_state:
    st.session_state.conversation_started = False
if 'current_query' not in st.session_state:
    st.session_state.current_query = ""

# Page configuration
st.set_page_config(
    page_title="Government HelpBot",
    page_icon="🏛️",
    layout="wide"
)

# Main title
st.title("🏛️ Government HelpBot")
st.markdown("Get help with government services and procedures")

# Sidebar with session management
with st.sidebar:
    st.header("ℹ️ About")
    st.markdown("""
    This bot helps you understand government services and procedures.
    
    **How to use:**
    1. Type your question
    2. Click "Get Help"
    3. Review the outline, guide, FAQs, and notes
    
    **Powered by:** Gemini AI + LangChain Memory
    """)
    
    st.header("🔑 API Status")
    if os.getenv("GOOGLE_API_KEY"):
        st.success("✅ Gemini API Key: Configured")
    else:
        st.error("❌ Gemini API Key: Missing")
    
    st.header("💾 Session Management")
    
    # Session summary
    session_summary = get_session_summary()
    st.info(session_summary)
    
    # Clear conversation button
    if st.button("🗑️ Clear History", type="secondary"):
        clear_conversation_history()
        st.session_state.conversation_started = False
        st.rerun()
    
    # Show conversation count
    history = get_conversation_history()
    if history:
        user_messages = [msg for msg in history if hasattr(msg, 'type') and msg.type == 'human']
        st.metric("Conversation Count", len(user_messages))

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    st.header("Ask Your Question")
    user_query = st.text_input(
        "What government service do you need help with?",
        placeholder="e.g., How to renew CNIC in Pakistan?",
        help="Type your question about any government service or procedure",
        key="user_input"
    )
    
    # Submit button
    if st.button("🚀 Get Help", type="primary", use_container_width=True):
        if user_query.strip():
            st.session_state.current_query = user_query
            st.session_state.conversation_started = True
            
            with st.spinner("🤖 Generating helpful information..."):
                try:
                    # Get response from the chain with memory
                    response = generate_service_info(user_query)
                    
                    # Display results in tabs
                    tab1, tab2, tab3, tab4 = st.tabs(["📋 Outline", "📖 Detailed Guide", "❓ FAQs", "⚠️ Important Notes"])
                    
                    with tab1:
                        st.subheader("Step-by-Step Outline")
                        if isinstance(response["outline"], list):
                            for i, step in enumerate(response["outline"], 1):
                                st.write(f"{i}. {step}")
                        else:
                            st.write(response["outline"])
                    
                    with tab2:
                        st.subheader("Complete Citizen Guide")
                        st.write(response["guide"])
                    
                    with tab3:
                        st.subheader("Frequently Asked Questions")
                        if isinstance(response["faqs"], list) and response["faqs"]:
                            for i, faq in enumerate(response["faqs"], 1):
                                with st.expander(f"Q{i}: {faq.get('question', 'Question')}"):
                                    st.write(faq.get('answer', 'Answer not available'))
                        else:
                            st.write("No FAQs available")
                    
                    with tab4:
                        st.subheader("Important Notes")
                        if isinstance(response["important_notes"], list):
                            for note in response["important_notes"]:
                                st.write(f"• {note}")
                        else:
                            st.write(response["important_notes"])
                        
                    st.success("✅ Information generated successfully!")
                    
                except Exception as e:
                    st.error(f"❌ An error occurred: {str(e)}")
                    st.info("Please check your API key and try again.")
        else:
            st.warning("⚠️ Please enter a question to get help.")

with col2:
    st.header("🔄 Conversation History")
    
    if st.session_state.conversation_started:
        history = get_conversation_history()
        if history:
            # Display recent conversation
            for i, message in enumerate(history[-6:], 1):  # Show last 6 messages
                if hasattr(message, 'type'):
                    if message.type == 'human':
                        st.markdown(f"**👤 Q{i}:** {message.content[:100]}{'...' if len(message.content) > 100 else ''}")
                    elif message.type == 'ai':
                        st.markdown(f"**🤖 A{i}:** Generated response")
                else:
                    st.markdown(f"**💬 Message {i}:** {str(message)[:100]}...")
    else:
        st.info("Start a conversation to see history here!")

# Footer
st.markdown("---")
st.markdown("Built with ❤️ using Streamlit, Gemini AI, and LangChain Memory")
