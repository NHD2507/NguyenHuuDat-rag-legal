# src/retriever.py

import chromadb

from src.embedding import (
    embed_query,
    embed_texts,
)


class LegalRetriever:
    def __init__(
        self,
        db_path="./chroma_db",
        collection_name="legal_docs",
    ):

        self.client = chromadb.PersistentClient(
            path=db_path
        )

        self.collection = self.client.get_or_create_collection(
            name=collection_name
        )

    def count(self):
        return self.collection.count()

    def add_documents(self, chunks):

        # Tránh add trùng khi Streamlit rerun
        if self.collection.count() > 0:
            print(
                f"Collection already contains "
                f"{self.collection.count()} documents"
            )
            return

        texts = [
            c["text"]
            for c in chunks
        ]

        embeddings = embed_texts(texts)

        self.collection.add(
            ids=[
                str(i)
                for i in range(len(chunks))
            ],
            documents=texts,
            embeddings=embeddings,
            metadatas=[
                {
                    "page": c["page"],
                    "source": c["source"],
                }
                for c in chunks
            ],
        )

        print(
            f"Added {len(chunks)} chunks "
            f"to ChromaDB"
        )

    def retrieve(
        self,
        query,
        top_k=5,
    ):

        query_embedding = embed_query(query)

        results = self.collection.query(
            query_embeddings=[
                query_embedding
            ],
            n_results=top_k,
            include=[
                "documents",
                "metadatas",
                "distances",
            ],
        )

        return results

    def reset_collection(self):

        try:

            self.client.delete_collection(
                name="legal_docs"
            )

            self.collection = (
                self.client.get_or_create_collection(
                    name="legal_docs"
                )
            )

            print(
                "Collection reset successfully"
            )

        except Exception as e:

            print(
                f"Reset failed: {e}"
            )

    def get_stats(self):

        return {
            "total_chunks":
                self.collection.count(),
            "collection_name":
                self.collection.name,
        }