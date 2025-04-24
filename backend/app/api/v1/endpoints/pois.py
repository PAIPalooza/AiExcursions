from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete

from app.api import deps
from app.models.poi import POI
from app.schemas.poi import POICreate, POIUpdate, POIInDB
from app.schemas.location import LocationQuery
from app.utils.geofence import is_within_radius
from app.core.auth import get_current_user

router = APIRouter()

@router.post("", response_model=POIInDB, status_code=status.HTTP_201_CREATED)
async def create_poi(
    *,
    db: AsyncSession = Depends(deps.get_db),
    poi_in: POICreate,
    current_user: dict = Depends(get_current_user)
) -> POIInDB:
    """Create new POI."""
    poi = POI(
        title=poi_in.title,
        description=poi_in.description,
        latitude=poi_in.latitude,
        longitude=poi_in.longitude,
        audio_url=poi_in.audio_url
    )
    db.add(poi)
    await db.commit()
    await db.refresh(poi)
    return poi

@router.get("/nearby", response_model=List[POIInDB])
async def get_nearby_pois(
    *,
    db: AsyncSession = Depends(deps.get_db),
    latitude: float = Query(..., ge=-90, le=90),
    longitude: float = Query(..., ge=-180, le=180),
    radius: float = Query(default=20.0, gt=0, le=1000),
    current_user: dict = Depends(get_current_user)
) -> List[POIInDB]:
    """Get POIs within specified radius of user's location."""
    # First, get all POIs
    result = await db.execute(select(POI))
    all_pois = result.scalars().all()
    
    # Filter POIs within radius
    nearby_pois = [
        poi for poi in all_pois
        if is_within_radius(
            latitude,
            longitude,
            poi.latitude,
            poi.longitude,
            radius
        )
    ]
    
    return nearby_pois

@router.get("/{poi_id}", response_model=POIInDB)
async def get_poi(
    *,
    db: AsyncSession = Depends(deps.get_db),
    poi_id: int,
    current_user: dict = Depends(get_current_user)
) -> POIInDB:
    """Get a POI by ID."""
    result = await db.execute(select(POI).where(POI.id == poi_id))
    poi = result.scalar_one_or_none()
    
    if poi is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"POI with ID {poi_id} not found"
        )
    
    return poi

@router.get("", response_model=List[POIInDB])
async def list_pois(
    *,
    db: AsyncSession = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: dict = Depends(get_current_user)
) -> List[POIInDB]:
    """List POIs with pagination."""
    result = await db.execute(select(POI).offset(skip).limit(limit))
    return result.scalars().all()

@router.put("/{poi_id}", response_model=POIInDB)
async def update_poi(
    *,
    db: AsyncSession = Depends(deps.get_db),
    poi_id: int,
    poi_in: POIUpdate,
    current_user: dict = Depends(get_current_user)
) -> POIInDB:
    """Update POI."""
    result = await db.execute(select(POI).filter(POI.id == poi_id))
    poi = result.scalar_one_or_none()
    if not poi:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="POI not found"
        )
    
    update_data = poi_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(poi, field, value)
    
    db.add(poi)
    await db.commit()
    await db.refresh(poi)
    return poi

@router.delete("/{poi_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_poi(
    *,
    db: AsyncSession = Depends(deps.get_db),
    poi_id: int,
    current_user: dict = Depends(get_current_user)
):
    """Delete POI."""
    result = await db.execute(select(POI).filter(POI.id == poi_id))
    poi = result.scalar_one_or_none()
    if not poi:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="POI not found"
        )
    
    await db.execute(delete(POI).where(POI.id == poi_id))
    await db.commit()
    return None
