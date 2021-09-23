import ctypes
import os.path

_PATH = os.path.dirname(os.path.abspath(__file__))

_math_lib = ctypes.CDLL(f'{_PATH}\\math.dll')


def hcf(*integers: int):
    """
    NOTE: is slightly faster with a sorted bunch of numbers, but can be omitted for small and few numbers.

    :param integers: list of integers
    :return: highest common factor of the integers
    """
    # return _math_lib.hcf(ctypes.c_ulonglong(integers[0]), ctypes.c_ulonglong(integers[1]))
    hcf_ = integers[0]
    for num in integers[1:]:
        while num:
            hcf_, num = num, hcf_ % num
    return hcf_


def lcm(*integers: int):
    """
    :param integers: list of integers
    :return: lowest common multiple of the integers
    """
    lcm_ = integers[0]
    for num in integers[1:]:
        hcf_ = hcf(lcm_, num)
        lcm_ = hcf_ * (lcm_ // hcf_) * (num // hcf_)
    return lcm_


def is_prime(number):
    """
    :param number: number to perform the prime check
    :return: True if the number is a prime else False
    """
    if number < 18446744073709551615:
        return not not _math_lib.is_prime(ctypes.c_ulonglong(number))  # not not is faster than bool

    if number % 2 == 0:
        return False
    for divisor in range(3, int(number ** 0.5) + 1, 2):
        if number % divisor == 0:
            return False
    return True


if __name__ == '__main__':
    from time import perf_counter

    numbers = [1234 * x for x in range(1000, 0, -1)]

    start = perf_counter()

    assert hcf(*numbers) == 1234
    assert lcm(*numbers) == 8797019748936724827607318048151412784104754835567192011917770457084435924075091590353932083461717538249059786202155866537017645859444325416308884819312531743694854888709042616708980628486490416131989046114414294845698920521762927946244403991304561809658910629700052735682753336399729124632868871060482125417295717171296084400129355103100364719040675613984011601326679009885010590403742659318254123908648360342359788109271449598743680000

    assert is_prime(10000000002065383)
    assert is_prime(10000000002065387) is False
    assert is_prime(18446744073709551616) is False

    print(f"Time: {(perf_counter() - start) * 1000}ms")
