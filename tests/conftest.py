"""
Shared pytest fixtures for the Epic Events CRM test suite.

Fixtures are organised by scope:
    - Model instance fixtures: plain Python objects, no DB required.
      Used by unit tests in tests/unit/.
    - DB session fixtures: in-memory SQLite session.
      Used by integration tests in tests/integration/.

All model instance fixtures use minimal valid data — just enough
to satisfy non-nullable constraints. Tests that need specific values
set their own attributes directly.
"""

import pytest
from datetime import datetime
from decimal import Decimal

from models.collaborator import Collaborator
from models.client import Client
from models.contract import Contract
from models.event import Event
from permissions.roles import RoleEnum, ContractStatus, ClientStatus


# ── Collaborator fixtures ─────────────────────────────────────────────────────

@pytest.fixture
def management_collaborator():
    """A minimally valid active Management collaborator instance.

    No database — pure Python object for unit tests.
    """
    c = Collaborator()
    c.id = 1
    c.first_name = "Alice"
    c.last_name = "Martin"
    c.email = "alice@epicevents.com"
    c.role = RoleEnum.MANAGEMENT
    c.is_active = True
    c.password_hash = "hashed"
    return c


@pytest.fixture
def commercial_collaborator():
    """A minimally valid active Commercial collaborator instance."""
    c = Collaborator()
    c.id = 2
    c.first_name = "Bob"
    c.last_name = "Dupont"
    c.email = "bob@epicevents.com"
    c.role = RoleEnum.COMMERCIAL
    c.is_active = True
    c.password_hash = "hashed"
    return c


@pytest.fixture
def support_collaborator():
    """A minimally valid active Support collaborator instance."""
    c = Collaborator()
    c.id = 3
    c.first_name = "Carol"
    c.last_name = "Leblanc"
    c.email = "carol@epicevents.com"
    c.role = RoleEnum.SUPPORT
    c.is_active = True
    c.password_hash = "hashed"
    return c


@pytest.fixture
def inactive_collaborator():
    """A deactivated collaborator — cannot log in or perform actions."""
    c = Collaborator()
    c.id = 4
    c.first_name = "Dave"
    c.last_name = "Ancien"
    c.email = "dave@epicevents.com"
    c.role = RoleEnum.COMMERCIAL
    c.is_active = False
    c.password_hash = "hashed"
    return c


# ── Client fixtures ───────────────────────────────────────────────────────────

@pytest.fixture
def prospect_client():
    """A freshly created client — default PROSPECT status, no contracts."""
    c = Client()
    c.id = 1
    c.first_name = "Jean"
    c.last_name = "Durand"
    c.email = "jean@company.com"
    c.commercial_id = 2
    c.status = ClientStatus.PROSPECT
    c.contracts = []
    return c


@pytest.fixture
def active_client():
    """A client with a signed contract — ACTIVE status, needs support assigned."""
    c = Client()
    c.id = 2
    c.first_name = "Marie"
    c.last_name = "Leclerc"
    c.email = "marie@company.com"
    c.commercial_id = 2
    c.status = ClientStatus.ACTIVE
    c.contracts = []
    return c


# ── Contract fixtures ─────────────────────────────────────────────────────────

@pytest.fixture
def draft_contract():
    """A contract in DRAFT status — cannot yet create events against it."""
    c = Contract()
    c.id = 1
    c.client_id = 1
    c.commercial_id = 2
    c.total_amount = Decimal("5000.00")
    c.remaining_amount = Decimal("5000.00")
    c.status = ContractStatus.DRAFT
    return c


@pytest.fixture
def signed_contract():
    """A contract in SIGNED status — events can be created against it."""
    c = Contract()
    c.id = 2
    c.client_id = 1
    c.commercial_id = 2
    c.total_amount = Decimal("5000.00")
    c.remaining_amount = Decimal("2500.00")
    c.status = ContractStatus.SIGNED
    return c


@pytest.fixture
def completed_contract():
    """A contract in COMPLETED status — fully paid and delivered."""
    c = Contract()
    c.id = 3
    c.client_id = 1
    c.commercial_id = 2
    c.total_amount = Decimal("5000.00")
    c.remaining_amount = Decimal("0.00")
    c.status = ContractStatus.COMPLETED
    return c


@pytest.fixture
def cancelled_contract():
    """A contract in CANCELLED status — no further actions possible."""
    c = Contract()
    c.id = 4
    c.client_id = 1
    c.commercial_id = 2
    c.total_amount = Decimal("3000.00")
    c.remaining_amount = Decimal("3000.00")
    c.status = ContractStatus.CANCELLED
    return c


@pytest.fixture
def fully_paid_contract():
    """A signed contract with zero remaining amount."""
    c = Contract()
    c.id = 5
    c.client_id = 1
    c.commercial_id = 2
    c.total_amount = Decimal("4000.00")
    c.remaining_amount = Decimal("0.00")
    c.status = ContractStatus.SIGNED
    return c


@pytest.fixture
def unpaid_contract():
    """A signed contract with remaining balance."""
    c = Contract()
    c.id = 6
    c.client_id = 1
    c.commercial_id = 2
    c.total_amount = Decimal("4000.00")
    c.remaining_amount = Decimal("1500.00")
    c.status = ContractStatus.SIGNED
    return c


# ── Event fixtures ────────────────────────────────────────────────────────────

@pytest.fixture
def event_without_support():
    """An event with no support assigned — needs Management to assign."""
    e = Event()
    e.id = 1
    e.contract_id = 2
    e.title = "Annual Gala"
    e.start_date = datetime(2025, 9, 1, 18, 0)
    e.end_date = datetime(2025, 9, 1, 23, 0)
    e.support_id = None
    e.is_cancelled = False
    return e


@pytest.fixture
def event_with_support(support_collaborator):
    """An event with a support collaborator assigned."""
    e = Event()
    e.id = 2
    e.contract_id = 2
    e.title = "Product Launch"
    e.start_date = datetime(2025, 10, 15, 9, 0)
    e.end_date = datetime(2025, 10, 15, 17, 0)
    e.support_id = support_collaborator.id
    e.is_cancelled = False
    return e


@pytest.fixture
def eight_hour_event():
    """An event with exactly 8 hours duration for duration_hours() tests."""
    e = Event()
    e.id = 3
    e.contract_id = 2
    e.title = "Workshop"
    e.start_date = datetime(2025, 11, 1, 9, 0)
    e.end_date = datetime(2025, 11, 1, 17, 0)
    e.support_id = None
    e.is_cancelled = False
    return e
