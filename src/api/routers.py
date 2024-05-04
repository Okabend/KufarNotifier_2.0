from api.telegram import router as router_telegram
from api.users import router as router_users

all_routers = [
    router_telegram,
    router_users,
]
