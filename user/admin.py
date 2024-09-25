from django.contrib import admin
from .models import User, Questions, Contactus, tech_test_model, User_Details, ForceSignout_User, Job

# Register your models here.
admin.site.register(User)
admin.site.register(Questions)
admin.site.register(Contactus)
admin.site.register(tech_test_model)
admin.site.register(User_Details)
admin.site.register(ForceSignout_User)
admin.site.register(Job)




