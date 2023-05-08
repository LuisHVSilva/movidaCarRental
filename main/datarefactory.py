def str_to_float(value):
    try:
        val = value.replace(",", ".")
        return float(val)
    except():
        return 0


