from enum import Flag
import os
import sys
import time
from threading import Thread

firstRun = False

try:
    import requests
except ModuleNotFoundError as e:
    print(e.msg)
    if input("Do you want to install 'requests'? (y/n): ") == "y":
        os.system("pip3 install requests")
        firstRun = True
    else:
        print("Exiting...")
        sys.exit()

try:
    from bs4 import BeautifulSoup
except ModuleNotFoundError as e:
    print(e.msg)
    if input("Do you want to install 'BeautifulSoup'? (y/n): ") == "y":
        os.system("pip3 install beautifulsoup4")
        firstRun = True
    else:
        print("Exiting... ")
        sys.exit()

if firstRun:
    os.system("clear")
    print("!! YOU ARE RUNNING THIS SCRIPT FOR THE FIRST TIIME !!")
    print("!! SO, WE HAD TO INSTALL SOME MISSING MODULES !!")
    print("!! THEREFORE, YOU MUST RESTART THE SCRIPT !!")
    print("!! EXITING... ")
    sys.exit()

st = time.time()


class LazyDict:
    global st

    def __init__(self, word) -> None:
        self.word = word

        self.EDEF = f"https://www.wordhippo.com/what-is/another-word-for/{self.word}.html"
        self.BDEF = f"https://www.bdword.com/english-to-bengali-meaning-{self.word}"

        self.NOUN = f"https://www.wordhippo.com/what-is/the-noun-for/{self.word}.html"
        self.ADJ = f"https://www.wordhippo.com/what-is/the-adjective-for/{self.word}.html"
        self.ADV = f"https://www.wordhippo.com/what-is/the-adverb-for/{self.word}.html"
        self.VRB = f"https://www.wordhippo.com/what-is/the-verb-for/{self.word}.html"

        self.SYNM = f"https://www.wordhippo.com/what-is/another-word-for/{self.word}.html"
        self.ANTNM = f"https://www.wordhippo.com/what-is/the-opposite-of/{self.word}.html"

        self.en_def = str()
        self.bn_def = str()
        self.n = list()
        self.adj = list()
        self.adv = list()
        self.vrb = list()
        self.snm = list()
        self.antnm = list()

    def getPage(self, url):
        return BeautifulSoup(requests.get(url).content, features="html.parser")

    def getEnglishDefination(self, n):
        soup = self.getPage(self.EDEF)
        definations = soup.find_all("div", class_="tabdesc")
        self.en_def = definations[0].text if definations else ["Nothing"]

    def getBanglaDefination(self, n):
        soup = self.getPage(self.BDEF)
        defination = soup.find_all("div", class_="align_text2")
        self.bn_def = defination[0].text if defination else ["Nothing"]

    def getNoun(self, amount):
        soup = self.getPage(self.NOUN)
        nouns = soup.find_all("div", class_="defv2wordtype", limit=amount)
        self.n = [noun.text for noun in nouns] if len(nouns) > 0 else [
            "Nothing"]

    def getAdjective(self, amount):
        adjPage = self.getPage(self.ADJ)
        adjs = adjPage.find_all("div", class_="defv2wordtype", limit=amount)
        self.adj = [adj.text for adj in adjs] if len(adjs) > 0 else ["Nothing"]

    def getAdverb(self, amount):
        advPage = self.getPage(self.ADV)
        advs = advPage.find_all("div", class_="defv2wordtype", limit=amount)
        self.adv = [adv.text for adv in advs] if len(advs) > 0 else ["Nothing"]

    def getVerb(self, amount):
        vrbPage = self.getPage(self.VRB)
        vrbs = vrbPage.find_all("div", class_="defv2wordtype", limit=amount)
        self.vrb = [vrb.text for vrb in vrbs] if len(vrbs) > 0 else ["Nothing"]

    def getSynonyms(self, amount):
        synmPage = self.getPage(self.SYNM)
        synms = synmPage.find_all("div", class_="wb", limit=amount)
        self.snm = [synm.a.text for synm in synms] if len(
            synms) > 0 else ["Nothing"]

    def getAntononyms(self, amount):
        antnmPage = self.getPage(self.ANTNM)
        antnms = antnmPage.find_all("div", class_="wb", limit=amount)
        self.antnm = [antm.a.text for antm in antnms] if len(
            antnms) > 0 else ["Nothing"]

    def fetchAll(self, n):
        t1 = Thread(target=self.getEnglishDefination, args=[n])
        t2 = Thread(target=self.getBanglaDefination, args=[n])
        t3 = Thread(target=self.getNoun, args=[n])
        t4 = Thread(target=self.getAdjective, args=[n])
        t5 = Thread(target=self.getAdverb, args=[n])
        t6 = Thread(target=self.getVerb, args=[n])
        t7 = Thread(target=self.getSynonyms, args=[n])
        t8 = Thread(target=self.getAntononyms, args=[n])

        t1.start()
        t2.start()
        t3.start()
        t4.start()
        t5.start()
        t6.start()
        t7.start()
        t8.start()

        t1.join()
        t2.join()
        t3.join()
        t4.join()
        t5.join()
        t6.join()
        t7.join()
        t8.join()

        return {
            "enDef": self.en_def,
            "bnDef": self.bn_def,
            "n": self.n,
            "adj": self.adj,
            "adv": self.adv,
            "vrb": self.vrb,
            "antnm": self.antnm,
            "snnm": self.snm
        }


def run():
    word = input("Word: ")
    print("Searching...")
    ld = LazyDict(word).fetchAll(2)

    print("Defination: ", ld["enDef"])
    print(ld["bnDef"])

    print("\n====== Nouns ======")
    for n in ld["n"]:
        print(n)

    print("\n====== Adjectives ======")
    for n in ld["adj"]:
        print(n)

    print("\n====== Adverbs ======")
    for n in ld["adv"]:
        print(n)

    print("\n====== Verbs ======")
    for n in ld["vrb"]:
        print(n)

    print("\n====== Synonyms ======")
    for n in ld["snnm"]:
        print(n)

    print("\n====== Antonyms ======")
    for n in ld["antnm"]:
        print(n)

    del ld


if __name__ == "__main__":
    # try:
    #     run()
    # except Exception as e:
    #     print("Ran into an error!\n", e)

    run()
