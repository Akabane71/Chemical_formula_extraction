from fastapi import APIRouter
from app.api.routers.servers import router as servers_router
from app.api.routers.health import router as health_router

router = APIRouter(
    prefix="/api/v1",
    tags=["v1"],
)


# 包含各个子路由

# Severs 路由
router.include_router(
    servers_router,
)

# Health 路由
router.include_router(
    health_router,
)


# 你可以在这里添加更多的路由包含