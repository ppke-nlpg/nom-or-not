import re
def evaluate():
    """

    :param
    :return: None
    """
    i = 0
    nom_nom = 0
    nom_nulla = 0  # falsely underspecified; window-context!
    gen_gen = 0
    gen_nulla = 0  # falsely underspecified; window-context!
    nulla_nulla = 0  # correctly underspecified; window-context!
    semmi_semmi = 0
    pred_pred = 0
    vok_vok = 0
    nomorpred_nomorpred = 0
    nom_gen = 0
    nom_pred = 0
    nom_semmi = 0
    pred_nulla = 0
    pred_gen = 0
    pred_nom = 0
    pred_semmi = 0
    semmi_nulla = 0
    semmi_nom = 0
    semmi_gen = 0
    pred_nomorpred = 0
    semmi_nomorpred = 0
    semmi_semmiorpred = 0
    nom_nomorpred = 0
    nomorpred_nom= 0
    nomorpred_pred = 0
    semmiorpred_semmi = 0
    semmiorpred_pred = 0
    nulla_nom = 0
    nulla_gen = 0
    gen_nom = 0
    amnk = 0
    other = 0
    postag = 0
    ortho = 0
    inf = open("/home/lnn/gitrepos/nyomor/data/merged_results.txt", encoding='UTF-8')
    for line in inf:
        i += 1
        if re.search("^[^0-9\-]", line.strip()):
            annot_manual = line.split()[2]
            # print(line)
            annot_automatic = inf.readline().strip().split()[2]
            i += 1
            if annot_manual == annot_automatic:
                # ha ugyanazt mondtuk:
                if annot_manual.endswith("nom]"):
                    nom_nom += 1
                elif annot_manual.endswith("gen]"):
                    gen_gen += 1
                elif annot_manual.endswith("nulla]"):
                    nulla_nulla += 1
                elif annot_manual.endswith("semmi]"):
                    semmi_semmi += 1
                elif annot_manual.endswith("pred]"):
                    pred_pred += 1
                elif annot_manual.endswith("vok]"):
                    vok_vok += 1
                elif annot_manual.endswith("nomorpred]"):
                    nomorpred_nomorpred += 1

            else:
                if annot_manual.endswith("nom]") and annot_automatic.endswith("nulla]"):
                    nom_nulla += 1
                elif annot_manual.endswith("gen]") and annot_automatic.endswith("nulla]"):
                    gen_nulla += 1
                elif annot_manual.endswith("nom]") and annot_automatic.endswith("gen]"):
                    nom_gen += 1

                elif annot_manual.endswith("nom]") and annot_automatic.endswith("[pred]"):
                    nom_pred += 1

                elif annot_manual.endswith("nom]") and annot_automatic.endswith("semmi]"):
                    nom_semmi += 1
                elif annot_manual.endswith("pred]") and annot_automatic.endswith("nulla]"):
                    pred_nulla += 1
                elif annot_manual.endswith("pred]") and annot_automatic.endswith("gen]"):
                    pred_gen += 1

                elif annot_manual.endswith("pred]") and annot_automatic.endswith("nom]"):
                    pred_nom += 1
                elif annot_manual.endswith("pred]") and annot_automatic.endswith("semmi]"):
                    pred_semmi += 1

                elif annot_manual.endswith("hiba]"):
                    postag += 1
                elif annot_manual.endswith("semmi]") and annot_automatic.endswith("nulla]"):
                    semmi_nulla +=1
                elif annot_manual.endswith("semmi]") and annot_automatic.endswith("nom]"):
                    semmi_nom += 1

                elif annot_manual.endswith("semmi]") and annot_automatic.endswith("nomorpred]"):
                    semmi_nomorpred += 1
                elif annot_manual.endswith("semmi]") and annot_automatic.endswith("gen]"):
                    semmi_gen += 1
                    print(i)
                elif annot_manual.endswith("pred]") and annot_automatic.endswith("nomorpred]"):
                    pred_nomorpred += 1
                elif annot_manual.endswith("gen]") and annot_automatic.endswith("nom]"):
                    gen_nom += 1
                elif annot_manual.endswith("semmi]") and annot_automatic.endswith("semmiorpred]"):
                    semmi_semmiorpred += 1
                elif annot_manual.endswith("semmiorpred]") and annot_automatic.endswith("semmi]"):
                    semmiorpred_semmi += 1
                elif annot_manual.endswith("semmiorpred]") and annot_automatic.endswith("[pred]"):
                    semmiorpred_pred += 1
                elif annot_manual.endswith("nomorpred]") and annot_automatic.endswith("nom]"):
                    nomorpred_nom += 1
                elif annot_manual.endswith("nomorpred]") and annot_automatic.endswith("[pred]"):
                    nomorpred_pred += 1
                elif annot_manual.endswith("nulla]") and annot_automatic.endswith("nom]"):
                    nulla_nom += 1
                elif annot_manual.endswith("nulla]") and annot_automatic.endswith("gen]"):
                    nulla_gen += 1

                elif annot_manual.endswith("nom]") and annot_automatic.endswith("nomorpred]"):
                    nom_nomorpred += 1
                else:
                    other += 1
                    print(annot_manual)
                    print(annot_automatic)
                    print()

    print("nom_nom = " + str(nom_nom))
    print("gen_gen = " + str(gen_gen))
    print("semmi_semmi = " + str(semmi_semmi))
    print("nulla_nulla = " + str(nulla_nulla))
    print("pred_pred = " + str(pred_pred))
    print("nomorpred_nomorpred = " + str(nomorpred_nomorpred))

    print("\n\nFP\n\n")
    print("nom_pred = " + str(nom_pred))
    print("pred_nom = " + str(pred_nom))

    print("nomorpred_nom = " + str(nomorpred_nom))
    print("nomorpred_pred = " + str(nomorpred_pred))
    print("semmiorpred_semmi = " + str(semmiorpred_semmi))
    print("semmiorpred_pred = " + str(semmiorpred_pred))
    print("nulla_gen = " + str(nulla_gen))
    print("nulla_nom = " + str(nulla_nom))
    print("nom_gen = " + str(nom_gen))
    print("gen_nom = " + str(gen_nom))

    print("nom_semmi = " + str(nom_semmi))
    print("pred_nulla = " + str(pred_nulla))
    print("pred_gen = " + str(pred_gen))
    print("pred_semmi = " + str(pred_semmi))
    print("semmi_gen = " + str(semmi_gen))
    print("semmi_nulla = " + str(semmi_nulla))
    print("semmi_nom = " + str(semmi_nom))
    print("semmi_nomorpred = " + str(semmi_nomorpred))
    print("\n\nFN\n\n")

    print("gen_nulla = " + str(gen_nulla))
    print("semmi_semmiorpred = " + str(semmi_semmiorpred))
    print("pred_nomorpred = " + str(pred_nomorpred))
    print("nom_nulla = " + str(nom_nulla))
    print("nom_nomorpred = " + str(nom_nomorpred))


    print("postag = " + str(postag))
    print("egyéb = " + str(other))

    print("TP: " + str(nom_nom + gen_gen + semmi_semmi + nulla_nulla + pred_pred + nomorpred_nomorpred))
    print("FP: " + str(nomorpred_nom + nomorpred_pred + semmiorpred_semmi + semmiorpred_pred + nulla_gen + nulla_nom + \
                       nom_gen + nom_pred + nom_semmi + gen_nom + semmi_gen + semmi_nomorpred + semmi_nom + semmi_nulla +
                       pred_nom + pred_gen + pred_semmi + pred_nulla + other))
    print("FN: " + str(nom_nomorpred + pred_nomorpred + nom_nulla + gen_nulla + semmi_semmiorpred))
evaluate()