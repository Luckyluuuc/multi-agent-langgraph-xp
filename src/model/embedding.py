from langchain_ollama import OllamaEmbeddings

class Embddings:
    """
    A class to handle embedding queries using the Ollama model.
    """
    def __init__(self, model: str = "mxbai-embed-large"):
        self.model = model
        self.embedding_model = OllamaEmbeddings(model=self.model)

    def embed_query(self, query: str):
        """Embed a query using the specified model."""
        return self.embedding_model.embed_query(query)
    
    def get_embedding_obj(self): 
        """return the object of the embedding model"""
        return self.embedding_model
    

        


if __name__ == "__main__":
    # Example usage
    embeddings = Embddings()
    query_embedding = embeddings.embed_query("What is the weather today?")
    print(type(query_embedding), len(query_embedding))

