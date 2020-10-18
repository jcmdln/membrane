import click
import re
import requests
import sys
from typing import Any, Dict, List

allowed: List[str] = [
    "duckduckgo.com",
    "google.com",
    "facebook.com",
    "github.com",
    "gitlab.com",
    "youtube.com",
]

sources: List[str] = [
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
    "https://someonewhocares.org/hosts/hosts",
]


def cleanup(t: str) -> str:
    """Cleanup a hosts list."""
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


@click.command()
def main() -> None:
    domains: Dict[str, Any] = {}

    print("membrane: getting sources...")
    for source in sources:
        r = requests.get(source).text
        r = cleanup(r)

        for line in r.split("\n"):
            if "." in line and line not in allowed:
                domains[line] = ""

    print("membrane: writing 'hosts.txt'...")
    with open("hosts.txt", "w") as f:
        for item in list(sorted(domains)):
            f.write("0.0.0.0 %s\n" % item)

    temp: Dict[str, Any] = {}
    for item in domains:
        item = ".".join(item.split(".")[-2:])
        if item not in allowed:
            temp[item] = ""
    domains = temp

    print("membrane: writing 'domains.txt'...")
    with open("domains.txt", "w") as f:
        for item in list(sorted(domains)):
            f.write("%s\n" % item)

    sys.exit(0)


if __name__ == "__main__":
    main()
