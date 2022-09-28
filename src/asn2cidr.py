#!/usr/bin/python3

"""Find All CIDRs in an ASN."""

import argparse
import sys
import re

from ipaddress import ip_network
from ssl import PROTOCOL_TLS
from ssl import CERT_REQUIRED
from ssl import OP_NO_TLSv1
from ssl import OP_NO_TLSv1_1
from requests import get
from requests import session
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util import ssl_
from requests.packages.urllib3.poolmanager import PoolManager


# https://hussainaliakbar.github.io/restricting-tls-version-and-cipher-suites-in-python-requests-and-testing-with-wireshark/
# https://stackoverflow.com/a/44432829
class TLSv2HttpAdapter(HTTPAdapter):
    """Allow use of only TLSv2 or above."""

    def __init__(self, ssl_options=0, **kwargs):
        self.ssl_options = ssl_options
        super(TLSv2HttpAdapter, self).__init__(**kwargs)

    def init_poolmanager(self, *pool_args, **pool_kwargs):
        ctx = ssl_.create_urllib3_context(
            PROTOCOL_TLS, cert_reqs=CERT_REQUIRED, options=self.ssl_options
        )

        self.poolmanager = PoolManager(*pool_args, ssl_context=ctx, **pool_kwargs)


def get_args(argv: list[str]) -> argparse.Namespace:
    """Parse arguments and return them."""
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        description="Automatically format Python scripts",
        add_help=False,
        allow_abbrev=False,
    )

    optional = parser.add_argument_group("optional arguments")

    parser.add_argument(
        "ASN",
        type=str,
        action="extend",
        nargs="+",
        help="ASN Number of an Organization",
    )

    optional.add_argument(
        "-h",
        "--help",
        action="help",
        default=argparse.SUPPRESS,
        help="Show this help message and exit",
    )

    return parser.parse_intermixed_args(argv)


def get_parent_cidr(sorted_cidr_list: list[str]):
    """"""
    unique_cidr = []
    cidr_add = True

    if sorted_cidr_list:
        previous_ip = ip_network(sorted_cidr_list[0])

        for ip in sorted_cidr_list:
            if cidr_add:
                unique_cidr.append(previous_ip)

            next_ip = ip_network(ip)

            try:
                if next_ip.subnet_of(previous_ip):
                    cidr_add = False
                    continue
                else:
                    unique_cidr.append(next_ip)
                    previous_ip = ip_network(ip)

            except TypeError:
                previous_ip = ip_network(next_ip)
                cidr_add = False

    return unique_cidr


def get_cidr_output(asn):
    """"""
    cidr_list = []
    cidr_string = ""
    return_value = ""

    response = session.request(
        "GET",
        "https://stat.ripe.net/data/announced-prefixes/data.json?resource=AS"
        + str(asn),
        verify=True,
    )

    if response.status_code == 200:
        all_details = str(response.text)
        prefix_list = re.findall("\"prefix\": \".*\"", all_details)

        for prefix in prefix_list:
            cidr_list.append(re.sub(r"\"prefix\": \"|\"$", "", prefix))

        cidr_list.sort()

        combined_cidr_list = get_parent_cidr(cidr_list)

        for combined_cidr in combined_cidr_list:
            cidr_string += str(combined_cidr) + "\n"

        cidr_string.strip().rstrip()

    return cidr_string


def return_cidr(asn):
    """"""
    try:
        return_value = get_cidr_output(asn)

    except KeyboardInterrupt:
        return_value = "\n"

    return return_value


def output_cidr(asn_number_list):
    """"""
    for asn in asn_number_list:
        print(return_cidr(asn), end="")


def main(argv: list[str]) -> None:
    """Start code execution."""
    args: argparse.Namespace = get_args(argv)

    if args.ASN:
        asns: list[str] = args.ASN

    output_cidr(asns)


if __name__ == "__main__":
    session = session()
    adapter = TLSv2HttpAdapter(OP_NO_TLSv1 | OP_NO_TLSv1_1)
    session.mount("https://", adapter)

    main(sys.argv[1:])
