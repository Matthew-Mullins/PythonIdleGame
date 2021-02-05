
def truncate_value(value):
    THOUSAND        = 10 ** 3
    MILLION         = 10 ** 6
    BILLION         = 10 ** 9
    TRILLION        = 10 ** 12
    QUADRILLION     = 10 ** 15
    QUINTILLION     = 10 ** 18
    SEXTILLION      = 10 ** 21
    SEPTILLION      = 10 ** 24
    OCTILLION       = 10 ** 27
    NONILLION       = 10 ** 30
    DECILLION       = 10 ** 33

    new_val = value
    suffix = ''
    if value < THOUSAND:
        new_val = value
        suffix = '  '
    elif value < MILLION:
        new_val /= float(THOUSAND)
        suffix = 'THOUSAND'
    elif value < BILLION:
        new_val /= float(MILLION)
        suffix = 'MILLION'
    elif value < TRILLION:
        new_val /= float(BILLION)
        suffix = 'BILLION'
    elif value < QUADRILLION:
        new_val /= float(TRILLION)
        suffix = 'TRILLION'
    elif value < QUINTILLION:
        new_val /= float(QUADRILLION)
        suffix = 'QUADRILLION'
    elif value < SEXTILLION:
        new_val /= float(QUINTILLION)
        suffix = 'QUINTILLION'
    elif value < SEPTILLION:
        new_val /= float(SEXTILLION)
        suffix = 'SEXTILLION'
    elif value < OCTILLION:
        new_val /= float(SEPTILLION)
        suffix = 'SEPTILLION'
    elif value < NONILLION:
        new_val /= float(OCTILLION)
        suffix = 'OCTILLION'
    elif value < DECILLION:
        new_val /= float(NONILLION)
        suffix = 'NONILLION'
    else:
        new_val /= float(DECILLION)
        suffix = 'DECILLION'
    return (new_val, suffix)