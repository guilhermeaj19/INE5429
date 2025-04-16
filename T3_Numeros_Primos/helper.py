def dec2bin(n):
    if n > 1:
        return str(n % 2) + dec2bin(n//2)
    return str(n % 2)
