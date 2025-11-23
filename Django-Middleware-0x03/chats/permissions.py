from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Allows access to SAFE methods for everyone.
    For unsafe methods, the user must be either:
    - the sender of the object, or
    - a participant on the object
    """

    def has_object_permission(self, request, view, obj) -> bool:  # type: ignore
        if request.method in permissions.SAFE_METHODS:
            return True
        user = request.user
        participants = getattr(obj, "participants", None)
        if getattr(obj, "sender", None) == user:
            return True
        if participants is not None:
            return participants.filter(id=user.id).exists()

        return False


class IsParticipantOfConversation(permissions.BasePermission):
    """
    User must be authenticated and a participant 
    of the conversation or related conversation object.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj) -> bool:  # type: ignore
        user = request.user
        participants = getattr(obj, "participants", None)
        conversation = getattr(obj, "conversation", None)

        if request.method in permissions.SAFE_METHODS:
            if participants:
                return participants.filter(id=user.id).exists()
            if conversation:
                return obj.conversation.participants.filter(id=user.id).exists()
            return False
        if request.method == "POST":
            if conversation:
                return obj.conversation.participants.filter(id=user.id).exists()
            if participants:
                return participants.filter(id=user.id).exists()
            return False
        if request.method in ["PUT", "PATCH", "DELETE"]:
            if conversation:
                return obj.conversation.participants.filter(id=user.id).exists()
            if participants:
                return participants.filter(id=user.id).exists()
            return False
        return False


class IsMessageOwnerOrReadOnly(permissions.BasePermission):
    """
    Safe Method: user must be part of the conversation.
    Unsafe Method: user must be the message sender
    """

    def has_object_permission(self, request, view, obj) -> bool:  # type: ignore
        user = request.user
        if request.method in permissions.SAFE_METHODS:
            return obj.conversation.participants.filter(id=user.id).exists()

        if request.method == "POST":
            return obj.conversation.participants.filter(id=user.id).exists()
        if request.method in ["PUT", "PATCH", "DELETE"]:
            return obj.sender == user
        return False
