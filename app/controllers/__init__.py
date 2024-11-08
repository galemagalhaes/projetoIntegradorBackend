from .login import init_login_routes
from .user import init_user_routes
from .client import init_client_routes
from .sale import init_sale_routes
from .dashboard import init_dashboard_routes

__all__ = ["init_login_routes", "init_user_routes", "init_client_routes", "init_sale_routes", "init_dashboard_routes"]