from app.core.config import settings
def chunk_text(
        text, 
        chunk_size: settings.chunk_size,
        overlap: settings.chunk_overlap): 
    """
    Splits the input text into chunks of specified size with a given overlap.

    Args:
        text (str): The input text to be chunked.
        chunk_size (int): The size of each chunk.
        overlap (int): The number of overlapping characters between chunks.

    Returns:
        List[str]: A list of text chunks.
    """
    words= text.split()
    chunks = []
    start = 0

    while start < len(words):
        end = start + chunk_size
        chunks.append(" ".join(words[start:end]))
        start = end - overlap

    return chunks