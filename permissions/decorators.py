"""
Role-based access control decorator for Epic Events CRM.

Provides the @require_role decorator which enforces that the
current user holds one of the permitted roles before a service
function is allowed to execute.

This is the first of two permission layers:
    Layer 1 — @require_role: department-level check (this file)
    Layer 2 — ownership checks inside service functions
              e.g. client.commercial_id == current_user.id

Usage:
    from permissions.decorators import require_role
    from permissions.roles import RoleEnum

    @require_role(RoleEnum.MANAGEMENT)
    def create_collaborator(session, current_user, ...):
        ...

    @require_role(RoleEnum.MANAGEMENT, RoleEnum.COMMERCIAL)
    def create_contract(session, current_user, ...):
        ...
"""

import functools
from permissions.roles import RoleEnum
from exceptions import PermissionError as CRMPermissionError


def require_role(*roles: RoleEnum):
    """Decorator factory that enforces role-based access on service functions.

    Wraps a service function and checks that current_user.role is in
    the list of permitted roles before allowing execution. Raises
    CRMPermissionError if the check fails.

    The decorated function must accept current_user as a keyword argument.
    The current_user object must have a .role attribute of type RoleEnum
    and an .is_active attribute — inactive collaborators are always blocked
    regardless of role.

    Args:
        *roles: One or more RoleEnum values that are permitted to call
                the decorated function.

    Returns:
        Callable: The wrapped function with role enforcement applied.

    Raises:
        CRMPermissionError: If current_user is None, is inactive, or
                            does not hold one of the permitted roles.

    Example:
        @require_role(RoleEnum.MANAGEMENT)
        def delete_collaborator(session, current_user, collaborator_id):
            ...
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            current_user = kwargs.get("current_user")

            if current_user is None:
                raise CRMPermissionError(
                    "Authentication required. Run: python main.py auth login"
                )

            if not current_user.is_active:
                raise CRMPermissionError(
                    "Your account has been deactivated. "
                    "Please contact Management."
                )

            if current_user.role not in roles:
                allowed = [r.value for r in roles]
                raise CRMPermissionError(
                    f"Access denied. This action requires one of: {allowed}. "
                    f"Your role: {current_user.role.value}"
                )

            return func(*args, **kwargs)
        return wrapper
    return decorator
