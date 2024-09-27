
from django.contrib import admin
from .models import UserProfile,Product


class PersonAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'email')

    # def my_name(self,obj):
    #     return 'Abdul'+ str(obj) 

class BbAdmin (admin.ModelAdmin) :
    actions = ('discount', )
    def discount (self, request, queryset) :
        f = UserProfile('first_name')
        for rec in queryset:
            rec.first_name =rec.first_name+'1'
            rec. save ()
            self.message_user (request, 'Действие выполнено')
    # discount.short_description - 'Уменьшить цену вдвое'

admin.site.register(UserProfile, BbAdmin)
admin.site.register(Product)

# class QuestionAdmin(admin.ModelAdmin):
#     list_display = ()