# main.py
import os
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain.tools.retriever import create_retriever_tool
from langchain import hub
from langchain_astradb import AstraDBVectorStore
from dotenv import load_dotenv
from github import get_github_data
from uni import load_split_docs
from email_tool_calling import setup_gmail_agent 

load_dotenv()

# Paths to your PDF files
profile_pdf_path = "Profile.pdf"
transcript_pdf_path = "UCP-Transcript.pdf"


def connect_to_vector_db():
    embeddings = OpenAIEmbeddings()
    ASTRA_DB_API_ENDPOINT = os.getenv('ASTRA_DB_API_ENDPOINT')
    ASTRA_DB_APPLICATION_TOKEN = os.getenv('ASTRA_DB_APPLICATION_TOKEN')
    desired_namespace = os.getenv('ASTRA_DB_KEYSPACE')

    if desired_namespace is not None:
        ASTRA_DB_KEYSPACE = desired_namespace
    else:
        ASTRA_DB_KEYSPACE = None

    Astra_vector_Store = AstraDBVectorStore(
        embedding=embeddings,
        collection_name="asktbs",
        api_endpoint=ASTRA_DB_API_ENDPOINT,
        token=ASTRA_DB_APPLICATION_TOKEN,
        namespace=ASTRA_DB_KEYSPACE
    )
    return Astra_vector_Store    

astra_vectordb = connect_to_vector_db()

# Fetching data
owner = "Tayyabbutt1133"
gitub_data = get_github_data(owner)
uni_data = load_split_docs(transcript_pdf_path, profile_pdf_path)
complete_data = gitub_data + uni_data
astra_vectordb.add_documents(complete_data)

# Creating retriever tool for GitHub data
retriever = astra_vectordb.as_retriever(search_kwargs={"k": 6})
retriever_tool = create_retriever_tool(
    retriever,
    name="github_search",
    description="Search for information about Tayyeb's GitHub repositories and Computer Science degree subjects. Use this tool to retrieve relevant repository data.",
)

# Setup Gmail agent tools
gmail_tools = setup_gmail_agent() 

# Pull the prompt template for the agent
prompt = hub.pull("hwchase17/openai-functions-agent")

# Create the LLM for the agent
llm = ChatOpenAI()

# Create the agent for both tools (GitHub + Gmail)
tools = [retriever_tool] + gmail_tools  # Include both tools here

# Create the tool calling agent
agent = create_tool_calling_agent(
    llm=llm,
    tools=tools,  # Pass the combined tools list
    prompt=prompt,
)

agent_executor = AgentExecutor(agent=agent, tools=tools)

# Interactive loop to ask questions
while (question := input("Ask AI Assistant Related to Tayyeb's Software Projects, Computer Science Degree, or email Generation: ")) != "q":
    try:
        result = agent_executor.invoke({"input": question, "agent_scratchpad": ""})
        print(result.get("output", "No output received."))
    except Exception as e:
        print(f"Error: {e}")
