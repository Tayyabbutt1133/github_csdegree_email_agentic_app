
from langchain_community.agent_toolkits import GmailToolkit
from langchain_community.tools.gmail.utils import (
    build_resource_service,
    get_gmail_credentials,
)
from dotenv import load_dotenv

load_dotenv()

def setup_gmail_agent():
    # Connect to Gmail
    credentials = get_gmail_credentials(
        token_file="token.json",
        scopes=["https://mail.google.com/"],
        client_secrets_file="credentials.json",
    )
    
    # Build the API resource service
    api_resource = build_resource_service(credentials=credentials)
    
    # Initialize the GmailToolkit and get the tools
    toolkit = GmailToolkit(api_resource=api_resource)
    tools = toolkit.get_tools()
    
    return tools  # Return the tools, not the agent execution
