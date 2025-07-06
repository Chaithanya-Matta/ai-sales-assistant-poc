from pinecone import Pinecone
from langchain_pinecone import PineconeVectorStore
from config.settings import settings
from config.model_config import embedding_model

# Pinecone initialization
pc = Pinecone(
    api_key=settings.PINECONE_API_KEY
)

index = pc.Index(
    name=settings.PINECONE_INDEX_NAME
)

vectorstore = PineconeVectorStore(
    index=index, 
    embedding=embedding_model
)