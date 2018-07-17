from django.contrib import admin
# from .models import agri
from .models import Owner
from .models import Area
from .models import Field, Pond, Forest

# Register your models here.

admin.site.register(Owner)
admin.site.register(Area)
admin.site.register(Field)
admin.site.register(Pond)
admin.site.register(Forest)