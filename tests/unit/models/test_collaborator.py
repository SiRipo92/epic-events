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


class TestCollaboratorPassword:
    """Tests for set_password() and verify_password() domain methods.

    Happy path:  correct password verifies True.
    Sad paths:   wrong password, empty password.
    Edge cases:  special characters, very long password.
    """

    def test_set_password_stores_hash_not_plaintext(self, management_collaborator):
        """Happy path: password is hashed — plaintext is never stored."""
        management_collaborator.set_password("securepassword123")
        assert management_collaborator.password_hash != "securepassword123"
        assert management_collaborator.password_hash.startswith("$2b$")

    def test_verify_password_correct(self, management_collaborator):
        """Happy path: correct password returns True."""
        management_collaborator.set_password("securepassword123")
        assert management_collaborator.verify_password("securepassword123") is True

    def test_verify_password_wrong(self, management_collaborator):
        """Sad path: incorrect password returns False."""
        management_collaborator.set_password("securepassword123")
        assert management_collaborator.verify_password("wrongpassword") is False

    def test_verify_password_empty_string(self, management_collaborator):
        """Sad path: empty string does not match a real password."""
        management_collaborator.set_password("securepassword123")
        assert management_collaborator.verify_password("") is False

    @pytest.mark.parametrize("password", [
        "p@$$w0rd!",              # special characters
        "a" * 72,                 # bcrypt max length boundary
        "pässwörð",               # unicode characters
    ])
    def test_set_and_verify_various_passwords(
        self, management_collaborator, password
    ):
        """Edge case: various password formats hash and verify correctly."""
        management_collaborator.set_password(password)
        assert management_collaborator.verify_password(password) is True
