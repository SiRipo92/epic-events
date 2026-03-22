"""
Shared pytest fixtures for the Epic Events CRM test suite.

Fixtures are organised by scope:
    - Factory fixtures: return a callable that builds model instances.
      Named fixtures call factories with specific values.
    - Model instance fixtures: plain Python objects, no DB required.
      Used by unit tests in tests/unit/.
    - DB session fixtures: in-memory SQLite session.
      Used by integration tests in tests/integration/.
"""

import pytest
from datetime import datetime, timedelta, timezone
from decimal import Decimal

from models.collaborator import Collaborator
from models.client import Client
from models.contract import Contract
from models.event import Event
from permissions.roles import RoleEnum, ContractStatus, ClientStatus


# ── Factory fixtures ──────────────────────────────────────────────────────────

@pytest.fixture
def make_collaborator():
    """Factory for Collaborator instances.

    Returns a callable so tests can build custom collaborators
    without needing a new fixture for every variation.

    Usage:
        def test_something(make_collaborator):
            user = make_collaborator(role=RoleEnum.SUPPORT, is_active=False)
    """
    def _factory(
        id=1,
        first_name="Test",
        last_name="User",
        email="test@epicevents.com",
        role=RoleEnum.MANAGEMENT,
        is_active=True,
        password_hash="hashed",
    ):
        c = Collaborator()
        c.id = id
        c.first_name = first_name
        c.last_name = last_name
        c.email = email
        c.role = role
        c.is_active = is_active
        c.password_hash = password_hash
        return c
    return _factory


@pytest.fixture
def make_contract():
    """Factory for Contract instances.

    Usage:
        def test_something(make_contract):
            c = make_contract(status=ContractStatus.SIGNED, remaining_amount=Decimal("0"))
    """
    def _factory(
        id=1,
        client_id=1,
        commercial_id=2,
        total_amount=Decimal("5000.00"),
        remaining_amount=Decimal("5000.00"),
        status=ContractStatus.DRAFT,
    ):
        c = Contract()
        c.id = id
        c.client_id = client_id
        c.commercial_id = commercial_id
        c.total_amount = total_amount
        c.remaining_amount = remaining_amount
        c.status = status
        return c
    return _factory


@pytest.fixture
def make_event():
    """Factory for Event instances.

    Usage:
        def test_something(make_event):
            e = make_event(support_id=3)
    """
    def _factory(
        id=1,
        contract_id=2,
        title="Test Event",
        start_date=None,
        end_date=None,
        support_id=None,
        is_cancelled=False,
    ):
        e = Event()
        e.id = id
        e.contract_id = contract_id
        e.title = title
        e.start_date = start_date or datetime(2025, 9, 1, 9, 0)
        e.end_date = end_date or datetime(2025, 9, 1, 17, 0)
        e.support_id = support_id
        e.is_cancelled = is_cancelled
        return e
    return _factory


@pytest.fixture
def make_client():
    """Factory for Client instances.

    Usage:
        def test_something(make_client):
            c = make_client(status=ClientStatus.ACTIVE)
    """
    def _factory(
        id=1,
        first_name="Jean",
        last_name="Durand",
        email="jean@company.com",
        commercial_id=2,
        status=ClientStatus.PROSPECT,
        contracts=None,
    ):
        c = Client()
        c.id = id
        c.first_name = first_name
        c.last_name = last_name
        c.email = email
        c.commercial_id = commercial_id
        c.status = status
        c.contracts = contracts if contracts is not None else []
        return c
    return _factory


# ── Named collaborator fixtures ───────────────────────────────────────────────

@pytest.fixture
def management_collaborator(make_collaborator):
    """An active Management collaborator."""
    return make_collaborator(
        id=1, first_name="Alice", last_name="Martin",
        email="alice@epicevents.com", role=RoleEnum.MANAGEMENT
    )


@pytest.fixture
def commercial_collaborator(make_collaborator):
    """An active Commercial collaborator."""
    return make_collaborator(
        id=2, first_name="Bob", last_name="Dupont",
        email="bob@epicevents.com", role=RoleEnum.COMMERCIAL
    )


@pytest.fixture
def support_collaborator(make_collaborator):
    """An active Support collaborator."""
    return make_collaborator(
        id=3, first_name="Carol", last_name="Leblanc",
        email="carol@epicevents.com", role=RoleEnum.SUPPORT
    )


