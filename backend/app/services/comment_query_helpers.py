from sqlalchemy.orm import Session, aliased

from app.ai.interfaces.capability import Capability
from app.models.comment_analysis import CommentAnalysis
from app.models.comment_analysis_result import CommentAnalysisResult


def get_non_spam_comments(db: Session, job_id: int) -> list[CommentAnalysis]:
    spam_result = aliased(CommentAnalysisResult)
    return (
        db.query(CommentAnalysis)
        .outerjoin(
            spam_result,
            (spam_result.comment_id == CommentAnalysis.id)
            & (spam_result.capability == Capability.SPAM.value),
        )
        .filter(
            CommentAnalysis.job_id == job_id,
            (spam_result.label != "spam") | (spam_result.label.is_(None)),
        )
        .order_by(CommentAnalysis.like_count.desc())
        .all()
    )
