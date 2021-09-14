import math
from decimal import Decimal, ROUND_HALF_UP

def dms2deg(dms):
    # 度分秒から度への変換
    h = dms[0]
    m = dms[1]
    s = dms[2]
    deg = Decimal(str(h + (m / 60) + (s / 3600))).quantize(Decimal('0.0001'), rounding=ROUND_HALF_UP)
    return deg

def deg2dms(deg):
    # 度から度分秒への変換
    h = math.modf(deg)[1]
    m = math.modf(math.modf(deg)[0] * 60)[1]
    s = math.modf(math.modf(deg)[0] * 60)[0]*60
    if Decimal(str(s)).quantize(Decimal('0'), rounding=ROUND_HALF_UP) == 60:
        s = 0
        m = m + 1
    if Decimal(str(m)).quantize(Decimal('0'), rounding=ROUND_HALF_UP) == 60:
        m = 0
        h = h + 1
    dms_tap = (int(Decimal(h).quantize(Decimal('0'), rounding=ROUND_HALF_UP)),
                int(Decimal(m).quantize(Decimal('0'), rounding=ROUND_HALF_UP)),
                int(Decimal(s).quantize(Decimal('0'), rounding=ROUND_HALF_UP)))
    return dms_tap
