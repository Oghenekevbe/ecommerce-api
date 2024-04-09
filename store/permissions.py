from django.contrib.auth.mixins import UserPassesTestMixin


# userpassestextmixins
class IsSellerMixin(UserPassesTestMixin):
    def test_func(self):
        return (
            hasattr(self.request.user, "seller") and self.request.user.seller.is_active
        )


class IsStaffMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff


class IsAdminMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser
