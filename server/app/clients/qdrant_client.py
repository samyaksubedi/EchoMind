from langchain_qdrant import QdrantVectorStore
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document
from app.config import settings


def embed_and_store(chunks: list[dict], conversation_id: str) -> None:
    # convert chunks to LangChain Documents
    docs = []
    for chunk in chunks:
        # build metadata based on chunk type
        metadata = {"conversationId": conversation_id}

        if "startTime" in chunk:
            # audio/video/youtube chunk
            metadata["startTime"] = chunk["startTime"]
            metadata["endTime"] = chunk["endTime"]
        else:
            # pdf chunk
            metadata["pageNumber"] = chunk["pageNumber"]

        docs.append(Document(page_content=chunk["text"], metadata=metadata))

    # embed and store in Qdrant
    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small", api_key=settings.OPENAI_API_KEY
    )

    QdrantVectorStore.from_documents(
        documents=docs,
        embedding=embeddings,
        url=settings.get_qdrant_url,
        collection_name="echomind_chunks",
        force_recreate=False,  # don't wipe existing chunks
    )
