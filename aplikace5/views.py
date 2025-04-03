from django.shortcuts import render, redirect
from itertools import combinations
import random

def generate_valid_schedule(jmena):
    """ Generuje platný rozpis zápasů tak, aby žádný tým nebyl ve dvou po sobě jdoucích řádcích více než jednou """
    zapasy = [{"team1": team1, "team2": team2, "score1": None, "score2": None} for team1, team2 in combinations(jmena, 2)]
    random.shuffle(zapasy)

    # Kontrola a oprava pořadí zápasů
    final_schedule = []
    last_appearance = {}

    for zapas in zapasy:
        team1, team2 = zapas["team1"], zapas["team2"]

        if team1 in last_appearance and last_appearance[team1] == len(final_schedule):
            # Najdeme zápas, který může být přesunut
            for i in range(len(final_schedule) - 1, -1, -1):
                prev_match = final_schedule[i]
                if team1 not in [prev_match["team1"], prev_match["team2"]] and team2 not in [prev_match["team1"], prev_match["team2"]]:
                    final_schedule.insert(i + 1, zapas)
                    break
            else:
                final_schedule.append(zapas)
        elif team2 in last_appearance and last_appearance[team2] == len(final_schedule):
            for i in range(len(final_schedule) - 1, -1, -1):
                prev_match = final_schedule[i]
                if team1 not in [prev_match["team1"], prev_match["team2"]] and team2 not in [prev_match["team1"], prev_match["team2"]]:
                    final_schedule.insert(i + 1, zapas)
                    break
            else:
                final_schedule.append(zapas)
        else:
            final_schedule.append(zapas)

        last_appearance[team1] = len(final_schedule)
        last_appearance[team2] = len(final_schedule)

    return final_schedule

def ovladani_view(request):
    pocet_poli = None
    range_pocet_poli = None
    jmena = request.session.get('jmena', None)
    rozpis_zapasu = request.session.get('rozpis_zapasu', None)
    krizova_tabulka = request.session.get('krizova_tabulka', None)

    if request.method == 'POST' and 'pocet_ucastniku' in request.POST:
        try:
            pocet_poli = int(request.POST['pocet_ucastniku'])
            if 3 <= pocet_poli <= 50:
                range_pocet_poli = range(pocet_poli)
            else:
                pocet_poli = None
        except ValueError:
            pocet_poli = None

    elif request.method == 'POST' and 'jmeno_0' in request.POST:
        jmena = [request.POST.get(f'jmeno_{i}') for i in range(len(request.POST) - 1)]
        request.session['jmena'] = jmena

        rozpis_zapasu = generate_valid_schedule(jmena)
        request.session['rozpis_zapasu'] = rozpis_zapasu
        request.session.modified = True

        krizova_tabulka = [
            {"jmeno": team,
             "radek": ["X" if team == opponent else "" for opponent in jmena],
             "celkove_skore": "0:0",
             "body": 0,
             "poradi": None}
            for team in jmena
        ]
        request.session['krizova_tabulka'] = krizova_tabulka
        request.session.modified = True

    elif request.method == 'POST' and 'odeslat3' in request.POST:
        if rozpis_zapasu:
            for i, zapas in enumerate(rozpis_zapasu):
                score1 = request.POST.get(f'score_write1_{i + 1}')
                score2 = request.POST.get(f'score_write2_{i + 1}')
                if score1 is not None and score2 is not None:
                    try:
                        zapas['score1'] = int(score1)
                        zapas['score2'] = int(score2)
                    except ValueError:
                        continue

            request.session['rozpis_zapasu'] = rozpis_zapasu
            request.session.modified = True

            krizova_tabulka = []
            for team in jmena:
                vstrelene = 0
                obdrzene = 0
                body = 0
                radek = []

                for opponent in jmena:
                    if team == opponent:
                        radek.append("X")
                    else:
                        zapas = next(
                            (z for z in rozpis_zapasu if (z['team1'] == team and z['team2'] == opponent) or 
                                                       (z['team2'] == team and z['team1'] == opponent)), 
                            None
                        )
                        if zapas and zapas['score1'] is not None and zapas['score2'] is not None:
                            if zapas['team1'] == team:
                                radek.append(f"{zapas['score1']}:{zapas['score2']}")
                                vstrelene += zapas['score1']
                                obdrzene += zapas['score2']
                                if zapas['score1'] > zapas['score2']:
                                    body += 2
                                elif zapas['score1'] == zapas['score2']:
                                    body += 1
                            elif zapas['team2'] == team:
                                radek.append(f"{zapas['score2']}:{zapas['score1']}")
                                vstrelene += zapas['score2']
                                obdrzene += zapas['score1']
                                if zapas['score2'] > zapas['score1']:
                                    body += 2
                                elif zapas['score2'] == zapas['score1']:
                                    body += 1
                        else:
                            radek.append("")

                krizova_tabulka.append({
                    "jmeno": team,
                    "radek": radek,
                    "celkove_skore": f"{vstrelene}:{obdrzene}",
                    "body": body,
                    "poradi": None
                })

            sorted_tabulka = sorted(krizova_tabulka, key=lambda x: (-x["body"], -int(x["celkove_skore"].split(":")[0])))
            for i, team_data in enumerate(sorted_tabulka, start=1):
                team_data["poradi"] = i

            krizova_tabulka = sorted(sorted_tabulka, key=lambda x: jmena.index(x["jmeno"]))

            request.session['krizova_tabulka'] = krizova_tabulka
            request.session.modified = True

    return render(request, 'aplikace5/ovladani.html', {
        'pocet_poli': pocet_poli,
        'range_pocet_poli': range_pocet_poli,
        'jmena': jmena,
        'rozpis_zapasu': rozpis_zapasu,
        'krizova_tabulka': request.session.get('krizova_tabulka', None),
    })


def tabulecka_view(request):
    jmena = request.session.get('jmena', None)
    krizova_tabulka = request.session.get('krizova_tabulka', None)

    return render(request, 'aplikace5/tabulecka.html', {
        'jmena': jmena,
        'krizova_tabulka': krizova_tabulka,
    })


def vysledky_view(request):
    jmena = request.session.get('jmena', None)
    rozpis_zapasu = request.session.get('rozpis_zapasu', None)

    return render(request, 'aplikace5/vysledky.html', {
        'jmena': jmena,
        'rozpis_zapasu': rozpis_zapasu,
    })
