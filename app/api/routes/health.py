"""
============================================================
Health API
============================================================
"""

from fastapi import APIRouter
from app.system.diagnose import build_report

router = APIRouter(
    prefix="/health",
    tags=["Health"]
)


@router.get("")
def health():
    """
    Return the overall platform health report.
    """

    return build_report()