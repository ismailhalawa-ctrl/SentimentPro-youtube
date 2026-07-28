from sqlalchemy.orm import Session

from app.ai.embeddings.embedding_registry import get_embedding_provider_by_id
from app.ai.rag.vector_store_registry import get_vector_store
from app.core.config import settings
from app.models.comment_analysis import CommentAnalysis
from app.models.embedding_index import EmbeddingIndex, EmbeddingIndexStatus
from app.services.embedding_service import collection_name_for_job


class RetrievalError(RuntimeError):
    pass


async def retrieve_relevant_comments(
    db: Session, job_id: int, question: str, top_k: int | None = None
) -> list[dict]:
    index_row = db.query(EmbeddingIndex).filter(EmbeddingIndex.job_id == job_id).first()
    if index_row is None or index_row.status != EmbeddingIndexStatus.COMPLETE:
        raise RetrievalError("This job hasn't been indexed for the comment assistant yet.")

    embedding_provider = get_embedding_provider_by_id(index_row.embedding_provider_id)
    query_vector = (await embedding_provider.embed([question]))[0]

    vector_store = get_vector_store()
    matches = await vector_store.query(
        collection_name_for_job(job_id), query_vector, top_k or settings.rag_top_k
    )
    if not matches:
        return []

    comment_ids = [m.metadata.get("comment_id") for m in matches if m.metadata.get("comment_id") is not None]
    rows = db.query(CommentAnalysis).filter(CommentAnalysis.id.in_(comment_ids)).all()
    rows_by_id = {row.id: row for row in rows}

    results = []
    for match in matches:
        comment_id = match.metadata.get("comment_id")
        comment = rows_by_id.get(comment_id) if comment_id is not None else None
        if comment is None:
            continue
        results.append(
            {
                "comment_id": comment.id,
                "text": comment.text,
                "author": comment.author_display_name,
                "like_count": comment.like_count,
                "score": match.score,
            }
        )
    return results
