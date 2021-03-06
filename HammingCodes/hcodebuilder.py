import numpy as np
from FFPoly import FFPoly, pol_to_string, string_to_pol, MODULATOR
import json
from time import time

Mparam = 3
Qparam = 2
assert Mparam > 1

def int_to_pol(integer, fieldcardinal):
    max_exp = 0
    scale = fieldcardinal**max_exp
    while scale <= integer :
        max_exp += 1
        scale = fieldcardinal**max_exp

    coeffs = np.zeros((scale))
    intcopy = integer
    while intcopy > 0:
        max_exp -= 1
        scale = fieldcardinal**max_exp
        coeffs[max_exp] = intcopy // scale
        intcopy -= (intcopy // scale) * scale
    return FFPoly(coeffs, fieldcardinal)

def find_hamming_gens(m=Mparam, q=Qparam):
    """
    find_hamming_gens function
    Args :
      m, an integer, parameter for Hamming Codes
      q, a prime, is the cardinal of the finite field you want to use
    Returns :
      generators, list of generators polynomials
      checkpols, list of check polynomials
    """
    assert m < 10
    n, k = int((q**m - 1) / (q - 1)), int((q**m - 1) / (q - 1) - m)
    print("computing generators for Hamming code N={} | K={} | Q={}".format(n, k, q))
    modulator = MODULATOR(n, q)

    generators, checkpols = [], []

    for i in range(q**m, q**(m+1)):
        testpol = int_to_pol(i, q)
        quot, rem = modulator / testpol
        # print(str(rem))
        if rem == FFPoly(np.array([0]), q):
            generators.append(testpol)
            checkpols.append(quot)
    return generators, checkpols

def store(MQparams=[(3,2)]):
    """
    store function
    Args :
      MQparams is a list of tuples. each tuple has 2 coordinates, M an integer and Q a prime
    Returns :
      Nothing. Dumps data in a json file
    """
    data = []
    for param in MQparams:
        m, q = param[0], param[1]
        temp = dict(q=q, m=m, pols=[])
        gen, check = find_hamming_gens(m=m, q=q)
        for i in range(len(gen)):
            temp["pols"].append(dict(generator=pol_to_string(gen[i], q),
                                     checkpol=pol_to_string(check[i], q)))
        data.append(temp)

    with open('hammingpolynomials.json', 'w') as jsonfile:
        jsonfile.write(json.dumps(dict(data=data),
                                  indent=4))
    print("storing finished !")

if __name__=='__main__':
    # print(str(int_to_pol(15,2)))
    inittime = time()
    generators, checkpols = find_hamming_gens(m=2, q=3)
    for gen in generators:
        print(str(gen))
    store([(2,2),(3,2),(4,2),(5,2),(6,2),(7,2),(8,2),(3,3),(2,3)])
    print("the end ! time needed : {}".format(time() - inittime))
