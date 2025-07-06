from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from config.settings import settings

llm = ChatOpenAI(
    model=settings.OPENAI_MODEL,
    # temperature=settings.OPENAI_TEMPERATURE,
    api_key=settings.OPENAI_API_KEY
)

embedding_model = OpenAIEmbeddings(
    api_key=settings.OPENAI_API_KEY,
    model=settings.OPENAI_EMBEDDING_MODEL
)