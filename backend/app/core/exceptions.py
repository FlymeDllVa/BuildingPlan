from fastapi import HTTPException
from starlette.status import HTTP_409_CONFLICT

# Core

UNKNOWN_ERROR_EXCEPTION = HTTPException(
    status_code=HTTP_409_CONFLICT, detail="Unknown error."
)

# Graph

CONFLICT_GRAPH_EXCEPTION = HTTPException(
    status_code=HTTP_409_CONFLICT, detail="This graph already exists."
)

DOCUMENT_INSERT_EXCEPTION = HTTPException(
    status_code=HTTP_409_CONFLICT, detail="This document already exists."
)

DELETE_EXCEPTION = HTTPException(
    status_code=HTTP_409_CONFLICT, detail="Collection or view not found."
)
