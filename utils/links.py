from django.urls import reverse
from django.utils.safestring import mark_safe


def admin_link(obj):
    change_url = reverse(
        'admin:%s_%s_change' % (
            obj._meta.app_label,
            obj._meta.object_name.lower()
        ),
        args=(obj.id,)
    )
    return mark_safe(u'<a href="%s">%s</a>' % (change_url, obj))

