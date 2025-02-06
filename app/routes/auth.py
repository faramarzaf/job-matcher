from fastapi import APIRouter, HTTPException

from app.repositories.user_repository import UserRepository
from app.schemas.auth import TokenResponse, GoogleLoginRequest
from app.services.auth_service import AuthService

auth_router = APIRouter()


@auth_router.post("/google-login", response_model=TokenResponse)
async def google_login(request: GoogleLoginRequest):
    try:
        id_info = await AuthService.verify_google_token(request.id_token)
        print(id_info)

        existing_user = await UserRepository.get_user_by_email(id_info['email'])

        if not existing_user:
            new_user_id = await UserRepository.create_user(email=id_info['email'])
            token = AuthService.create_access_token({"sub": id_info['email']})
        else:
            token = AuthService.create_access_token({"sub": existing_user.email})

        return {"access_token": token, "token_type": "bearer"}

    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))
