from django.db.models import Exists, OuterRef

BATCH_SIZE = 1000


def set_voucher_to_voucher_code(
    Order,
    Voucher,
    VoucherCode,
) -> None:
    orders = Order.objects.filter(voucher_code__isnull=True).order_by("pk")[:BATCH_SIZE]
    if ids := list(orders.values_list("pk", flat=True)):
        qs = Order.objects.filter(pk__in=ids)
        set_voucher_code(Order, Voucher, VoucherCode, qs)
        set_voucher_to_voucher_code(Order, Voucher, VoucherCode)


def set_voucher_code(
    Order,
    Voucher,
    VoucherCode,
    orders,
) -> None:
    voucher_id_to_code_map = get_voucher_id_to_code_map(Voucher, VoucherCode, orders)
    orders_list = []
    for order in orders:
        code = voucher_id_to_code_map[order.voucher_id]
        order.voucher_code = code
        orders_list.append(order)
    Order.objects.bulk_update(orders_list, ["voucher_code"])


def get_voucher_id_to_code_map(
    Voucher,
    VoucherCode,
    orders,
) -> None:
    voucher_id_to_code_map = {}
    vouchers = Voucher.objects.filter(Exists(orders.filter(voucher_id=OuterRef("pk"))))
    codes = VoucherCode.objects.filter(
        Exists(vouchers.filter(id=OuterRef("voucher_id")))
    )
    for code in codes:
        voucher_id_to_code_map[code.voucher_id] = code

    return voucher_id_to_code_map
