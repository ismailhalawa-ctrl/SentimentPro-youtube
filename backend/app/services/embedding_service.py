import logging

from sqlalchemy.orm import Session

from app.ai.embeddings.embedding_registry import get_embedding_provider
from app.ai.rag.vector_store_registry import get_vector_store
from app.models.embedding_index import EmbeddingIndex, EmbeddingIndexStatus
from app.services.comment_query_helpers import get_non_spam_comments

logger = logging.getLogger(__name__)

_EMBED_CHUNK_SIZE = 64


def collection_name_for_job(job_id: int) -> str:
    return f"job_{job_id}"


async def index_job_comments(job_id: int, db: Session) -> None:
    existing = db.query(EmbeddingIndex).filter(EmbeddingIndex.job_id == job_id).first()
    if existing is not None and existing.status == EmbeddingIndexStatus.COMPLETE:
        return

    embedding_provider = get_embedding_provider()
    vector_store = get_vector_store()

    index_row = existing or EmbeddingIndex(
        job_id=job_id,
        embedding_provider_id=embedding_provider.provider_id,
        vector_store_provider_id=vector_store.provider_id,
        vector_count=0,
        status=EmbeddingIndexStatus.PENDING,
    )
    if existing is None:
        db.add(index_row)
        db.commit()

    if not vector_store.is_configured():
        index_row.status = EmbeddingIndexStatus.FAILED
        index_row.error_message = f"Vector store '{vector_store.provider_id}' is not configured."
        db.commit()
        return

    try:
        comments = get_non_spam_comments(db, job_id)
        if not comments:
            index_row.status = EmbeddingIndexStatus.COMPLETE
            index_row.vector_count = 0
            db.commit()
            return

        collection_name = collection_name_for_job(job_id)
        total_indexed = 0
        for chunk_start in range(0, len(comments), _EMBED_CHUNK_SIZE):
            chunk = comments[chunk_start : chunk_start + _EMBED_CHUNK_SIZE]
            texts = [c.text for c in chunk]
            embeddings = await embedding_provider.embed(texts)
            await vector_store.upsert(
                collection_name=collection_name,
                ids=[f"comment_{c.id}" for c in chunk],
                embeddings=embeddings,
                documents=texts,
                metadatas=[
                    {"comment_id": c.id, "author": c.author_display_name, "like_count": c.like_count}
                    for c in chunk
                ],
            )
            total_indexed += len(chunk)

        index_row.embedding_provider_id = embedding_provider.provider_id
        index_row.vector_store_provider_id = vector_store.provider_id
        index_row.vector_count = total_indexed
        index_row.status = EmbeddingIndexStatus.COMPLETE
        index_row.error_message = None
        db.commit()
        logger.info(
            "Indexed %d comments for job %s into '%s'", total_indexed, job_id, vector_store.provider_id
        )
    except Exception as exc:
        logger.exception("Embedding indexing failed for job %s", job_id)
        index_row.status = EmbeddingIndexStatus.FAILED
        index_row.error_message = str(exc)[:1024]
        db.commit()
