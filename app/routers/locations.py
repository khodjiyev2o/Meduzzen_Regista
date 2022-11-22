from app.schemas.locations import LocationCreateSchema, LocationAlterSchema, LocationSchema
from app.models.locations import Location
from app.models.users import User
from app.services.locations import LocationCRUD, get_location
from app.db import get_session
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.users import get_user

location_router = APIRouter(
    prefix="/locations",
    tags=["locations"],
    responses={404: {"description": "Not found"}},
)






@location_router.post('/add', response_model=LocationSchema)
async def add_location(location: LocationCreateSchema, session: AsyncSession = Depends(get_session)) -> LocationSchema:
    location = await LocationCRUD(session=session).create_location(location)
    return location


@location_router.get('/all', response_model=list[LocationSchema])
async def all_locations(session: AsyncSession = Depends(get_session), page: int = Query(default=1)) -> list[LocationSchema]:
    result = await LocationCRUD(session=session).get_locations(page)
    return result



@location_router.patch('/patch', response_model=LocationSchema)
async def patch_location(location: LocationAlterSchema,user: User = Depends(get_user), db_location: Location = Depends(get_location)) -> LocationSchema:
    if user.admin:
        location = await LocationCRUD(location=db_location).patch_location(location=location)
        return location
    raise HTTPException(403,f"This user is not autharized to update a location")


@location_router.delete('/delete')
async def delete_location(location_id: int,user: User = Depends(get_user), location: Location = Depends(get_location)) -> HTTPException:
    if user.admin:
        location = await LocationCRUD(location=location).delete_location(location_id=location_id)
        return location
    raise HTTPException(403,f"This user is not autharized to delete a location")