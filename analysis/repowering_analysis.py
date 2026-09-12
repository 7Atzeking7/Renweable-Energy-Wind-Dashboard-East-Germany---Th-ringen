import pandas as pd

# Daten laden
df = pd.read_csv("data/Stromerzeuger (8).csv", delimiter=";")

# Repowering-Potenzial filtern (Alter > 10 Jahre)
df["Inbetriebnahmedatum"] = pd.to_datetime(
    df["Inbetriebnahmedatum der Einheit"],
    format="%d.%m.%Y",
    errors="coerce"
)
df["Alter"] = 2026 - df["Inbetriebnahmedatum"].dt.year
repowering_potential = df[df["Alter"] > 10]

# Ergebnisse speichern
repowering_potential.to_csv("analysis/repowering_potential.csv", index=False)

# Zusammenfassung nach Planungsregionen
planning_regions = {
    'Nordthüringen': ['Eichsfeld', 'Mühlhausen', 'Heilbad Heiligenstadt', 'Dingelstädt', 'Küllstedt', 'Sonderhausen', 'Bad Langensalza', 'Kindelbrück', 'Günstedt', 'Hörselberg-Hainich'],
    'Mittelthüringen': ['Erfurt', 'Gotha', 'Weimar', 'Apolda', 'Bad Tennstedt', 'Sömmerda'],
    'Ostthüringen': ['Gera', 'Altenburg', 'Schmölln', 'Ronneburg', 'Zeitz', 'Weida', 'Greiz'],
    'Südthüringen': ['Schmalkalden-Meiningen', 'Suhl', 'Eisenach', 'Oberhof', 'Bad Liebenstein', 'Wartburgkreis', 'Thüringer Wald', 'Rennsteig']
}

repowering_potential["Planungsregion"] = repowering_potential["Ort"].apply(
    lambda x: next((region for region, locations in planning_regions.items() if x in locations), "Unbekannt")
)

summary = repowering_potential.groupby("Planungsregion").agg({
    "Anzeige-Name der Einheit": "count",
    "Bruttoleistung der Einheit": "sum"
}).reset_index()

summary.columns = ["Planungsregion", "Anzahl WEA", "Gesamtleistung (kW)"]
summary["Gesamtleistung (MW)"] = summary["Gesamtleistung (kW)"] / 1000

print(summary)
