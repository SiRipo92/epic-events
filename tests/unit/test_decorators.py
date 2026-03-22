"""
Unit tests for the @require_role access control decorator.

Tests cover all three guard layers in order:
    1. No current_user provided
    2. current_user is inactive
    3. current_user role not in allowed roles
    4. current_user role is allowed — function executes

No database required — uses fixtures from conftest.py.
"""

import pytest

from permissions.decorators import require_role
from permissions.roles import RoleEnum
from exceptions import PermissionError as CRMPermissionError


class TestRequireRoleGuards:
    """Tests for the three guard layers inside @require_role.

    Happy path:  correct role allows execution.
    Sad paths:   missing user, inactive user, wrong role.
    """

    # ── Helper — a simple decorated function to test against ─────────────────

    @staticmethod
    def _make_action(*roles):
        """Return a decorated function that requires the given roles."""
        @require_role(*roles)
        def action(session=None, current_user=None):
            return "executed"
        return action

    # ── Happy Path ────────────────────────────────────────────────────────────

    def test_correct_role_allows_execution(self, management_collaborator):
        """Happy path: Management user passes Management-only guard."""
        action = self._make_action(RoleEnum.MANAGEMENT)
        result = action(current_user=management_collaborator)
        assert result == "executed"

    def test_one_of_multiple_roles_allows_execution(self, commercial_collaborator):
        """Happy path: Commercial user passes Management+Commercial guard."""
        action = self._make_action(RoleEnum.MANAGEMENT, RoleEnum.COMMERCIAL)
        result = action(current_user=commercial_collaborator)
        assert result == "executed"

    # ── Sad Path ──────────────────────────────────────────────────────────────

    def test_raises_when_no_current_user(self):
        """Sad path: no current_user passed raises CRMPermissionError."""
        action = self._make_action(RoleEnum.MANAGEMENT)
        with pytest.raises(CRMPermissionError, match="Authentication required"):
            action()

    def test_raises_when_current_user_is_none(self):
        """Sad path: current_user=None raises CRMPermissionError."""
        action = self._make_action(RoleEnum.MANAGEMENT)
        with pytest.raises(CRMPermissionError, match="Authentication required"):
            action(current_user=None)

    def test_raises_when_collaborator_is_inactive(self, inactive_collaborator):
        """Sad path: inactive collaborator blocked regardless of role."""
        action = self._make_action(RoleEnum.COMMERCIAL)
        with pytest.raises(CRMPermissionError, match="deactivated"):
            action(current_user=inactive_collaborator)

    def test_raises_when_wrong_role(self, support_collaborator):
        """Sad path: Support user blocked by Management-only guard."""
        action = self._make_action(RoleEnum.MANAGEMENT)
        with pytest.raises(CRMPermissionError, match="Access denied"):
            action(current_user=support_collaborator)

    # ── Edge Cases ────────────────────────────────────────────────────────────

    @pytest.mark.parametrize("role", [
        RoleEnum.COMMERCIAL,
        RoleEnum.SUPPORT,
    ])
    def test_non_management_roles_blocked_from_management_action(
        self, make_collaborator, role
    ):
        """Edge case: every non-Management role is blocked from Management-only action."""
        action = self._make_action(RoleEnum.MANAGEMENT)
        user = make_collaborator(role=role)
        with pytest.raises(CRMPermissionError):
            action(current_user=user)
