import os
import openai

openai.api_base = os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1")

BAIDU_API_KEY = os.getenv("BAIDU_API_KEY")
BAIDU_SECRET_KEY = os.getenv("BAIDU_SECRET_KEY")
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import OnlinePDFLoader, UnstructuredPDFLoader, PyPDFLoader
from langchain.text_splitter import TokenTextSplitter
from langchain.memory import ConversationBufferMemory
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.llms import OpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferWindowMemory
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
import os
from langchain.llms import OpenAI
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import CohereRerank
os.environ["COHERE_API_KEY"] = 'OHJ5kTLNlDfsu0SJfllGhkQ0EZPL8BJOn9tgFYJr'
from langchain.llms.openai import OpenAI
from langchain.chat_models import ChatOpenAI
llm =ChatOpenAI(model="gpt-3.5-turbo",temperature=0.2)
from langchain_community.embeddings import CohereEmbeddings
embeddings = CohereEmbeddings()
import getpass


import os
from langchain_fireworks import Fireworks
os.environ["FIREWORKS_API_KEY"] ="N5BcO9fLPPZUKemGQRqVeqQJErb1AHNU8lWUfsIERmWj1PJZ"
current_directory = os.getcwd()
file_name = "new244.pdf"
file_path = os.path.join(current_directory, file_name)
loader = PyPDFLoader(file_path)
pages = loader.load()
from langchain.text_splitter import RecursiveCharacterTextSplitter
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size = 1800,
    chunk_overlap  = 300,
    length_function = len,
)
splitData = text_splitter.split_documents(pages)
from langchain.vectorstores import Pinecone

vectorstore = FAISS.from_documents(splitData,embeddings)
faiss_retriever = vectorstore.as_retriever(search_kwargs={"k":5})

memory = ConversationBufferWindowMemory(memory_key="chat_history", k=3, return_messages=True)
chatQA = ConversationalRetrievalChain.from_llm(
            llm,
            retriever = faiss_retriever,
            memory=memory,verbose=True, )
chat_history = []
def q(qry):
  a= chatQA({"question": qry})
  return ((a['answer']))
