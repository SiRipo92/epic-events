"""
Role and status enumerations for Epic Events CRM.

Defines all enumeration types used across the domain:
    RoleEnum:       The three collaborator roles.
    ContractStatus: The lifecycle states of a contract.
    ClientStatus:   The lifecycle states of a client dossier.

All enums inherit from both str and enum.Enum so they serialise
correctly when stored in PostgreSQL via SAEnum, encoded in JWT
payloads, and displayed in Rich CLI output without needing to
call .value explicitly.
"""

import enum


class RoleEnum(str, enum.Enum):
    """The three operational roles for Epic Events collaborators.

    Values:
        MANAGEMENT: Full administrative access — collaborators,
                    all contracts, event assignment.
        COMMERCIAL: Client and contract management, event creation
                    scoped to own clients.
        SUPPORT:    Event execution and updates scoped to assigned
                    events only.
    """

    MANAGEMENT = "management"
    COMMERCIAL = "commercial"
    SUPPORT = "support"


class ContractStatus(str, enum.Enum):
    """Lifecycle states for a contract.

    Transitions:
        DRAFT → PENDING → SIGNED → COMPLETED
                        ↘ CANCELLED (from any active state)

    Values:
        DRAFT:     Being filled in by Management.
        PENDING:   Awaiting client signature.
        SIGNED:    Signed — events can now be created against it.
        COMPLETED: All amounts paid and event delivered. Dossier closed.
        CANCELLED: Cancelled — no further action possible.
                   Linked event is also cancelled by the service layer.
    """

    DRAFT = "draft"
    PENDING = "pending"
    SIGNED = "signed"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class ClientStatus(str, enum.Enum):
    """Lifecycle states for a client dossier.

    Transitions:
        PROSPECT → IN_NEGOTIATION → PENDING_SIGNATURE → ACTIVE
            → IN_SUPPORT → COMPLETED
        Any state → INACTIVE (client departs or requests RGPD deletion)

    Values:
        PROSPECT:           Client created. No contract yet.
                            Commercial collaborator responsible.
        IN_NEGOTIATION:     Contract being drafted by Management.
        PENDING_SIGNATURE:  Contract sent, awaiting client signature.
        ACTIVE:             Contract signed. Commercial role complete.
                            Management must create event and assign support.
        IN_SUPPORT:         Support collaborator assigned.
                            Event in preparation.
        COMPLETED:          Event delivered. Dossier closed.
        INACTIVE:           Client no longer active — departed or
                            RGPD deletion pending.
    """

    PROSPECT = "prospect"
    IN_NEGOTIATION = "in_negotiation"
    PENDING_SIGNATURE = "pending_signature"
    ACTIVE = "active"
    IN_SUPPORT = "in_support"
    COMPLETED = "completed"
    INACTIVE = "inactive"
