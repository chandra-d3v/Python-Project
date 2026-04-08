from geopy.distance import geodesic
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Address
from app.schemas import AddressCreate, AddressUpdate, NearbyAddress, NearbySearchParams


def list_addresses(session: Session) -> list[Address]:
    statement = select(Address).order_by(Address.id)
    return list(session.scalars(statement).all())


def get_address(session: Session, address_id: int) -> Address | None:
    return session.get(Address, address_id)


def create_address(session: Session, payload: AddressCreate) -> Address:
    address = Address(**payload.model_dump())
    session.add(address)
    session.commit()
    session.refresh(address)
    return address


def update_address(session: Session, address: Address, payload: AddressUpdate) -> Address:
    updates = payload.model_dump(exclude_unset=True)
    for field, value in updates.items():
        setattr(address, field, value)
    session.add(address)
    session.commit()
    session.refresh(address)
    return address


def delete_address(session: Session, address: Address) -> None:
    session.delete(address)
    session.commit()


def find_nearby_addresses(session: Session, params: NearbySearchParams) -> list[NearbyAddress]:
    addresses = list_addresses(session)
    origin = (params.latitude, params.longitude)
    nearby: list[NearbyAddress] = []

    for address in addresses:
        distance_km = geodesic(origin, (address.latitude, address.longitude)).kilometers
        if distance_km <= params.distance_km:
            nearby.append(
                NearbyAddress(
                    **address.__dict__,
                    distance_km=round(distance_km, 3),
                )
            )

    nearby.sort(key=lambda item: item.distance_km)
    return nearby
