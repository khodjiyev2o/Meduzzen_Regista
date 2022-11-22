
from app.models.locations import Location
from app.models.users import User
from app.services.users import get_user
from sqlalchemy.future import select
from sqlalchemy import or_
from fastapi import HTTPException, Header, Depends
from app.schemas.locations import LocationCreateSchema, LocationSchema, LocationAlterSchema
from sqlalchemy.ext.asyncio import AsyncSession, async_object_session
from fastapi_pagination.ext.async_sqlalchemy import paginate
from fastapi_pagination import Params
from app.db import get_session
from typing import Optional
from app.services.auth import AuthHandler


auth_cls = AuthHandler()


class LocationCRUD:
    def __init__(self, session: Optional[AsyncSession] = None, location: Optional[Location] = None):
        if not session:
            self.session = async_object_session(location)
        else:
            self.session = session
        self.location = location

    async def create_location(self, location: LocationCreateSchema) -> LocationSchema:
        db_location = await self.session.execute(select(Location).filter(or_(Location.placename == location.placename)))
        db_location = db_location.scalars().first()
        if db_location:
            raise HTTPException(404, 'This location  already exists')
        else:
            new_location = Location(placename=location.placename, latitude=location.latitude, longitude=location.longitude)
            self.session.add(new_location)
            await self.session.commit()
            return LocationSchema(id=new_location.id, placename=location.placename, latitude=location.latitude, longitude=location.longitude)


    async def get_locations(self, page: int) -> list[LocationSchema]:
        params = Params(page=page, size=10)
        locations = await paginate(self.session, select(Location), params=params)
        return [LocationSchema(id=location.id, placename=location.placename, latitude=location.latitude, longitude=location.longitude) for location in locations.items]

    async def patch_location(self, location):
        if location.placename:
            self.location.placename =  location.placename
        if location.latitude:
            self.location.latitude = location.latitude
        if location.longitude:
            self.location.longitude = location.longitude
        await self.session.commit()
        return LocationSchema(id=self.location.id, placename=self.location.placename, latitude=self.location.latitude, longitude=self.location.longitude)
     




    async def delete_location(self, location_id: int) -> HTTPException:
        location_tobe_deleted = await self.session.get(Location,location_id)
        if location_tobe_deleted:
            await self.session.delete(location_tobe_deleted)
            await self.session.commit()
            return HTTPException(200,detail=f"Location with id {location_tobe_deleted.id} is successfully deleted")
        raise HTTPException(404,f"Location with id {id} not found")


async def get_location(id: int, session: AsyncSession = Depends(get_session), user: User = Depends(get_user)) -> Location:
    if user.admin:
        location = await session.get(Location, id)
        if location:
                return location
        else:
            raise HTTPException(404, 'location not found')
    raise HTTPException(404,"You are not authorized for this action!")