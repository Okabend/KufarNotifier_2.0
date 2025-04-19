from schemas.users import UserSchemaAdd
from utils.repository import AbstractRepository


class UsersService:
    def __init__(self, users_repo: AbstractRepository):
        self.users_repo: AbstractRepository = users_repo()

    async def add_user(self, user: UserSchemaAdd):
        user_dict = user.model_dump()
        user_id = await self.users_repo.add_one(user_dict)
        return user_id

    async def get_users(self):
        users = await self.users_repo.find_all()
        return users

    async def get_user(self, user_id: int):
        user = await self.users_repo.find_by_id(user_id)
        return user

    async def update_user_name(self, user_id: int, new_name: str):
        user = await self.get_user(user_id)
        if user:
            user_data = {'name': new_name}
            await self.users_repo.update_one(user_id, user_data)
            return True
        return False
