from shop.tax import vat


def test_vat_on_round_amount():
    assert vat(10000) == 2200


def test_vat_rounds_half_up():
    # 1025 * 0.22 = 225.5 -> 226
    assert vat(1025) == 226


def test_vat_rounds_down_below_half():
    # 1005 * 0.22 = 221.1 -> 221
    assert vat(1005) == 221
