"""
Custom domain exceptions for Epic Events CRM.

All application-specific exceptions are defined here in one place.
Using domain-named exceptions rather than generic Python exceptions
makes error handling explicit and readable throughout the codebase.

Each exception maps to a specific business rule violation:
    AuthenticationError:    Login failed or session is missing/expired.
    PermissionError:        User lacks the required role or ownership.
    ContractNotSignedError: Event creation attempted on unsigned contract.
    NotYourClientError:     Commercial tried to modify another's client.
    NotYourEventError:      Support tried to modify an unassigned event.
    InactiveCollaboratorError: Deactivated account attempted an action.
    ReassignmentRequiredError: Collaborator has active records that must
                               be reassigned before deactivation.
"""


class AuthenticationError(Exception):
    """Raised when login fails or the session token is missing or expired."""
    pass


class PermissionError(Exception):
    """Raised when the current user lacks the required role or ownership.

    This is a domain exception that intentionally shadows Python's
    built-in PermissionError. It is aliased as CRMPermissionError
    when imported into other modules to avoid ambiguity.
    """
    pass


class ContractNotSignedError(Exception):
    """Raised when an event creation is attempted against an unsigned contract.

    A contract must have status SIGNED or COMPLETED before an event
    can be created against it.
    """
    pass


class NotYourClientError(Exception):
    """Raised when a Commercial collaborator attempts to modify a client
    that belongs to a different commercial.

    Enforces the ownership check: client.commercial_id == current_user.id
    """
    pass


class NotYourEventError(Exception):
    """Raised when a Support collaborator attempts to modify an event
    they are not assigned to.

    Enforces the ownership check: event.support_id == current_user.id
    """
    pass


class InactiveCollaboratorError(Exception):
    """Raised when a deactivated collaborator attempts to log in or
    perform any action in the system.
    """
    pass


class ReassignmentRequiredError(Exception):
    """Raised when a Management user attempts to deactivate a collaborator
    who still has active clients, open contracts, or assigned events.

    The error message should list exactly what needs to be reassigned
    before deactivation can proceed.
    """
    pass
