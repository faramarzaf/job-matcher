from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse

from app.repositories.cv_data_repository import CVDataRepository
from app.services.auth_service import AuthService
from app.services.cv_extraction_service import CVExtractionService
from app.services.job_matching_service import JobMatchingService

cv_router = APIRouter()


@cv_router.post("/upload")
async def upload_cv(
        file: UploadFile = File(...),
        current_user=Depends(AuthService.get_current_user)
):
    try:
        skills = await CVExtractionService.extract_cv_data(file)

        cv_data_id = await CVDataRepository.create_or_update_cv_data(
            user_id=current_user.id,
            skills=skills,
        )
        return {"message": "CV uploaded successfully", "cv_data_id": cv_data_id}


    except HTTPException as he:
        return JSONResponse(content={"message": he.detail}, status_code=he.status_code)

    except Exception as e:
        return JSONResponse(content={"message": str(e)}, status_code=500)


@cv_router.get("/recommendations")
async def get_job_recommendations(current_user=Depends(AuthService.get_current_user)):
    try:
        recommended_jobs = await JobMatchingService.recommend_jobs(current_user.id)
        return {"jobs": recommended_jobs}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
