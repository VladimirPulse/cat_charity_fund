from http import HTTPStatus
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charityproject import charity_project_crud
# from app.crud.reservation import reservation_crud
# from app.models.meeting_room import MeetingRoom
# импортировать их можно прямо из пакета.
from app.models import CharityProject, User


async def check_name_duplicate(
        project_name: str,
        session: AsyncSession,
) -> None:
    project_id = await charity_project_crud.get_project_id_by_name(project_name, session)
    if project_id is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Проект с таким именем уже существует!',
        )

        
async def check_project_exists(
        project_id: int,
        session: AsyncSession,
) -> CharityProject:
    project = await charity_project_crud.get(project_id, session)
    if project is None:
        raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
            detail='Проект не найден!'
        )
    return project

async def check_project_full_amount(
        project_id: int,
        full_amount: int,
        session: AsyncSession,
) -> CharityProject:
    project = await charity_project_crud.get(project_id, session)
    if project.full_amount > full_amount:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Нелья установить значение full_amount меньше уже вложенной суммы.'
        )
    return project


async def check_project_remove(
        project: CharityProject,
) -> CharityProject:
    # import pdb;pdb.set_trace()
    if project.close_date or project.fully_invested == True:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='В проект были внесены средства, не подлежит удалению!'
        )
    return project

# async def check_reservation_intersections(**kwargs) -> None:
#     reservations = await reservation_crud.get_reservations_at_the_same_time(
#         **kwargs
#     )
#     if reservations:
#         raise HTTPException(
#             status_code=422,
#             detail=str(reservations)
#         )


# async def check_reservation_before_edit(
#         reservation_id: int,
#         session: AsyncSession,
#         user: User
# ) -> Reservation:
#     reservation = await reservation_crud.get(
#         # Для понятности кода можно передавать аргументы по ключу.
#         obj_id=reservation_id, session=session 
#     )
#     if user.id != reservation.user_id and not user.is_superuser:
#         raise HTTPException(
#             status_code=403,
#             detail='Невозможно редактировать или удалить чужую бронь!'
#         )
#     if reservation is None:
#         raise HTTPException(
#             status_code=404,
#             detail='Бронь не найдена!!'
#         )
#     return reservation
