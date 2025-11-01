import google.generativeai as genai
from langchain_core.messages import HumanMessage, AIMessage
import os
from dotenv import load_dotenv

# BaseMessage: the abstract class (common structure for all messages)
# HumanMessage: represents a user's input message
# AIMessage: represents a message from the AI model.

class SalesAgent:
    def __init__(self):
        """
        Initializes the SalesAgent using Google's Gemini model.
        Gemini 1.5 Flash is fast, capable, and has a free tier.
        """
        # Initialize Gemini client
        genai.configure(api_key="API-KEY")
        self.model = genai.GenerativeModel("gemini-2.0-flash")

    def respond(self, query):
        """
        Generates a response and includes an action tag for the orchestrator.
        """
        system_prompt = """
        You are a helpful, polite **Sales Agent** for a software company.

        ---

        ###  Primary Goal & Response Rules

        1.  **If the user's query is about SALES or GENERAL INFORMATION:**
            * Topics: **Pricing, subscription plans, product features, suitability/fit, company info, or any non-technical query.**
            * **Action:** Generate a polite, clear, and helpful conversational response.
            * **Internal Tag:** **Do NOT** append any action tag. Your response should look like a normal chat message.

        2.  **If the user's query is TECHNICAL:**
            * Topics: **Bugs, errors, technical issues, installation, configuration, troubleshooting, or code-related questions.**
            * **Action:** **Do NOT** generate a conversational response.
            * **Internal Tag (Exact Output):** Generate only the tag `[ACTION: TRANSFER_TO_TECH]`.

        ---
        ###  Critical Output Format Instructions

        * **For Sales/General Queries (Conversational Output):** Your output must be **ONLY** the polite, helpful response text.
            * *Example Output:* "Hello! Our Premium subscription includes unlimited user seats and 24/7 priority support. Would you like to know more about our pricing tiers?"
        * **For Technical Queries (Tag Only Output):** Your output must **ONLY** be the action tag. **No other text or explanation.**
            * *Example Output:* `[ACTION: TRANSFER_TO_TECH]`
        * Do not use any other format for the action tag.
        * Do not mention the internal action tag or the transfer process to the user.
        """
        response = self.model.generate_content(system_prompt +"\n"+ query)

        return response.text
    


class TechAgent:
    def __init__(self):
        """
        Initializes the SalesAgent using Google's Gemini model.
        """
        # Initialize Gemini client
        genai.configure(api_key="API-KEY")
        self.model = genai.GenerativeModel("gemini-2.0-flash")

    def respond(self, query):
        """
        Generates a technical support response using the previous chat history for context.
        """

        system_prompt = """
        You are an elite Technical Support Expert. You were just handed this conversation by the Sales Agent.

        1. **Acknowledge the Handover** briefly (e.g., "Hello, I see the Sales team flagged a crash report...").
        2. **Analyze the conversation history** to understand the full context of the issue.
        3. Provide clear, step-by-step troubleshooting or explain the solution professionally.
        """

        response = self.model.generate_content(system_prompt +"\n"+ query)

        return response.text