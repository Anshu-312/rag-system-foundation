from sentence_transformers import SentenceTransformer
from app.core.config import settings

_model = SentenceTransformer(settings.embedding_model)

def embed_text(texts: list[str]):
    """Generate embeddings for a list of texts using a pre-trained SentenceTransformer model.

    Args:
        texts (list[str]): A list of strings to be embedded.
    """ 
    return _model.encode(texts, normalize_embeddings=True).tolist()