from typing import Annotated
from pydantic import Field, UUID4

from fastapi import Depends

from .service import assign_candidate_id


ScoreInt = Annotated[int, Field(ge=1, le=5)]
AssignCandidateIdDep = Annotated[UUID4, Depends(assign_candidate_id)]
