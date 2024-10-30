import pytest
from rest_framework.exceptions import ValidationError

from electronics.validators import validate_admin_role, validate_supplier_role


@pytest.mark.django_db
def test_validate_admin_role():
    with pytest.raises(ValidationError):
        validate_admin_role("admin")
