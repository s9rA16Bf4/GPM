#!/bin/env python
try:
    from github import Github
except ImportError:
    print("You need to have pygithub installed!")
    exit()

from argparse import ArgumentParser
from os import system

def search(githubObject,term, limit, user=None, language=None, printResult=True):
    QUERY = f"{term}"
    FOUND_RESULTS = []
    if (user != None):
        QUERY += f"+user:{user}"
    if (language != None):
        QUERY += f"+language:{language}"

    rate_limit = githubObject.get_rate_limit()
    rate = rate_limit.search
    if (rate.remaining == 0):
        print(f"You have exhausted the amount of calls you can make [0/{rate.limit}] Please wait {rate.reset} before trying again")
        exit()
    else:
        repos = githubObject.search_repositories(QUERY)
    print(f"[!] Found {repos.totalCount} repo(s) matching does requirments")
    print(f"[~] Limit {limit}")
    try:
        for i,n in enumerate(repos):
            if (i <= int(limit)):
                if (printResult):
                    print(f"({i}) {n.name}\n\tAUTHOR -> {n.clone_url.split('/')[3]}\n\tURL -> {n.clone_url}\n\tLANG -> {n.language}")
                FOUND_RESULTS.append(n)
            else:
                break
    except KeyboardInterrupt:
        pass
    return FOUND_RESULTS

def install(githubObject, term, limit, user=None, language=None, directLink=False):
    if (directLink == False):
        FOUND_RESULTS = search(githubObject, term, limit, user, language, False)
        for n in FOUND_RESULTS:
            if (term.lower() in n.name.lower() or n.name.lower() in term.lower()):
                print(f"""*** Repo ***
NAME -> {n.name}
AUTHOR -> {n.clone_url.split('/')[3]}
LANG -> {n.language}
URL -> {n.clone_url}
                """)
                userInput = input("[?] Is this correct? [y/n] ")
                if (userInput.lower() == "y"):
                    term = n.clone_url
                    directLink = True
                    break
    if (directLink):
        print("[!] Cloning Repo!")
        system(f"git clone {term}")
    print("[!] Done")

if __name__ == "__main__":
    githubObject = Github("INSERT YOUR PAT HERE") # This will allow us to communicate with the github servers
    parser = ArgumentParser()
    parser.add_argument("--search", "-s", help="Searches github for a repo with the same name as provided")
    parser.add_argument("--install", "-i", help="Downloads the repo with the same name as provided")
    parser.add_argument("--user", help="Used to indicate which user you are after. Available with the --search flag")
    parser.add_argument("--language", help="Used to indicate which language you are after. Available with the --search flag")
    parser.add_argument("--limit", default=100, type=int, help="How many results should be shown when searching/installing? [DEFAULT:100]")
    parser.add_argument("--direct_link", action="store_true", help="Used to indicate that what you're providing is a direct link to a repo. Only usable with the --install flag")
    args = parser.parse_args()

    if (args.search):
        search(githubObject, args.search, args.limit, args.user, args.language)
    elif (args.install):
        install(githubObject, args.install, args.limit, args.user, args.language, args.direct_link)
