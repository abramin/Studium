"""Authentication placeholders and helpers."""


def get_current_user_id() -> str:
    """Placeholder for future OIDC integration.

    Returns a fixed user ID for local development to simplify wiring in future
    authentication without changing the data model.
    """

    return "local-dev"
