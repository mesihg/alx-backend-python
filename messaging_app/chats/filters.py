import django_filters
from .models import Message, User


class MessageFilter(django_filters.FilterSet):
    """
    Filter message with support for:
    - Filtering by sender ID or username
    - Filtering by date range
    """

    sender = django_filters.ModelChoiceFilter(
        field_name="sender",
        queryset=User.objects.all(),
        label="Sender (ID or username)",
        method="filter_sender"
    )
    start_date = django_filters.DateTimeFilter(
        field_name="sent_at",
        lookup_expr="gte",
        label="Sent after (YYYY-MM-DD HH:MM:SS)",
    )
    end_date = django_filters.DateTimeFilter(
        field_name="sent_at",
        lookup_expr="lte",
        label="Sent before (YYYY-MM-DD HH:MM:SS)"
    )
    search = django_filters.CharFilter(
        field_name="message_body",
        lookup_expr="icontains",
        label="Search in messages",
    )

    class Meta:
        model = Message
        fields = [
            "sender",
            "start_date",
            "end_date",
            "search"
        ]

    def filter_sender(self, queryset, name, value):
        if not value:
            return queryset
        try:
            sender_id = int(value)
            return queryset.filter(sender__id=sender_id)
        except (ValueError, TypeError):
            return queryset.filter(sender__username=str(value))
