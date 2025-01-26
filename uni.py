from langchain_community.document_loaders import PyMuPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders.merge import MergedDataLoader

# Paths to your PDF files
profile_pdf_path = "Profile.pdf"
transcript_pdf_path = "UCP-Transcript.pdf"





def load_split_docs(doc1, doc2):
    loader1 = PyMuPDFLoader(doc1)
    loader2 = PyMuPDFLoader(doc2)
    
    loader_all = MergedDataLoader(loaders=[loader1, loader2])
    # # loading documents
    docs_all = loader_all.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size = 1000, chunk_overlap = 200)
    # Splitting text into chunks and returning as a dictionary
    docs_chunks = text_splitter.split_documents(docs_all)
    return docs_chunks


