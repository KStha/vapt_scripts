#!/usr/bin/python3

"""Find all CIDRs of ASNs."""

import argparse
import sys
import re

from typing import Union
from ipaddress import ip_network
from ipaddress import IPv4Network
from ipaddress import IPv6Network
from ssl import PROTOCOL_TLS
from ssl import CERT_REQUIRED
from ssl import OP_NO_TLSv1
from ssl import OP_NO_TLSv1_1
from requests import session
from requests.adapters import HTTPAdapter
from urllib3.util import ssl_
from urllib3.poolmanager import PoolManager


# https://requests.readthedocs.io/en/latest/user/advanced/#example-specific-ssl-version
# https://hussainaliakbar.github.io/restricting-tls-version-and-cipher-suites-in-python-requests-and-testing-with-wireshark/
# https://stackoverflow.com/a/44432829
class TLSHTTPAdapter(HTTPAdapter):
    """Allow use of only TLSv2 or above."""

    def __init__(self, ssl_options=0, **kwargs):
        self.ssl_options = ssl_options
        super(__class__, self).__init__(**kwargs)

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
        "asn",
        type=str,
        action="extend",
        nargs="*",
        help="ASN Number of an Organization",
    )

    optional.add_argument(
        "--stdin",
        "-",
        action="store_true",
        help="Take ASN Number of Organization(s) from stdin",
    )

    optional.add_argument(
        "-h",
        "--help",
        action="help",
        default=argparse.SUPPRESS,
        help="Show this help message and exit",
    )

    return parser.parse_intermixed_args(argv)


def get_parent_cidr(sorted_cidr_list: list[str]) -> list[Union[IPv4Network | IPv6Network]]:
    """Get Parent CIDR from a list of sorted CIDRs."""
    unique_cidr: list[Union[IPv4Network | IPv6Network]] = []
    cidr_add: bool = True

    if sorted_cidr_list:
        previous_ip: Union[IPv4Network | IPv6Network] = ip_network(sorted_cidr_list[0])

        for ip_cidr in sorted_cidr_list:
            if cidr_add:
                unique_cidr.append(previous_ip)

            next_ip = ip_network(ip_cidr)

            try:
                if next_ip.subnet_of(previous_ip):
                    cidr_add = False
                    continue

                unique_cidr.append(next_ip)
                previous_ip = ip_network(ip_cidr)

            except TypeError:
                previous_ip = ip_network(next_ip)
                cidr_add = False

    return unique_cidr


def get_cidr_output(asn, http_session, adapter) -> str:
    """Get CIDRs of an ASN from RIPE."""
    cidr_list = []
    cidr_string = ""

    try:
        http_session.mount("https://", adapter)

        response = http_session.request(
            "GET",
            "https://stat.ripe.net/data/announced-prefixes/data.json?resource=AS"
            + str(asn),
            verify=True,
        )

        if response.status_code == 200:
            all_details = str(response.text)
            prefix_list = re.findall('"prefix": ".*"', all_details)

            for prefix in prefix_list:
                cidr_list.append(re.sub(r"\"prefix\": \"|\"$", "", prefix))

            cidr_list.sort()

            combined_cidr_list = get_parent_cidr(cidr_list)

            for combined_cidr in combined_cidr_list:
                cidr_string += str(combined_cidr) + "\n"

            cidr_string.strip().rstrip()

    except ConnectionError:
        print("Unable to connect to the server.")
        sys.exit(1)

    except KeyboardInterrupt:
        sys.exit()

    return cidr_string


def return_cidr(asn, http_session, adapter) -> str:
    """Return CIDRs obtained."""
    return_value: str = ""

    try:
        return_value = get_cidr_output(asn, http_session, adapter)

    except KeyboardInterrupt:
        return_value = "\n"

    return return_value


def output_cidr(asn_number_list, http_session, adapter) -> None:
    """Output CIDR values."""
    for asn in asn_number_list:
        print(return_cidr(asn, http_session, adapter), end="")


def main(argv: list[str]) -> None:
    """Start code execution."""
    args: argparse.Namespace = get_args(argv)

    http_session = session()
    adapter = TLSHTTPAdapter(OP_NO_TLSv1 | OP_NO_TLSv1_1)

    asns: list[str] = []
    asns_stdin: list[str] = []

    if args.asn:
        asns = args.asn

    if args.stdin:
        for asns_raw in sys.stdin:
            asn_bulk = asns_raw.split()

            for asn in asn_bulk:
                asns_stdin.append(asn.strip().rstrip())

        asns = asns_stdin + asns

    asns = [re.sub(r"^(AS)", "", asn, flags=re.IGNORECASE) for asn in asns]
    asns_set: set[str] = set(asns)
    asns = list(asns_set)

    output_cidr(asns, http_session, adapter)


if __name__ == "__main__":
    main(sys.argv[1:])
