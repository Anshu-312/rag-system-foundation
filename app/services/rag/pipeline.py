from app.services.ingestion.embedder import embed_text
from app.services.generation.prompt import build_prompt
from app.services.generation.llm_client import generate_answer
from app.services.retrieval.reranker import rerank
from app.evaluation.faithfulness import is_faithful

def run_rag_pipeline(query: str, store, top_k: int) -> tuple[str, list]:
    """
    Runs the Retrieval-Augmented Generation (RAG) pipeline.
    
    Args:
        query (str): The input query to be answered.
        store: The vector store to retrieve relevant documents from.
        top_k (int): The number of top relevant documents to retrieve.
        
    Returns:
        tuple[str, list]: A tuple containing the generated answer and the reranked chunks.
    """
    # Step 1: Embed the query (embed_text returns a list of vectors)
    query_vector = embed_text([query])[0]

    # Step 2: Retrieve chunks from the vector store broadly
    initial_chunks = store.search(query_vector, top_k)

    # Step 3: Rerank retrived chunks
    reranked_chunks = rerank(query, initial_chunks, top_n=4)

    # Step 4: Extract plain text chunks and build the prompt
    prompt = build_prompt(reranked_chunks, query)

    # Step 5: Generate the answer using the LLM client
    answer = generate_answer(prompt)

    # Step 6: (Optional) Evaluate faithfulness of the answer
    faithful = is_faithful(answer, reranked_chunks)
    if not faithful:
        answer += "\n\n(Note: The answer may not be fully supported by the provided context.)"

    # Return the answer and plain text sources to match the response model
    return answer, reranked_chunks