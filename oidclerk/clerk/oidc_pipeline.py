# pylint: disable=keyword-arg-before-vararg

def save_all_claims_as_extra_data(response, storage, social=None, *_args, **_kwargs):
    """Update user extra-data using data from provider."""
    if not social:
        return

    social.extra_data = response
    storage.user.changed(social)
