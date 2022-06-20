from . import models

from django.shortcuts import render


def calc(rub):
    currency = models.Currency.objects.latest('last_update')
    rates = {
        "rub_usd_uni": currency.rub_usd_uni,
        "rub_eur_uni": currency.rub_eur_uni,
        "rub_amd_uni": currency.rub_amd_uni,
        "usd_amd_sas": currency.usd_amd_sas,
        "eur_amd_sas": currency.eur_amd_sas,
    }

    calculations = {"rub": rub,
                    "usd_uni": round(rub * rates["rub_usd_uni"], 2),
                    "usd_sas": round(
                        rub * rates["rub_usd_uni"] * rates["usd_amd_sas"], 2),
                    "eur_uni": round(rub * rates["rub_eur_uni"], 2),
                    "eur_sas": round(
                        rub * rates["rub_eur_uni"] * rates["eur_amd_sas"], 2),
                    "amd_uni": round(rub * rates["rub_amd_uni"], 2)}

    calculations["rub_usd_amd"] = round(calculations['usd_sas'] / rub, 3)
    calculations["rub_eur_amd"] = round(calculations['eur_sas'] / rub, 3)
    calculations["rub_amd"] = rates["rub_amd_uni"]

    calculations["best_rate"] = max(calculations["rub_usd_amd"],
                                    calculations["rub_eur_amd"],
                                    calculations["rub_amd"])
    calculations["best_scenario"] = list(calculations.keys())[
        list(calculations.values()).index(calculations["best_rate"])]
    return calculations




def index(request):
    # create_db()
    return render(request, 'rates.html')


def show_results(request):
    rub = float(request.POST["rub_input"])
    calculations = calc(rub)

    return render(request, 'result.html', calculations)
