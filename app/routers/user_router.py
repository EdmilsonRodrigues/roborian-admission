from fastapi import APIRouter, HTTPException, Depends
from ..models import User
from typing import List
from ..db import get_database

router = APIRouter()

# POST endpoint to create a new user
@router.post("/users/", response_model=User)
async def create_user(user: User):
    # Assuming user validation and database insertion logic
    # Here you would typically validate the user input, hash passwords, etc.
    # For demonstration purposes, we'll assume direct database insertion

    # Get the database connection
    db = get_database()

    # Insert the user into the database
    new_user = await db.users.insert_one(user.model_dump())

    # Return the created user with an autogenerated ID
    return {**user.model_dump(), "_id": str(new_user.inserted_id)}

# GET endpoint to get user data by email
@router.get("/users/{email}", response_model=User)
async def get_user(email: str, db=Depends(get_database)):
    # Query the database for the user by email
    user_data = await db.users.find_one({"email": email})

    # If user not found, raise HTTPException with status code 404 (Not found)
    if not user_data:
        raise HTTPException(status_code=404, detail="User not found")

    # Return the user data
    return user_data