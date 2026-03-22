"""
Unit tests for ORM model domain methods and properties.

These tests are pure Python — no database, no fixtures requiring
a session. They test the behaviour of model instances directly.

Test organisation:
    Happy paths:  Expected inputs produce expected outputs.
    Sad paths:    Invalid or boundary inputs produce correct failures.
    Edge cases:   Boundary values and unusual but valid scenarios.
"""

import pytest
from decimal import Decimal
from datetime import datetime

from models.contract import Contract
from models.client import Client
from models.event import Event
from models.collaborator import Collaborator
from permissions.roles import RoleEnum, ContractStatus, ClientStatus


class TestContractStatusProperties:
    """Tests for is_signed and is_cancelled computed properties.

    Happy paths: statuses that should return True for each property.
    Sad paths:   statuses that should return False.
    """

    # ────────────────────────────────────────
    # Happy Path
    # ────────────────────────────────────────

    def test_signed_contract_is_signed_property(self, signed_contract):
        """Happy path: a SIGNED contract reports is_signed as True."""
        assert signed_contract.is_signed is True