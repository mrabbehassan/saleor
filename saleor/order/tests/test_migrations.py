import pytest
from django.apps import apps
from mock import patch

from saleor.order.migrations.tasks.voucher_to_voucher_code_in_order import (
    set_voucher_to_voucher_code,
)


@pytest.mark.django_db
def test_set_voucher_to_voucher_code_in_order(draft_order_list):
    Order = apps.get_model("order", "Order")
    Voucher = apps.get_model("discount", "Voucher")
    VoucherCode = apps.get_model("discount", "VoucherCode")

    order, order_1, order_2 = draft_order_list

    vouchers = []
    for i in range(3):
        voucher = Voucher.objects.create()
        vouchers.append(voucher)
        VoucherCode.objects.create(code=f"Voucher code {i}", voucher=voucher)

    voucher_1, voucher_2, voucher_3 = vouchers

    order.voucher = voucher_1
    order.save()
    order_1.voucher = voucher_2
    order_1.save()
    order_2.voucher = voucher_3
    order_2.save()

    assert order.voucher_code is None

    with patch(
        "saleor.order.migrations.tasks.voucher_to_voucher_code_in_order.BATCH_SIZE", 2
    ):
        set_voucher_to_voucher_code(Order, Voucher, VoucherCode)

    order.refresh_from_db()
    order_1.refresh_from_db()
    order_2.refresh_from_db()
    assert order.voucher_code is not None
    assert order_1.voucher_code is not None
    assert order_2.voucher_code is not None
    assert order.voucher_code.code == "Voucher code 0"
    assert order_1.voucher_code.code == "Voucher code 1"
    assert order_2.voucher_code.code == "Voucher code 2"
