Govt HelpBot

A chatbot built with LangChain and Gemini AI to help Pakistani citizens quickly access government services such as CNIC renewal, passport renewal, and more.

This project was developed as part of an academic assignment to demonstrate AI-powered citizen assistance using conversational agents.

Features

Conversational AI with Memory: Retains context during a session for more natural interactions.

Gemini AI Integration: Processes natural language queries about government procedures.

LangChain Framework: Handles prompt chaining and logic flow.

Streamlit Interface: Provides a simple, interactive, and user-friendly web app.

Modular Design: Easily extendable to more services.

Installation

1. Clone the Repository
git clone <your-repo-url>
cd Govt-help

2. Create a Virtual Environment
python -m venv .venv
source .venv/bin/activate   # On Windows: .venv\Scripts\activate

3. Install Dependencies
pip install -r requirements.txt

4. Set Up Environment Variables

Create a .env file (do not share this file publicly). Use the .env.example for reference:

GOOGLE_API_KEY=your_google_gemini_api_key_here

Usage
Run the Local App
streamlit run app.py


Once started, open the URL provided by Streamlit (usually http://localhost:8501) to access the chatbot.

Example Query
How can I renew my CNIC in Pakistan?


The bot will provide a structured outline of steps, detailed instructions, and relevant information.

Project Structure
Govt-help/
├── app.py                # Streamlit app entry point
├── chains.py             # Core LangChain logic
├── try_chains.py         # Test script to verify chain functionality
├── requirements.txt      # Python dependencies
├── .env.example          # Example environment variables (no real keys)
└── README.md             # Project documentation

How It Works

User Input – The citizen types their query in the Streamlit app.

LangChain Memory – Keeps the conversation context during a session.

Gemini Model – Processes the query and generates a structured response.

Formatted Output – The chatbot provides a step-by-step outline and detailed guidance.

Future Improvements

Deploy Globally: Host on Streamlit Cloud, Hugging Face Spaces, or Render.

Multi-Language Support: Add Urdu.

Expanded Services: Cover more government procedures (e.g., driving license renewal, tax filing).

License

This project is created for educational purposes and does not represent an official government service.
