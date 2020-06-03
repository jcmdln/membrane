# noqa: E501

import re
import requests
import sys

domains: list = []

sources: list = [
    "http://winhelp2002.mvps.org/hosts.txt",
    "http://www.malwaredomainlist.com/hostslist/hosts.txt",
    "https://gitlab.com/ZeroDot1/CoinBlockerLists/raw/master/hosts",
    "https://gitlab.com/ZeroDot1/CoinBlockerLists/raw/master/hosts_browser",
    "https://gitlab.com/ZeroDot1/CoinBlockerLists/raw/master/hosts_optional",
    "https://mirror.cedia.org.ec/malwaredomains/justdomains",
    "https://pgl.yoyo.org/adservers/serverlist.php?hostformat=hosts&showintro=1&mimetype=plaintext",
    "https://raw.githubusercontent.com/AdAway/adaway.github.io/master/hosts.txt",
    "https://raw.githubusercontent.com/FadeMind/hosts.extras/master/UncheckyAds/hosts",
    "https://raw.githubusercontent.com/FadeMind/hosts.extras/master/add.2o7Net/hosts",
    "https://raw.githubusercontent.com/FadeMind/hosts.extras/master/add.Dead/hosts",
    "https://raw.githubusercontent.com/FadeMind/hosts.extras/master/add.Risk/hosts",
    "https://raw.githubusercontent.com/FadeMind/hosts.extras/master/add.Spam/hosts",
    "https://raw.githubusercontent.com/StevenBlack/hosts/master/alternates/gambling-porn-social/hosts",
    "https://raw.githubusercontent.com/lightswitch05/hosts/master/ads-and-tracking-extended.txt",
]


def cleanup(t: str) -> str:
    t = re.sub(r"^\s", "", t, flags=re.MULTILINE)
    t = re.sub(r"^#.*$", "", t, flags=re.MULTILINE)
    t = re.sub(r"#.*$", "", t, flags=re.MULTILINE)
    t = re.sub(r"^<.*$", "", t, flags=re.MULTILINE)
    t = re.sub(r"^<.*$", "", t, flags=re.MULTILINE)
    t = re.sub(r"^127.0.0.1\s", "", t, flags=re.MULTILINE)
    t = re.sub(r"^0.0.0.0\s", "", t, flags=re.MULTILINE)
    t = re.sub(r"^0.0.0.0$", "", t, flags=re.MULTILINE)
    t = re.sub(r"^.*localhost$", "", t, flags=re.MULTILINE)
    t = re.sub(r"^.*localdomain$", "", t, flags=re.MULTILINE)
    t = re.sub(r"^.*::.*$", "", t, flags=re.MULTILINE)
    t = re.sub(r"\r", "", t, flags=re.MULTILINE)
    t = re.sub(r"^\s+", "", t, flags=re.MULTILINE)
    t = re.sub(r"\s+$", "", t, flags=re.MULTILINE)
    t = re.sub(r"\t", "", t, flags=re.MULTILINE)
    t = re.sub(r"^$\n", "", t, flags=re.MULTILINE)

    return t


def main() -> None:
    tmp_list: dict = {}

    print("membrane: getting sources...")
    for source in sources:
        r = requests.get(source).text
        r = cleanup(r)

        # Writing to a temporary dict is way faster than attempting
        # to only add unique items to a list.
        for line in r.split("\n"):
            if "." in line:
                tmp_list[line] = ""

    domains = list(sorted(tmp_list))

    print("membrane: writing 'hosts.txt'...")
    with open("hosts.txt", "w") as f:
        for item in domains:
            f.write("0.0.0.0 %s\n" % item)

    tmp_list = {}
    for item in domains:
        item = ".".join(item.split(".")[-2:])
        tmp_list[item] = ""

    print("membrane: writing 'domains.txt'...")
    with open("domains.txt", "w") as f:
        for item in list(sorted(tmp_list)):
            f.write("%s\n" % item)

    sys.exit(0)


if __name__ == "__main__":
    main()
