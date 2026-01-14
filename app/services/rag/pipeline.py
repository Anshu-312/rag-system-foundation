from app.services.ingestion.embedder import embed_text
from app.services.generation.prompt import build_prompt
from app.services.generation.llm_client import generate_answer
from app.evaluation.faithfulness import is_faithful

def run_rag_pipeline(query: str, store, top_k: int) -> str:
    """
    Runs the Retrieval-Augmented Generation (RAG) pipeline.
    
    Args:
        query (str): The input query to be answered.
        store: The vector store to retrieve relevant documents from.
        top_k (int): The number of top relevant documents to retrieve.
        
    Returns:
        str: The generated answer based on the retrieved documents.
    """
    # Step 1: Embed the query (embed_text returns a list of vectors)
    query_vector = embed_text([query])[0]

    # Step 2: Retrieve relevant documents from the vector store
    relevant_chunks = store.search(query_vector, top_k)

    # Step 3: Extract plain text chunks and build the prompt
    context_chunks = [chunk.get("text") if isinstance(chunk, dict) else str(chunk) for chunk in relevant_chunks]
    prompt = build_prompt(context_chunks, query)

    # Step 4: Generate the answer using the LLM client
    answer = generate_answer(prompt)

    # Step 5: (Optional) Evaluate faithfulness of the answer
    faithful = is_faithful(answer, context_chunks)
    if not faithful:
        answer += "\n\n(Note: The answer may not be fully supported by the provided context.)"

    # Return the answer and plain text sources to match the response model
    return answer, context_chunks