from django.db import migrations

from saleor.order.migrations.tasks.voucher_to_voucher_code_in_order import (
    set_voucher_to_voucher_code,
)


def set_voucher_to_voucher_code_in_order(apps, schema_editor):
    Order = apps.get_model("order", "Order")
    Voucher = apps.get_model("discount", "Voucher")
    VoucherCode = apps.get_model("discount", "VoucherCode")
    set_voucher_to_voucher_code(Order, Voucher, VoucherCode)


class Migration(migrations.Migration):
    dependencies = [
        ("discount", "0059_voucher_single_use"),
        ("order", "0176_order_voucher_code_add_index"),
    ]

    operations = [
        migrations.RunPython(
            set_voucher_to_voucher_code_in_order,
            migrations.RunPython.noop,
        ),
    ]
