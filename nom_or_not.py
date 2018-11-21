# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
    author: ligetinagy
    last update: 2017.11.12.

    nyom-or-not
"""
import re

# still incomplete:
Post_Adj_list = ['alatti', 'általi', 'elleni', 'előli', 'előtti',
                 'felőli', 'fölötti', 'helyetti', 'iránti',
                 'képesti', 'körüli', 'közötti', 'melletti',
                 'mellőli', 'miatti', 'mögötti', 'nélküli', 'szerinti',
                 'végetti', 'utáni', 'közti', 'eleji', 'végi']

kopulativusz_name = "pred"
nom_or_kop_name = "nomorpred"
semmi_or_kop_name = "semmiorpred"

input_file_name = "/home/lnn/gitrepos/nyomor/data/small_test.txt"
output_file_name = "/home/lnn/gitrepos/nyomor/data/small_eval.txt"
outfile = open(output_file_name, 'w')


def is_be(anal):
    if anal[1] == "van":
        return True
    return False


def volt_nom(pool):
    """

    :param pool: list of tokens seen so far
    :return: true if there was a Nom already, false otherwise
    """
    for token in pool:
        if re.search("nom", token[2]) and not re.search("pred", token[2]):
            return True
    return False


def may_be_cop_verb(token):
    """

    :param token:  list of token, lemma, annotation with dots
    :return: True if the word is a potential copula, false otherwise
    """
    if token[1] in ["van", "lesz", "marad"] and token[0] not in ["van", "vannak"]:
        return True
    else:
        return False


def volt_verb(pool):
    """

    :param pool: list of tokens seen so far
    :return: true if there was a non copular verb already, false otherwise
    """
    for token in pool:
        if re.search("V", token[2]) and not may_be_cop_verb(token):
            return True
    return False


def is_volt(anal):
    """

    :param anal: one word, token, lemma and tags
    :return: true if it is a form of be but not van or vannak, false otherwise
    """
    if anal[1] == "van" and anal[0] != "van" and anal[0] != "vannak":
        return True
    return False


def may_be_gen(anal):
    """
    rules out words that can never be gen
    :param anal: list of token, lemma, annotation with dots
    :return: true or false
    """

    if anal[0] == "mindez" or anal[0] == "az" or anal[0] == "Mindez" or anal[0] == "Az" \
            or anal[0] == "Ez" or anal[0] == "ez" or anal[0] == "ami" \
            or anal[0] == "Ami" or anal[0] == "aki" or anal[0] == "Aki":
        return False

    return True


def may_be_DP(anal, pool):
    """

    :param anal: list of token, lemma, annotation.with.dots
    :param pool: list of tokens seen so far
    :return: true if this is a potential head of a DP, false otherwise
    """
    if re.search("Prop", anal[2]):
        return True
    if len(pool) > 0 and re.search("Det\|Art", pool[len(pool) - 1][2]):
        return True
    if not may_be_gen(anal):
        return True
    return False


def may_be_kop(anal):
    """
    rules out words that can never be kop
    :param anal: list of token, lemma, annotation with dots
    :return: true or false
    """
    no_kop_list = ["mindez", "Mindez", "aki", "ami", "Aki", "Ami", "Ez", "Az"]
    if anal[0] in no_kop_list:
        return False
    return True


def NPMod(anal):
    """
    defines if a token is an NPMod or not
    :param anal: list of token, lemma, annotation.with.dots
    :return: true if it is an NPMod, false otherwise
    """

    if re.search("Adj", anal[2]) or re.search("Num", anal[2]) or re.search("Ptcp", anal[2]):
        return True

    else:
        return False


def change_info(anal, to_change, change_to):
    """
    changes the info (suffix)
    :param anal: list of token, lemma, annotation.with.dots
    :param to_change: string of annotation info to change (e.g. "Nom")
    :param change_to: string to use as new annotation info (e.g. "semmi")
    :return: nothing
    """

    anal[2] = re.sub(to_change, change_to, anal[2])


def readtext():
    """
    read input file of test sentences
    sentence / line
    appends end-of-sentence characters

    :return: list of sentences
    """

    endofsent = ['#', '#', '#']

    sents = []

    with open(input_file_name, encoding='UTF-8') as infile:
        inputlines = infile.readlines()

    for line in inputlines:
        sentlist = []
        sent = line.strip().split(' ')
        for word in sent:
            sentlist.append(word.split('/'))
        sentlist.append(endofsent)
        sentlist.append(endofsent)
        sents.append(sentlist)

    return sents


def nyomorwhat(sents):
    """
    simulates nom-or-not

    :param sents: list of test sentences
    :return: None
    """
    j = 1
    n = 0
    for given_sent in sents:
        pure_tokens = []

        # write the sentence without annotation
        for item in given_sent:
            pure_tokens.append(item[0])
        outfile.write("\n \n" + str(j) + ": ")
        outfile.write(' '.join(pure_tokens))
        outfile.write("\n")
        j += 1
        may_be_nom = True

        for i in range(0, len(given_sent)):
            anal = given_sent[i]
            if anal[0] == '#':
                break
            window: object = given_sent[i + 1:i + 3]
            pool = given_sent[0:i]
            maradek = given_sent[i + 1:len(given_sent) - 2]
            first_right_annot = window[0][2]
            first_right_lemma = window[0][1]
            first_right_token = window[0][0]
            if volt_nom(pool):
                may_be_nom = False
                print(given_sent[i])
            if anal[2].endswith('Nom]'):
                # here come the rules
                n+=1
                if ((re.search("\[N(\|Pro)?(\|Rel)?(\|Int)?\]", anal[2])) or (NPMod(anal) and re.search("Pl", anal[2]))
                        or (re.search("TULN", anal[2])) or re.search("Det\|Pro", anal[2])):
                    # if it is a noun; noun rules here; plural NPMods as well
                    # if vagyok or vagy: kop
                    if is_be(anal) and (re.search("1Sg", anal[2]) or re.search("2Sg", anal[2])):
                        change_info(anal, 'Nom', kopulativusz_name)

                    # before postpositions, alatti-feletti and című-nevű: semmi
                    elif (first_right_token in Post_Adj_list) or (first_right_token == "című") or \
                            (first_right_token == "nevű") or (first_right_annot == "[Post]"):
                        change_info(anal, 'Nom', 'semmi')

                    # orig rule: if sg never can be a gen, then it is a nom; nom-or-kop version requires different \
                    # handling, therefore now switched off
                    # elif not may_be_gen(anal):
                    # change_info(anal, 'Nom', 'nom')

                    # before poss word but only if it can be a gen
                    elif re.search("Poss.3Sg", first_right_annot) and may_be_gen(anal):
                        change_info(anal, 'Nom', 'gen')

                    # before verbs and everything that can not be a kop
                    elif may_be_nom and ((re.search("V", first_right_annot) and not is_be(first_right_annot)) \
                                         or not may_be_kop(anal)):
                        change_info(anal, 'Nom', 'nom')

                    elif may_be_nom and re.search("TULN", anal[2]):
                        if re.search("TULN", first_right_annot) or \
                                ((first_right_token == 'a' or first_right_token == 'az') and
                                 re.search("Det", first_right_annot)):
                            change_info(anal, 'Nom', 'nom')

                    elif ((first_right_token == 'a' or first_right_token == 'az') and re.search("Det",
                                                                                                first_right_annot)
                          and not re.search("TULN", anal[2])) \
                            or first_right_token == "is" or first_right_token == "sem" or \
                            first_right_annot == "OTHER" or first_right_token == '!' \
                            or first_right_token == "nem" or re.search("Pro", first_right_annot) \
                            or first_right_token == "pedig" or first_right_token == "de" \
                            or first_right_token == "azonban" or first_right_annot == "Prev" or \
                            (not re.search("TULN", anal[2]) and re.search("TULN", first_right_token)) \
                            or re.search("Pl", first_right_annot) or (
                            re.search("TULN", anal[2]) and is_volt(first_right_annot)):
                        # before article, is, sem, dot or comma and a lot of other stuff: nomorkop
                        change_info(anal, 'Nom', nom_or_kop_name)
                        if not may_be_nom and not may_be_DP(anal, pool):
                            change_info(anal, nom_or_kop_name, kopulativusz_name)
                        elif volt_verb(pool):
                            change_info(anal, nom_or_kop_name, "nom")
                    elif NPMod(window[0]):
                        # before NPMod: nom or gen
                        change_info(anal, 'Nom', 'Nulla')
                        # check the next token
                        if re.search("Poss", window[1][2]) and not re.search("Poss.3Sg", anal[2]):
                            change_info(anal, 'Nulla', 'gen')
                        elif may_be_nom and (re.search("V", window[1][2]) or re.search("OTHER", window[1][2])
                                             or re.match("a[mk]i", window[1][0]) or re.match("hogy", window[1][0])
                                             or re.match("de", window[1][0]) or re.search("Poss.3Sg",
                                                                                          anal[2]) or re.match(
                                    "azonban", window[1][0])):
                            # check the second in the window
                            change_info(anal, 'Nulla', 'nom')

                    else:
                        # otherwise default
                        if may_be_nom:
                            change_info(anal, 'Nom', 'Nulla')
                            # check the second in the window
                            if re.search("V", window[1][2]):
                                # before verb: nom
                                change_info(anal, 'Nulla', 'nom')
                            elif re.search("OTHER", window[1][2]) or re.match("a[km]i", window[1][0]) or \
                                    re.match("hogy", window[1][0]) or re.match("de", window[1][0]) or \
                                    re.search("Poss.3Sg", anal[2]) or re.match("azonban", window[1][0]):
                                change_info(anal, 'Nulla', nom_or_kop_name)
                                if volt_verb(pool) and may_be_DP(anal, pool):
                                    change_info(anal, nom_or_kop_name, "nom")
                        else:
                            change_info(anal, 'Nom', 'gen')
                            if re.search("OTHER", window[1][2]) or re.match("a[km]i", window[1][0]) or \
                                    re.match("hogy", window[1][0]) or re.match("de", window[1][0]) or \
                                    re.search("Poss.3Sg", anal[2]) or re.match("azonban", window[1][0]):
                                change_info(anal, 'Nulla', 'gen')
                    if not may_be_gen(anal):
                        change_info(anal, 'Nulla', 'nom')

                    # window to file
                    # outfile.write('-' + pure_tokens[i] + ' ' + pure_tokens[i + 1] + ' ' + pure_tokens[i + 2] + '\n')
                    # three times for detailed analysis; twice for a simple one
                    # outfile.write(' '.join(anal) + "\n")
                    outfile.write(' '.join(anal) + "\n")
                    outfile.write(' '.join(anal) + '\n')

                # if it is an adjective; adj rules here
                elif re.search("Adj", anal[2]) or re.search("Ptcp", anal[2]):
                    if is_be(anal) and (re.search("1Sg", anal[2]) or re.search("2Sg", anal[2])):
                        change_info(anal, 'Nom', kopulativusz_name)

                    # before postpositions, alatti-feletti and című-nevű: semmi
                    elif (first_right_token in Post_Adj_list) or (first_right_token == "című") or \
                            (first_right_token == "nevű") or (first_right_annot == "Post"):
                        change_info(anal, 'Nom', 'semmi')


                    # if the next one is a verb: nom
                    elif may_be_nom and re.search("V", first_right_annot) and not re.search('van', first_right_lemma):
                        change_info(anal, 'Nom', 'nom')

                    # before article, is, sem, dot or comma: nomorkop
                    elif ((first_right_token == 'a' or first_right_token == 'az') and \
                          re.search("Det", first_right_annot)) \
                            or first_right_token == "is" or first_right_token == "sem" or \
                            first_right_annot == "OTHER" or first_right_token == "és" or first_right_token == '!' \
                            or first_right_token == "nem" or re.search("Pro", first_right_annot) \
                            or first_right_token == "pedig" or is_volt(window[0]):
                        change_info(anal, 'Nom', nom_or_kop_name)
                        if volt_verb(pool) or may_be_DP(anal, pool):
                            change_info(anal, nom_or_kop_name, "nom")
                        elif not may_be_nom:
                            change_info(anal, nom_or_kop_name, kopulativusz_name)

                    elif re.search("Num", first_right_annot):
                        # before a Num: nom or gen
                        if may_be_nom:
                            change_info(anal, 'Nom', 'Nulla')
                            if re.search("Poss.3Sg", window[1][2]):
                                change_info(anal, 'Nulla', 'gen')
                            else:
                                change_info(anal, 'Nulla', nom_or_kop_name)
                                if volt_verb(pool) or may_be_DP(anal, pool):
                                    change_info(anal, nom_or_kop_name, "nom")
                        else:
                            change_info(anal, 'Nom', 'gen')
                    else:
                        # otherwise default
                        change_info(anal, 'Nom', 'semmi')
                        if re.search("OTHER", window[1][2]):
                            change_info(anal, 'semmi', semmi_or_kop_name)
                            if volt_verb(pool) or may_be_DP(anal, pool):
                                change_info(anal, semmi_or_kop_name, "semmi")

                    # window to file
                    # outfile.write('-' + pure_tokens[i] + ' ' + pure_tokens[i + 1] + ' ' + pure_tokens[i + 2] + '\n')
                    # three times for detailed analysis; twice for a simple one
                    # outfile.write(' '.join(anal) + "\n")
                    outfile.write(' '.join(anal) + "\n")
                    outfile.write(' '.join(anal) + '\n')


                elif re.search("Num", anal[2]):
                    # if it is a Numeral; Num rules here

                    if re.search("(N)|(Num)|(Adj)|(Post)", first_right_annot) or re.search("című", first_right_token) \
                            or re.search("nevű", first_right_token) or first_right_token in Post_Adj_list:
                        change_info(anal, 'Nom', 'semmi')

                    elif may_be_nom and re.search("V", first_right_annot) and first_right_lemma != "van":
                        change_info(anal, 'Nom', 'nom')

                    elif ((first_right_token == "a" or first_right_token == "az") and
                          re.search("Det", first_right_annot)) or re.search("Adv", first_right_annot) or \
                            first_right_token == "is" \
                            or first_right_token == "sem" or first_right_token == "nem" or \
                            first_right_token == "pedig" or first_right_annot == "OTHER" or is_volt(window[0]):
                        change_info(anal, 'Nom', nom_or_kop_name)
                        if not may_be_nom:
                            change_info(anal, nom_or_kop_name, kopulativusz_name)
                        elif volt_verb(pool) or may_be_DP(anal, pool):
                            change_info(anal, nom_or_kop_name, "nom")
                    else:
                        # default
                        change_info(anal, 'Nom', semmi_or_kop_name)
                        if volt_verb(pool):
                            change_info(anal, semmi_or_kop_name, "semmi")

                    # window to file
                    # outfile.write('-' + pure_tokens[i] + ' ' + pure_tokens[i + 1] + ' ' + pure_tokens[i + 2] + '\n')
                    # three times for detailed analysis; twice for a simple one
                    # outfile.write(' '.join(anal) + "\n")
                    outfile.write(' '.join(anal) + "\n")
                    outfile.write(' '.join(anal) + '\n')

                else:

                    outfile.write("---valamire nem gondoltál!" + '\n' + "---")
                    outfile.write(' '.join(anal) + '\n')
    print(n)
    return

def main():
    sentlist = readtext()
    nyomorwhat(sentlist)
    # evaluate()


if __name__ == "__main__":
    main()
