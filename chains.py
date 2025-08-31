import os
import json
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain.schema import HumanMessage, AIMessage

# Load environment variables
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Initialize Gemini (main content generation)
gemini = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    temperature=0.3,
    google_api_key=GOOGLE_API_KEY
)

# Initialize memory for conversation history
memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True,
    max_token_limit=2000
)

def generate_service_info(service_query: str, session_id: str = None):
    """Main chain for government helpbot using only Gemini with structured output and memory."""
    
    # Add user query to memory
    memory.chat_memory.add_user_message(service_query)
    
    # Get conversation history for context
    chat_history = memory.chat_memory.messages if memory.chat_memory.messages else []
    
    # Build context from previous interactions
    context = ""
    if len(chat_history) > 1:  # More than just the current query
        context = "Based on our previous conversation, here's updated information: "
    
    # First, get a structured response
    structured_prompt = f"""
    {context}For the government service query: "{service_query}"
    
    Please provide information in this exact format:
    
    OUTLINE:
    - Step 1: [action]
    - Step 2: [action] 
    - Step 3: [action]
    - Step 4: [action]
    
    GUIDE:
    [Write a 220-320 word detailed guide about the application process, including where to apply (online vs in-person), required documents, biometrics, fees, tracking, and collection instructions]
    
    FAQS:
    Q1: [common question about fees]
    A1: [clear answer]
    Q2: [common question about time]
    A2: [clear answer]
    Q3: [common question about lost documents]
    A3: [clear answer]
    Q4: [common question about minors]
    A4: [clear answer]
    
    IMPORTANT NOTES:
    - [reminder about official website]
    - [reminder about original documents]
    - [reminder about appointments]
    
    Keep the tone clear, simple, and official-style.
    """
    
    try:
        # Get the structured response
        response = gemini.invoke(structured_prompt).content
        
        # Parse the response into our desired structure
        lines = response.split('\n')
        
        # Initialize variables
        outline = []
        guide = ""
        faqs = []
        important_notes = []
        
        current_section = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            if line.startswith('OUTLINE:'):
                current_section = 'outline'
            elif line.startswith('GUIDE:'):
                current_section = 'guide'
            elif line.startswith('FAQS:'):
                current_section = 'faqs'
            elif line.startswith('IMPORTANT NOTES:'):
                current_section = 'important_notes'
            elif line.startswith('- ') and current_section == 'outline':
                outline.append(line[2:])
            elif line.startswith('- ') and current_section == 'important_notes':
                important_notes.append(line[2:])
            elif current_section == 'guide' and line and not line.startswith('Q') and not line.startswith('A'):
                guide += line + " "
            elif line.startswith('Q') and current_section == 'faqs':
                # Extract Q&A pairs
                if ':' in line:
                    question = line.split(':', 1)[1].strip()
                    # Look for the next answer
                    for next_line in lines[lines.index(line)+1:]:
                        if next_line.strip().startswith('A') and ':' in next_line:
                            answer = next_line.split(':', 1)[1].strip()
                            faqs.append({"question": question, "answer": answer})
                            break
        
        # Clean up guide text
        guide = guide.strip()
        
        # Ensure we have at least some content
        if not outline:
            outline = ["Step 1: Gather required documents", "Step 2: Submit application", "Step 3: Pay fees", "Step 4: Collect result"]
        if not guide:
            guide = "Please refer to the official government website for detailed information about this service."
        if not faqs:
            faqs = [
                {"question": "What are the fees?", "answer": "Check the official website for current fee structure."},
                {"question": "How long does it take?", "answer": "Processing time varies, check with the office."},
                {"question": "What if I lose my documents?", "answer": "Contact the office immediately for guidance."},
                {"question": "Can minors apply?", "answer": "Yes, with proper documentation and parental consent."}
            ]
        if not important_notes:
            important_notes = ["Always check the official website", "Bring original documents", "Make an appointment if required"]
        
        # Create the response
        ai_response = {
            "outline": outline,
            "guide": guide,
            "faqs": faqs,
            "important_notes": important_notes
        }
        
        # Add AI response to memory
        memory.chat_memory.add_ai_message(json.dumps(ai_response))
        
        return ai_response
                
    except Exception as e:
        # Fallback for any errors
        error_response = {
            "outline": ["Error: Could not generate response"],
            "guide": f"An error occurred: {str(e)}",
            "faqs": [],
            "important_notes": ["Please try again", "Check your API key", "Contact support if issue persists"]
        }
        
        # Add error response to memory
        memory.chat_memory.add_ai_message(json.dumps(error_response))
        
        return error_response

def get_conversation_history():
    """Get the current conversation history."""
    return memory.chat_memory.messages

def clear_conversation_history():
    """Clear the conversation history."""
    memory.clear()

def get_session_summary():
    """Get a summary of the current session."""
    messages = memory.chat_memory.messages
    if not messages:
        return "No conversation history yet."
    
    user_messages = [msg.content for msg in messages if isinstance(msg, HumanMessage)]
    return f"Session has {len(user_messages)} queries: {', '.join(user_messages[:3])}{'...' if len(user_messages) > 3 else ''}"
