from openai import OpenAI


class EmbeddingsGenerator:
    """Class to generate embeddings for text."""

    openai_client: OpenAI | None = None

    @staticmethod
    def init_models() -> None:
        """Initialize embedding models."""
        EmbeddingsGenerator.openai_client = OpenAI()

    @staticmethod
    def embed_openai(
        *, texts: list[str], embedding_model: str = "text-embedding-3-small"
    ) -> list[list[float]]:
        """Embed text using OpenAI's text embedding API."""
        model = EmbeddingsGenerator.openai_client
        if not model:
            msg = "Model not initialized"
            raise ValueError(msg)

        vals = model.embeddings.create(
            input=texts, model=embedding_model, timeout=60 * 10.0
        ).data
        return [v.embedding for v in vals]
