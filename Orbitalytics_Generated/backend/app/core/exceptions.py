"""
Orbitalytics - Custom Exceptions
"""
from fastapi import HTTPException, status

class DatasetNotFoundError(HTTPException):
    def __init__(self, dataset_name: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Space Research dataset '{dataset_name}' not found."
        )

class ForecastingError(HTTPException):
    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Forecasting engine error: {detail}"
        )

class HadoopExecutionError(HTTPException):
    def __init__(self, service: str, detail: str):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Hadoop ecosystem error ({service}): {detail}"
        )

class PipelineExecutionError(HTTPException):
    def __init__(self, stage: str, detail: str):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Pipeline stage '{stage}' execution failed: {detail}"
        )
