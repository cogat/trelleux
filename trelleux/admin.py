from django.contrib import admin
from djangosite.trelleux.models import *

class TrelloBoardAdmin(admin.ModelAdmin):
    list_display = ["board_realid", "timezone", "enabled", "client", "fail_count",]# "board_realid"]
    list_filter = ["enabled", "timezone"]
    actions = ['update_lists']
    readonly_fields = ['fail_count']

    def update_lists(self, request, queryset):
        for b in queryset:
            b.update_lists()
    update_lists.short_description = "Update lists"


admin.site.register(TrelloBoard, TrelloBoardAdmin)
admin.site.register(TrelloClient)
