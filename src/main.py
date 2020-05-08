import re
import requests
import sys

domains: list = []

block_hosts: list = [
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
    "https://raw.githubusercontent.com/lightswitch05/hosts/master/ads-and-tracking-extended.txt"
]


def cleanup(t: str) -> str:
    t = re.sub("^\s", "", t, flags=re.MULTILINE)
    t = re.sub("^#.*$", "", t, flags=re.MULTILINE)
    t = re.sub("#.*$", "", t, flags=re.MULTILINE)
    t = re.sub("^<.*$", "", t, flags=re.MULTILINE)
    t = re.sub("^<.*$", "", t, flags=re.MULTILINE)
    t = re.sub("^127.0.0.1\s", "", t, flags=re.MULTILINE)
    t = re.sub("^0.0.0.0\s", "", t, flags=re.MULTILINE)
    t = re.sub("^0.0.0.0$", "", t, flags=re.MULTILINE)
    t = re.sub("^.*localhost$", "", t, flags=re.MULTILINE)
    t = re.sub("^.*localdomain$", "", t, flags=re.MULTILINE)
    t = re.sub("^.*::.*$", "", t, flags=re.MULTILINE)
    t = re.sub("\r", "", t, flags=re.MULTILINE)
    t = re.sub("^\s+", "", t, flags=re.MULTILINE)
    t = re.sub("\s+$", "", t, flags=re.MULTILINE)
    t = re.sub("\t", "", t, flags=re.MULTILINE)
    t = re.sub("^$\n", "", t, flags=re.MULTILINE)

    return t


def main() -> None:
    tmp_list: dict = {}

    print("membrane: getting sources...")
    for i in block_hosts:
        r = requests.get(i).text
        r = cleanup(r)

        # Writing to a temporary dict is way faster than attempting
        # to only add unique items to a list.
        for l in r.split("\n"):
            if "." in l:
                tmp_list[l] = ""

    # Convert tmp_list to an actual list
    domains = list(sorted(tmp_list))

    print("membrane: writing to 'hosts.txt'...")
    with open('hosts.txt', 'w') as f:
        for item in domains:
            f.write("0.0.0.0 %s\n" % item)

    sys.exit(0)


if __name__ == "__main__":
    main()
