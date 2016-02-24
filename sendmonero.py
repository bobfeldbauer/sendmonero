#!/usr/bin/python
# Modified from https://github.com/moneroexamples/python-json-rpc, src/simplewallet_basic_rpc_call_04.py
# Some exchanges or service providers require specifying payment ids, but otherwise you usually want a random one.
# Example usage: sendmonero.py <destination address> <amount> [payment id]
# destination address and amount are required, payment id is optional and will be generated if it isn't provided.

import requests
import json
import os
import binascii
import sys

def main():
    # simple wallet is running on the localhost and port of 18082
    url = "http://127.0.0.1:18082/json_rpc"

    # standard json header
    headers = {'content-type': 'application/json'}

    destination_address = str(sys.argv[1])

    # amount of xmr to send
    amount = float(sys.argv[2])

    # cryptonote amount format is different then
    # that normally used by people.
    # thus the float amount must be changed to
    # something that cryptonote understands
    int_amount = int(get_amount(amount))

    # just to make sure that amount->coversion->back
    # gives the same amount as in the initial number
    assert amount == float(get_money(str(int_amount))), "Amount conversion failed"

    # send specified xmr amount to the given destination_address
    recipents = [{"address": destination_address,
                  "amount": int_amount}]

    # using given mixin
    mixin = 1

    # get some random payment_id
    if len(sys.argv) == 4:
        payment_id = sys.argv[3]
    else:
        payment_id = get_payment_id()
    # simplewallet' procedure/method to call
    rpc_input = {
        "method": "transfer",
        "params": {"destinations": recipents,
                   "mixin": mixin,
                   "payment_id" : payment_id}
    }

    # add standard rpc values
    rpc_input.update({"jsonrpc": "2.0", "id": "0"})

    # execute the rpc request
    response = requests.post(
         url,
         data=json.dumps(rpc_input),
         headers=headers)

    # print the payment_id
    print("#payment_id: ", payment_id)

    # pretty print json output
    print(json.dumps(response.json(), indent=4))


def get_amount(amount):
    """encode amount (float number) to the cryptonote format. Hope its correct.

    Based on C++ code:
    https://github.com/monero-project/bitmonero/blob/master/src/cryptonote_core/cryptonote_format_utils.cpp#L211
    """

    CRYPTONOTE_DISPLAY_DECIMAL_POINT = 12

    str_amount = str(amount)

    fraction_size = 0

    if '.' in str_amount:

        point_index = str_amount.index('.')

        fraction_size = len(str_amount) - point_index - 1

        while fraction_size < CRYPTONOTE_DISPLAY_DECIMAL_POINT and '0' == str_amount[-1]:
            print(44)
            str_amount = str_amount[:-1]
            fraction_size = fraction_size - 1

        if CRYPTONOTE_DISPLAY_DECIMAL_POINT < fraction_size:
            return False

        str_amount = str_amount[:point_index] + str_amount[point_index+1:]

    if not str_amount:
        return False

    if fraction_size < CRYPTONOTE_DISPLAY_DECIMAL_POINT:
        str_amount = str_amount + '0'*(CRYPTONOTE_DISPLAY_DECIMAL_POINT - fraction_size)

    return str_amount


def get_money(amount):
    """decode cryptonote amount format to user friendly format. Hope its correct.

    Based on C++ code:
    https://github.com/monero-project/bitmonero/blob/master/src/cryptonote_core/cryptonote_format_utils.cpp#L751
    """

    CRYPTONOTE_DISPLAY_DECIMAL_POINT = 12

    s = amount

    if len(s) < CRYPTONOTE_DISPLAY_DECIMAL_POINT + 1:
        # add some trailing zeros, if needed, to have constant width
        s = '0' * (CRYPTONOTE_DISPLAY_DECIMAL_POINT + 1 - len(s)) + s

    idx = len(s) - CRYPTONOTE_DISPLAY_DECIMAL_POINT

    s = s[0:idx] + "." + s[idx:]

    return s


def get_payment_id():
    """generate random payment_id

    generate some random payment_id for the
    transactions

    payment_id is 32 bytes (64 hexadecimal characters)
    thus we first generate 32 random byte array
    which is then change to string representation, since
    json will not not what to do with the byte array.
    """
    payment_id = os.urandom(32).encode('hex')
    return payment_id


if __name__ == "__main__":
    main()
