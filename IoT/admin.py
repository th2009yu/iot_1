from django.contrib import admin
from .models import Owner
from .models import Status
from .models import Area
from .models import RaspberryPi
from .models import KindOfArduino
from .models import Arduino
from .models import Agri

# Register your models here.
admin.site.register(Owner)
admin.site.register(Area)
admin.site.register(Status)
admin.site.register(RaspberryPi)
admin.site.register(KindOfArduino)
admin.site.register(Arduino)
admin.site.register(Agri)
