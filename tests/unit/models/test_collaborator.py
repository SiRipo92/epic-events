"""
Unit tests for the Collaborator ORM model.

Tests cover:
    - full_name computed property
    - full_name_formal computed property
    - is_manager, is_commercial, is_support convenience properties
"""

import pytest
from permissions.roles import RoleEnum


class TestCollaboratorFullName:
    """Tests for full_name and full_name_formal computed properties."""

    @pytest.mark.parametrize("first, last, expected", [
        ("Alice",   "Martin",   "Alice Martin"),
        ("Jean",    "Dupont",   "Jean Dupont"),
        ("Marie",   "de la Tour", "Marie de la Tour"),  # edge: compound name
    ])
    def test_full_name(self, management_collaborator, first, last, expected):
        """Parametrized: full_name returns first + last in display format."""
        management_collaborator.first_name = first
        management_collaborator.last_name = last
        assert management_collaborator.full_name == expected

    @pytest.mark.parametrize("first, last, expected", [
        ("Alice", "Martin",     "MARTIN, Alice"),
        ("Jean",  "Dupont",     "DUPONT, Jean"),
        ("Marie", "de la Tour", "DE LA TOUR, Marie"),  # edge: compound name
    ])
    def test_full_name_formal(self, management_collaborator, first, last, expected):
        """Parametrized: full_name_formal returns LAST, First format."""
        management_collaborator.first_name = first
        management_collaborator.last_name = last
        assert management_collaborator.full_name_formal == expected


class TestCollaboratorRoleProperties:
    """Tests for is_manager, is_commercial, is_support convenience properties."""

    @pytest.mark.parametrize("role, is_manager, is_commercial, is_support", [
        (RoleEnum.MANAGEMENT, True,  False, False),
        (RoleEnum.COMMERCIAL, False, True,  False),
        (RoleEnum.SUPPORT,    False, False, True),
    ])
    def test_role_properties(
        self, management_collaborator, role,
        is_manager, is_commercial, is_support
    ):
        """Parametrized: exactly one role property is True per role."""
        management_collaborator.role = role
        assert management_collaborator.is_manager    is is_manager
        assert management_collaborator.is_commercial is is_commercial
        assert management_collaborator.is_support    is is_support
