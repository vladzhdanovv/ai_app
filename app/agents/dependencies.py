from typing import Annotated

from fastapi import Depends

from .service import Workflow, get_workflow


WorkflowDep = Annotated[Workflow, Depends(get_workflow)]
