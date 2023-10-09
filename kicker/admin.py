from django.contrib import admin

from kicker.models import Location, Player, Match

admin.site.register(Player)
admin.site.register(Match)


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    def get_form(self, request, obj=None, **kwargs):
        form = super(LocationAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields["admins"].required = False
        return form
