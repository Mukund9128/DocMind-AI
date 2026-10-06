import numpy as np

try:
    from sentence_transformers import SentenceTransformer
except Exception:
    SentenceTransformer = None


_model = None


def model():
    global _model

    if _model is None and SentenceTransformer:
        _model = SentenceTransformer('all-MiniLM-L6-v2')

    return _model


def retrieve(question, chunks, k=5):
    if not chunks:
        return []

    m = model()

    # Fallback if embedding model is unavailable
    if m is None:
        return chunks[:k]

    texts = [c.content for c in chunks]

    embeddings = m.encode(
        texts,
        normalize_embeddings=True
    )

    question_embedding = m.encode(
        [question],
        normalize_embeddings=True
    )[0]

    scores = np.dot(
        embeddings,
        question_embedding
    )

    # ------------------------------------------------
    # Group chunks by document
    # ------------------------------------------------

    document_groups = {}

    for index, chunk in enumerate(chunks):
        document_groups.setdefault(
            chunk.document_id,
            []
        ).append(index)

    selected_indices = []

    # ------------------------------------------------
    # MULTIPLE DOCUMENTS
    # Retrieve relevant chunks from EACH document
    # ------------------------------------------------

    if len(document_groups) > 1:

        per_document = max(
            2,
            k // len(document_groups)
        )

        for document_id, indices in document_groups.items():

            ranked = sorted(
                indices,
                key=lambda i: scores[i],
                reverse=True
            )

            added = 0

            for i in ranked:

                if scores[i] > 0.15:
                    selected_indices.append(i)
                    added += 1

                if added >= per_document:
                    break

        # Sort final results by relevance
        selected_indices = sorted(
            selected_indices,
            key=lambda i: scores[i],
            reverse=True
        )

    # ------------------------------------------------
    # SINGLE DOCUMENT
    # Original behaviour
    # ------------------------------------------------

    else:

        selected_indices = (
            np.argsort(scores)[::-1][:k]
        )

        selected_indices = [
            int(i)
            for i in selected_indices
            if scores[int(i)] > 0.15
        ]

    return [
        chunks[int(i)]
        for i in selected_indices
    ]