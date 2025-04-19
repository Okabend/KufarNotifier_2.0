from abc import ABC, abstractmethod

from sqlalchemy import insert, select, update

from db.db import async_session_maker


class AbstractRepository(ABC):
    @abstractmethod
    async def add_one():
        raise NotImplementedError

    @abstractmethod
    async def find_all():
        raise NotImplementedError

    @abstractmethod
    async def find_by_id():
        raise NotImplementedError

    @abstractmethod
    async def update_one():
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository):
    model = None

    async def add_one(self, data: dict) -> int:
        async with async_session_maker() as session:
            stmt = insert(self.model).values(**data).returning(self.model.id)
            res = await session.execute(stmt)
            await session.commit()
            return res.scalar_one()

    async def find_all(self, filters=None):
        async with async_session_maker() as session:
            stmt = select(self.model)
            res = await session.execute(stmt)
            #
            # query = self.session.query(self.model)
            #
            # if filters:
            #     for key, value in filters.items():
            #         query = query.filter(getattr(self.model, key) == value)
            #
            # results = query.all()
            #
            res = [row[0].to_read_model() for row in res.all()]
            return res

    async def find_by_id(self, id: int):
        async with async_session_maker() as session:
            stmt = select(self.model).where(self.model.id == id)
            res = await session.execute(stmt)
            res = res.scalar_one().to_read_model()
            return res

    async def update_one(self, id: int, data: dict):
        async with async_session_maker() as session:
            stmt = update(self.model).where(self.model.id == id).values(**data)
            await session.execute(stmt)
            await session.commit()
