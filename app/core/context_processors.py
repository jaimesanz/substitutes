def school_membership(request):
    """Expose the current school user's active membership to all templates."""
    membership = None
    user = getattr(request, "user", None)
    if user and user.is_authenticated and getattr(user, "role", None) == "school":
        membership = user.school_memberships.select_related("school").first()
    return {"current_membership": membership}
