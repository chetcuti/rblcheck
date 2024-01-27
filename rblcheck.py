#!/usr/bin/env python3
"""
Author: Greg Chetcuti <greg@chetcuti.com>
Date: 2022-11-14
Purpose: Real-time Blackhole List Checker (rblcheck.py)
"""

import dns.resolver as dns
import socket


# =============================================================================
# Main                                                                     Main
# ----------------------------------------------------------
def main():

    check_domains = get_file_contents("check.domains")
    check_ips = get_file_contents("check.ips")
    rbls_domains = get_file_contents("rbls.domains")
    rbls_ips = get_file_contents("rbls.ips")

    check_all_domains(check_domains, rbls_domains)
    check_all_ips(check_ips, rbls_ips)


# =============================================================================
# Functions                                                           Functions
# ----------------------------------------------------------
def get_file_contents(filename):

    with open(filename) as file:
        file_contents = file.read().splitlines()

    return [x for x in file_contents if not x.startswith("#") if x != ""]


def check_all_ips(ips, rbls_ips):

    for ip in ips:

        if check_ip(ip, rbls_ips) == 1:
            print("*** " + ip + " has issues ***")


def check_ip(ip, rbls_ips):

    for ip_rbl in rbls_ips:

        try:

            socket.gethostbyname(get_full_hostname(ip, ip_rbl))
            return 1

        except Exception:

            pass

    return 0


def check_all_domains(domains, rbls_domains):

    for domain in domains:

        if check_domain(domain, rbls_domains) == 1:
            print("*** " + domain + " has issues ***")


def check_domain(domain, rbls_domains):

    for domain_rbl in rbls_domains:

        try:

            dns.resolve(domain + "." + domain_rbl, "A")
            return 1

        except Exception:

            pass

    return 0


def get_full_hostname(ip, rbl):
    return ".".join(ip.split(".")[::-1]) + "." + rbl


# ----------------------------------------------------------
if __name__ == "__main__":
    main()

