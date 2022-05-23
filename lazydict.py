import requests
from bs4 import BeautifulSoup


class LazyDict:
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

    def getPage(self, url):
        return BeautifulSoup(requests.get(url).content, features="html.parser")

    def getEnglishDefination(self):
        soup = self.getPage(self.EDEF)
        definations = soup.find_all("div", class_="tabdesc")
        return definations[0].text if definations else ""

    def getBanglaDefination(self):
        soup = self.getPage(self.BDEF)
        defination = soup.find_all("div", class_="align_text2")
        return defination[0].text if defination else "Nothing"

    def getNoun(self, amount):
        soup = self.getPage(self.NOUN)
        nouns = soup.find_all("div", class_="defv2wordtype", limit=amount)
        return [noun.text for noun in nouns]

    def getAdjective(self, amount):
        adjPage = self.getPage(self.ADJ)
        adjs = adjPage.find_all("div", class_="defv2wordtype", limit=amount)
        return [adj.text for adj in adjs] if len(adjs) > 0 else "Nothing"

    def getAdverb(self, amount):
        advPage = self.getPage(self.ADV)
        advs = advPage.find_all("div", class_="defv2wordtype", limit=amount)
        return [adv.text for adv in advs] if len(advs) > 0 else "Nothing"

    def getVerb(self, amount):
        vrbPage = self.getPage(self.VRB)
        vrbs = vrbPage.find_all("div", class_="defv2wordtype", limit=amount)
        return [vrb.text for vrb in vrbs] if len(vrbs) > 0 else "Nothing"

    def getSynonyms(self, amount):
        synmPage = self.getPage(self.SYNM)
        synms = synmPage.find_all("div", class_="wb", limit=amount)
        return [synm.a.text for synm in synms] if len(synms) > 0 else "nothing"

    def getAntononyms(self, amount):
        antnmPage = self.getPage(self.ANTNM)
        antnms = antnmPage.find_all("div", class_="wb", limit=amount)
        return [antm.a.text for antm in antnms] if len(antnms) > 0 else "nothing"

    def fetchAll(self, n):

        return {
            "enDef": self.getEnglishDefination(),
            "bnDef": self.getBanglaDefination(),
            "n": self.getNoun(n),
            "adj": self.getAdjective(n),
            "adv": self.getAdverb(n),
            "vrb": self.getVerb(n),
            "antnm": self.getAntononyms(n),
            "snnm": self.getSynonyms(n)
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
