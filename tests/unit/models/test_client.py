"""
Unit tests for the Client ORM model.

Tests cover:
    - full_name computed property
    - full_name_formal computed property
    - has_active_support computed property
"""

import pytest
from unittest.mock import MagicMock


class TestClientFullName:
    """Tests for full_name and full_name_formal computed properties.

    Mirrors TestCollaboratorFullName — same logic, separate model.
    """

    @pytest.mark.parametrize("first, last, expected", [
        ("Jean",  "Durand",     "Jean Durand"),
        ("Marie", "Leclerc",    "Marie Leclerc"),
        ("Anne",  "de la Rue",  "Anne de la Rue"),   # edge: compound name
    ])
    def test_full_name(self, prospect_client, first, last, expected):
        """Parametrized: full_name returns first + last in display format."""
        prospect_client.first_name = first
        prospect_client.last_name = last
        assert prospect_client.full_name == expected

    @pytest.mark.parametrize("first, last, expected", [
        ("Jean",  "Durand",    "DURAND, Jean"),
        ("Marie", "Leclerc",   "LECLERC, Marie"),
        ("Anne",  "de la Rue", "DE LA RUE, Anne"),   # edge: compound name
    ])
    def test_full_name_formal(self, prospect_client, first, last, expected):
        """Parametrized: full_name_formal returns LAST, First format."""
        prospect_client.first_name = first
        prospect_client.last_name = last
        assert prospect_client.full_name_formal == expected


class TestClientHasActiveSupport:
    """Tests for the has_active_support computed property.

    This property traverses client → contracts → event → support_id.
    We use MagicMock to simulate the relationship chain without a DB.

    Happy path:  at least one event has a support_id set.
    Sad paths:   no contracts, contracts with no events,
                 events with no support assigned.
    """

    def _make_contract_with_event(self, support_id):
        """Helper: build a mock contract whose event has the given support_id."""
        event = MagicMock()
        event.support_id = support_id
        contract = MagicMock()
        contract.event = event
        return contract

    def _make_contract_without_event(self):
        """Helper: build a mock contract with no linked event."""
        contract = MagicMock()
        contract.event = None
        return contract

    # ── Happy Path ────────────────────────────────────────────────────────────

    def test_has_active_support_when_event_has_support(self, prospect_client):
        """Happy path: one contract with one event with support assigned."""
        prospect_client.contracts = [
            self._make_contract_with_event(support_id=3)
        ]
        assert prospect_client.has_active_support is True

    def test_has_active_support_with_multiple_contracts(self, prospect_client):
        """Happy path: multiple contracts, only one event has support."""
        prospect_client.contracts = [
            self._make_contract_without_event(),
            self._make_contract_with_event(support_id=3),
        ]
        assert prospect_client.has_active_support is True

    # ── Sad Path ──────────────────────────────────────────────────────────────

    def test_no_support_when_no_contracts(self, prospect_client):
        """Sad path: client with no contracts returns False."""
        prospect_client.contracts = []
        assert prospect_client.has_active_support is False

    def test_no_support_when_contracts_have_no_events(self, prospect_client):
        """Sad path: contracts exist but none have a linked event."""
        prospect_client.contracts = [
            self._make_contract_without_event(),
            self._make_contract_without_event(),
        ]
        assert prospect_client.has_active_support is False

    def test_no_support_when_event_has_no_support_assigned(self, prospect_client):
        """Sad path: event exists but support_id is None."""
        prospect_client.contracts = [
            self._make_contract_with_event(support_id=None)
        ]
        assert prospect_client.has_active_support is False
