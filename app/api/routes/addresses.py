import logging

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.db.session import get_db_session
from app.schemas import AddressCreate, AddressRead, AddressUpdate, NearbyAddress, NearbySearchParams
from app.services.address_service import (
    create_address,
    delete_address,
    find_nearby_addresses,
    get_address,
    list_addresses,
    update_address,
)

router = APIRouter(prefix="/addresses", tags=["addresses"])
logger = logging.getLogger("address_book.routes.addresses")


@router.get("", response_model=list[AddressRead])
def get_addresses(session: Session = Depends(get_db_session)) -> list[AddressRead]:
    logger.info("Listing all addresses")
    return list_addresses(session)


@router.post("", response_model=AddressRead, status_code=status.HTTP_201_CREATED)
def create_address_endpoint(
    payload: AddressCreate, session: Session = Depends(get_db_session)
) -> AddressRead:
    logger.info("Creating address with label '%s'", payload.label)
    try:
        return create_address(session, payload)
    except SQLAlchemyError as exc:
        session.rollback()
        logger.exception("Database error while creating address")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to save address",
        ) from exc


@router.get("/search/nearby", response_model=list[NearbyAddress])
def get_nearby_addresses(
    latitude: float = Query(..., ge=-90, le=90),
    longitude: float = Query(..., ge=-180, le=180),
    distance_km: float = Query(..., gt=0, le=20000),
    session: Session = Depends(get_db_session),
) -> list[NearbyAddress]:
    params = NearbySearchParams(
        latitude=latitude,
        longitude=longitude,
        distance_km=distance_km,
    )
    logger.info(
        "Searching nearby addresses for latitude=%s longitude=%s distance_km=%s",
        latitude,
        longitude,
        distance_km,
    )
    return find_nearby_addresses(session, params)


@router.get("/{address_id}", response_model=AddressRead)
def get_address_endpoint(address_id: int, session: Session = Depends(get_db_session)) -> AddressRead:
    logger.info("Fetching address id=%s", address_id)
    address = get_address(session, address_id)
    if address is None:
        logger.warning("Address id=%s not found", address_id)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Address not found")
    return address


@router.put("/{address_id}", response_model=AddressRead)
def update_address_endpoint(
    address_id: int, payload: AddressUpdate, session: Session = Depends(get_db_session)
) -> AddressRead:
    logger.info("Updating address id=%s", address_id)
    address = get_address(session, address_id)
    if address is None:
        logger.warning("Address id=%s not found for update", address_id)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Address not found")

    try:
        return update_address(session, address, payload)
    except SQLAlchemyError as exc:
        session.rollback()
        logger.exception("Database error while updating address id=%s", address_id)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update address",
        ) from exc


@router.delete("/{address_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_address_endpoint(address_id: int, session: Session = Depends(get_db_session)) -> Response:
    logger.info("Deleting address id=%s", address_id)
    address = get_address(session, address_id)
    if address is None:
        logger.warning("Address id=%s not found for deletion", address_id)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Address not found")

    try:
        delete_address(session, address)
    except SQLAlchemyError as exc:
        session.rollback()
        logger.exception("Database error while deleting address id=%s", address_id)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete address",
        ) from exc

    return Response(status_code=status.HTTP_204_NO_CONTENT)