@pytest.fixture
def inactive_collaborator(make_collaborator):
    """A deactivated collaborator — cannot log in or perform actions."""
    return make_collaborator(
        id=4, first_name="Dave", last_name="Ancien",
        email="dave@epicevents.com", role=RoleEnum.COMMERCIAL,
        is_active=False
    )


# ── Named client fixtures ─────────────────────────────────────────────────────

@pytest.fixture
def prospect_client(make_client):
    """A freshly created client — PROSPECT status, no contracts."""
    return make_client(id=1, status=ClientStatus.PROSPECT)


@pytest.fixture
def active_client(make_client):
    """A client with a signed contract — ACTIVE status."""
    return make_client(
        id=2, first_name="Marie", last_name="Leclerc",
        email="marie@company.com", status=ClientStatus.ACTIVE
    )


# ── Named contract fixtures ───────────────────────────────────────────────────

@pytest.fixture
def draft_contract(make_contract):
    """A contract in DRAFT status."""
    return make_contract(id=1, status=ContractStatus.DRAFT)


@pytest.fixture
def pending_contract(make_contract):
    """A contract in PENDING status — awaiting client signature."""
    return make_contract(id=7, status=ContractStatus.PENDING)


@pytest.fixture
def signed_contract(make_contract):
    """A contract in SIGNED status — events can be created against it."""
    return make_contract(
        id=2, status=ContractStatus.SIGNED,
        remaining_amount=Decimal("2500.00")
    )


@pytest.fixture
def completed_contract(make_contract):
    """A contract in COMPLETED status — fully paid and delivered."""
    return make_contract(
        id=3, status=ContractStatus.COMPLETED,
        remaining_amount=Decimal("0.00")
    )


@pytest.fixture
def cancelled_contract(make_contract):
    """A contract in CANCELLED status — no further actions possible."""
    return make_contract(
        id=4, status=ContractStatus.CANCELLED,
        total_amount=Decimal("3000.00"),
        remaining_amount=Decimal("3000.00")
    )


@pytest.fixture
def fully_paid_contract(make_contract):
    """A signed contract with zero remaining amount."""
    return make_contract(
        id=5, status=ContractStatus.SIGNED,
        total_amount=Decimal("4000.00"),
        remaining_amount=Decimal("0.00")
    )


@pytest.fixture
def unpaid_contract(make_contract):
    """A signed contract with remaining balance."""
    return make_contract(
        id=6, status=ContractStatus.SIGNED,
        total_amount=Decimal("4000.00"),
        remaining_amount=Decimal("1500.00")
    )


# ── Named event fixtures ──────────────────────────────────────────────────────

@pytest.fixture
def event_without_support(make_event):
    """An event with no support assigned."""
    return make_event(
        id=1, title="Annual Gala",
        start_date=datetime(2025, 9, 1, 18, 0),
        end_date=datetime(2025, 9, 1, 23, 0)
    )


@pytest.fixture
def event_with_support(make_event, support_collaborator):
    """An event with a support collaborator assigned."""
    return make_event(
        id=2, title="Product Launch",
        start_date=datetime(2025, 10, 15, 9, 0),
        end_date=datetime(2025, 10, 15, 17, 0),
        support_id=support_collaborator.id
    )


@pytest.fixture
def eight_hour_event(make_event):
    """An event with exactly 8 hours duration."""
    return make_event(
        id=3, title="Workshop",
        start_date=datetime(2025, 11, 1, 9, 0),
        end_date=datetime(2025, 11, 1, 17, 0)
    )


@pytest.fixture
def past_event(make_event):
    """An event that ended yesterday — is_past returns True."""
    return make_event(
        id=4, title="Past Conference",
        start_date=datetime.now(timezone.utc) - timedelta(days=2),
        end_date=datetime.now(timezone.utc) - timedelta(days=1)
    )


@pytest.fixture
def future_event(make_event):
    """An event starting tomorrow — is_past returns False."""
    return make_event(
        id=5, title="Upcoming Gala",
        start_date=datetime.now(timezone.utc) + timedelta(days=1),
        end_date=datetime.now(timezone.utc) + timedelta(days=2)
    )
