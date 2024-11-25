from django.contrib import admin
from django import forms
from django.db.models import IntegerField
from django.db.models.functions import Cast, Substr, Length
from .models import Package, AllUser, UserPaymentLedger, UserRechargeHistory

# ------------To sort dropdown pkg field of allUser table in admin panel------------
class AllUserForm(forms.ModelForm):
    class Meta:
        model = AllUser
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Extract the numerical part from the beginning of the 'pkg_name' field and order the queryset
        self.fields['pkg'].queryset = Package.objects.annotate(numerical_part=Cast(Substr('pkg_name', 1, Length('pkg_name')), IntegerField())).order_by('numerical_part', 'pkg_name')

@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = ('id', 'pkg_name', 'description', 'price')
    search_fields = ('pkg_name', 'description')
    # ordering = ['-pkg_name']  # Ascending order by name (it does not work on lexicographical data)

    # To achieve ordering by pkg name on admin panel interface.
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Extract the numerical part from the beginning of the 'pkg_name' field
        numerical_part_expression = Substr('pkg_name', 1, Length('pkg_name'))
        return qs.annotate(numerical_part=Cast(numerical_part_expression, IntegerField())).order_by('numerical_part')

@admin.register(AllUser)
class AllUserAdmin(admin.ModelAdmin):
    form = AllUserForm  # for dropdown ordering in admin panel
    list_display = ('id', 'userid', 'name', 'contact', 'address', 'pkg', 'rechargedate', 'monthlyfees', 'balance', 'remarks')
    search_fields = ('name', 'userid')
    # list_filter = ('pkg',)

@admin.register(UserPaymentLedger)
class UserPaymentLedgerAdmin(admin.ModelAdmin):
    exclude = ('user_name',)
    list_display = ('id', 'user', 'user_name', 'paid_amount', 'payment_date', 'paid_by', 'received_by', 'remarks')
    search_fields = ('user_name', 'paid_by', 'received_by')
    # list_filter = ('payment_date',)

@admin.register(UserRechargeHistory)
class UserRechargeHistoryAdmin(admin.ModelAdmin):
    exclude = ('user_name','monthlyfees','package',)
    list_display = ('id', 'user', 'user_name', 'package', 'recharge_date', 'monthlyfees', 'remarks')
    search_fields = ('user_name', 'package', 'remarks')
    # list_filter = ('recharge_date', 'package')
