"""
Unit tests for the Contract ORM model.

Tests cover:
    - is_signed computed property (all ContractStatus values)
    - is_cancelled computed property (all ContractStatus values)
    - is_fully_paid() domain method
"""

import pytest
from decimal import Decimal
from permissions.roles import ContractStatus


class TestContractStatusProperties:
    """Tests for is_signed and is_cancelled computed properties.

    Uses parametrize to test all ContractStatus values in one sweep
    rather than one test per status. This catches regressions if a
    new status is added without updating the property logic.
    """

    @pytest.mark.parametrize("status, expected", [
        (ContractStatus.SIGNED,    True),
        (ContractStatus.COMPLETED, True),
        (ContractStatus.DRAFT,     False),
        (ContractStatus.PENDING,   False),
        (ContractStatus.CANCELLED, False),
    ])
    def test_is_signed(self, draft_contract, status, expected):
        """Parametrized: is_signed returns correct value for every status."""
        draft_contract.status = status
        assert draft_contract.is_signed is expected

    @pytest.mark.parametrize("status, expected", [
        (ContractStatus.CANCELLED, True),
        (ContractStatus.DRAFT,     False),
        (ContractStatus.PENDING,   False),
        (ContractStatus.SIGNED,    False),
        (ContractStatus.COMPLETED, False),
    ])
    def test_is_cancelled(self, draft_contract, status, expected):
        """Parametrized: is_cancelled returns correct value for every status."""
        draft_contract.status = status
        assert draft_contract.is_cancelled is expected


class TestContractIsFullyPaid:
    """Tests for the is_fully_paid() domain method.

    Happy paths:  zero remaining amount.
    Sad paths:    positive remaining amount.
    Edge cases:   exactly zero, overpaid, one cent remaining.
    """

    @pytest.mark.parametrize("remaining, expected", [
        (Decimal("0.00"),   True),   # happy: exactly zero
        (Decimal("-0.01"),  True),   # edge: overpaid
        (Decimal("0.01"),   False),  # edge: one cent remaining
        (Decimal("500.00"), False),  # sad: large balance remaining
    ])
    def test_is_fully_paid(self, draft_contract, remaining, expected):
        """Parametrized: is_fully_paid returns correct value for all amounts."""
        draft_contract.remaining_amount = remaining
        assert draft_contract.is_fully_paid() is expected
