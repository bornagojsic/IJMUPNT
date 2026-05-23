from __future__ import annotations

import json
import math
import re
import textwrap
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from scipy.stats import chi2_contingency


ROOT = Path(__file__).resolve().parents[2]
DATA_PATH = ROOT / "anketa_utorak.xlsx"
OUTPUTS = ROOT / "analysis" / "outputs"
FIGURES = OUTPUTS / "figures"
TABLES = OUTPUTS / "tables"
REPORT_TABLES = ROOT / "report" / "tables"
REPORT_FIGURES = ROOT / "report" / "figures"
PRESENTATION_FIGURES = ROOT / "presentation" / "figures"

TITLE = "Analiza javnog mnijenja o sigurnosti SMR tehnologije i prihvatljivosti izgradnje u blizini mjesta stanovanja"

DEMOGRAPHICS = {
    "zupanija": "Županija:",
    "spol": "Spol:",
    "dob": "Dob:",
    "obrazovanje": "Najviši završen stupanj obrazovanja:",
    "zaposlenost": "Status zaposlenosti:",
}

QUESTION_PREFIXES = {
    "p9": "P9:",
    "p10": "P10:",
}

DISPLAY_NAMES = {
    "zupanija": "Županija",
    "spol": "Spol",
    "dob": "Dob",
    "obrazovanje": "Obrazovanje",
    "zaposlenost": "Status zaposlenosti",
    "p9": "P9",
    "p10": "P10",
}

P9_SHORT = {
    "Niski početni i ukupni troškovi investicije": "Niži troškovi",
    "Daleko kraće vrijeme izgradnje i puštanje u pogon": "Kraća izgradnja",
    "Poboljšane sigurnosne značajke reaktora": "Sigurnosne značajke",
    "Ne znam": "Ne znam",
}

P10_SHORT = {
    "Da": "Da",
    "Ne": "Ne",
    "Ne znam": "Ne znam",
}

TEAM_MEMBERS = [
    "Ivan Draženović",
    "Mateo Držanić",
    "Ivan Dundović",
    "Matej Đaković",
    "Lovro Đuranec",
    "Darko Erceg",
    "Andro Filić",
    "Marko Flajsig",
    "Andro Gabaj",
    "Kristijan Gašpar",
    "Borna Gojšić",
    "Ivan Golubić",
    "Toni Grdović",
    "Jakov Gregurić",
    "Ljubo Grubišić",
]

MIN_CATEGORY_COUNT = 5


def ensure_dirs() -> None:
    for path in [FIGURES, TABLES, REPORT_TABLES, REPORT_FIGURES, PRESENTATION_FIGURES]:
        path.mkdir(parents=True, exist_ok=True)


def find_column(columns: list[str], exact: str | None = None, prefix: str | None = None) -> str:
    if exact is not None and exact in columns:
        return exact
    if prefix is not None:
        matches = [column for column in columns if str(column).startswith(prefix)]
        if len(matches) == 1:
            return matches[0]
        if not matches:
            raise ValueError(f"Nije pronađen stupac s prefiksom: {prefix}")
        raise ValueError(f"Pronađeno je više stupaca s prefiksom {prefix}: {matches}")
    raise ValueError("Potrebno je zadati exact ili prefix.")


def normalize_text(value: object) -> str | None:
    if pd.isna(value):
        return None
    text = " ".join(str(value).strip().split())
    return text if text else None


def frequency_table(series: pd.Series, order: list[str] | None = None) -> pd.DataFrame:
    counts = series.dropna().value_counts()
    if order is not None:
        counts = counts.reindex(order).dropna().astype(int)
    total = counts.sum()
    return pd.DataFrame(
        {
            "Odgovor": counts.index,
            "Broj": counts.values,
            "Postotak": (counts.values / total * 100).round(2) if total else [],
        }
    )


def save_table(df: pd.DataFrame, name: str) -> None:
    csv_path = TABLES / f"{name}.csv"
    tex_path = REPORT_TABLES / f"{name}.tex"
    df.to_csv(csv_path, index=False, float_format="%.2f")
    df.to_latex(tex_path, index=False, escape=False, float_format="%.2f")


def wrap_labels(labels: list[str], width: int = 18) -> list[str]:
    return ["\n".join(textwrap.wrap(label, width=width)) for label in labels]


def bar_chart(df: pd.DataFrame, name: str, title: str, color: str) -> None:
    sns.set_theme(style="whitegrid", font="DejaVu Sans")
    fig, ax = plt.subplots(figsize=(9, 5.2))
    bars = ax.bar(df["Odgovor"], df["Postotak"], color=color)
    ax.set_title(title, fontsize=14, weight="bold")
    ax.set_ylabel("Udio odgovora (%)")
    ax.set_xlabel("")
    ax.set_ylim(0, max(100, math.ceil(float(df["Postotak"].max()) / 10) * 10 + 10))
    ax.set_xticks(range(len(df["Odgovor"])))
    ax.set_xticklabels(wrap_labels(df["Odgovor"].astype(str).tolist()), rotation=0, ha="center")
    for bar, value in zip(bars, df["Postotak"]):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 1, f"{value:.2f}%", ha="center", va="bottom", fontsize=10)
    fig.tight_layout()
    for folder in [FIGURES, REPORT_FIGURES, PRESENTATION_FIGURES]:
        fig.savefig(folder / f"{name}.pdf")
        fig.savefig(folder / f"{name}.png", dpi=200)
    plt.close(fig)


def stacked_chart(df: pd.DataFrame, row: str, col: str, name: str, title: str) -> None:
    table = pd.crosstab(df[row], df[col], normalize="index") * 100
    table = table.round(2)
    fig, ax = plt.subplots(figsize=(10, 5.8))
    table.plot(kind="bar", stacked=True, ax=ax, colormap="viridis")
    ax.set_title(title, fontsize=13, weight="bold")
    ax.set_ylabel("Udio odgovora (%)")
    ax.set_xlabel(DISPLAY_NAMES.get(row, row))
    ax.set_xticklabels(wrap_labels([str(x) for x in table.index], width=16), rotation=0, ha="center")
    ax.legend(title=DISPLAY_NAMES.get(col, col), bbox_to_anchor=(1.02, 1), loc="upper left")
    fig.tight_layout()
    for folder in [FIGURES, REPORT_FIGURES, PRESENTATION_FIGURES]:
        fig.savefig(folder / f"{name}.pdf")
        fig.savefig(folder / f"{name}.png", dpi=200)
    plt.close(fig)


def slugify(value: str) -> str:
    value = value.lower().replace("ž", "z").replace("š", "s").replace("đ", "d").replace("č", "c").replace("ć", "c")
    return re.sub(r"[^a-z0-9]+", "_", value).strip("_")


def collapse_rare_categories(series: pd.Series, min_count: int = MIN_CATEGORY_COUNT) -> tuple[pd.Series, list[str]]:
    counts = series.dropna().value_counts()
    rare_values = counts[counts < min_count].index.tolist()
    if not rare_values:
        return series, []
    return series.where(~series.isin(rare_values), f"Ostalo (<{min_count})"), [str(value) for value in rare_values]


def prepare_pair_data(df: pd.DataFrame, left: str, right: str) -> tuple[pd.DataFrame, dict[str, list[str]]]:
    pair_df = df[[left, right]].dropna().copy()
    collapsed: dict[str, list[str]] = {}
    for column in [left, right]:
        pair_df[column], rare_values = collapse_rare_categories(pair_df[column])
        if rare_values:
            collapsed[column] = rare_values
    return pair_df, collapsed


def association_heatmap(
    pair_df: pd.DataFrame,
    left: str,
    right: str,
    name: str,
    title: str,
    p_value: float,
    cramer_v: float,
) -> None:
    counts = pd.crosstab(pair_df[left], pair_df[right])
    percentages = (counts.div(counts.sum(axis=1), axis=0) * 100).round(2)
    labels = percentages.map(lambda value: f"{value:.2f}%")

    fig_width = max(8, 1.5 * len(percentages.columns) + 2)
    fig_height = max(4.8, 0.7 * len(percentages.index) + 2)
    fig, ax = plt.subplots(figsize=(fig_width, fig_height))
    sns.heatmap(percentages, annot=labels, fmt="", cmap="Blues", cbar_kws={"label": "Udio po retku (%)"}, ax=ax)
    ax.set_title(f"{title}\nhi-kvadrat: p = {p_value:.5f}, Cramér V = {cramer_v:.3f}", fontsize=13, weight="bold")
    ax.set_xlabel(DISPLAY_NAMES.get(right, right))
    ax.set_ylabel(DISPLAY_NAMES.get(left, left))
    ax.set_xticklabels(wrap_labels([str(x) for x in percentages.columns], width=16), rotation=0, ha="center")
    ax.set_yticklabels(wrap_labels([str(y) for y in percentages.index], width=18), rotation=0)
    fig.tight_layout()
    for folder in [FIGURES, REPORT_FIGURES, PRESENTATION_FIGURES]:
        fig.savefig(folder / f"{name}.pdf")
        fig.savefig(folder / f"{name}.png", dpi=200)
    plt.close(fig)


def cramers_v(chi2: float, n: int, shape: tuple[int, int]) -> float:
    r, k = shape
    denom = n * (min(r - 1, k - 1))
    if denom <= 0:
        return 0.0
    return math.sqrt(chi2 / denom)


def chi_square_tests(df: pd.DataFrame, pairs: list[tuple[str, str]]) -> pd.DataFrame:
    rows = []
    for left, right in pairs:
        pair_df, collapsed = prepare_pair_data(df, left, right)
        table = pd.crosstab(pair_df[left], pair_df[right])
        collapse_note = "; ".join(
            f"{DISPLAY_NAMES[column]}: " + ", ".join(values)
            for column, values in collapsed.items()
        )
        if table.shape[0] < 2 or table.shape[1] < 2:
            rows.append(
                {
                    "Ključ 1": left,
                    "Ključ 2": right,
                    "Varijabla 1": DISPLAY_NAMES[left],
                    "Varijabla 2": DISPLAY_NAMES[right],
                    "Hi-kvadrat": None,
                    "df": None,
                    "p-vrijednost": None,
                    "Cramér V": None,
                    "Najmanja očekivana frekvencija": None,
                    "Slika": None,
                    "Spojene kategorije": collapse_note,
                    "Napomena": "Test nije proveden jer jedna varijabla ima manje od dvije kategorije.",
                }
            )
            continue
        chi2, p_value, dof, expected = chi2_contingency(table)
        n = int(table.to_numpy().sum())
        min_expected = float(expected.min())
        rows.append(
            {
                "Ključ 1": left,
                "Ključ 2": right,
                "Varijabla 1": DISPLAY_NAMES[left],
                "Varijabla 2": DISPLAY_NAMES[right],
                "Hi-kvadrat": round(float(chi2), 3),
                "df": int(dof),
                "p-vrijednost": round(float(p_value), 5),
                "Cramér V": round(cramers_v(float(chi2), n, table.shape), 3),
                "Najmanja očekivana frekvencija": round(min_expected, 2),
                "Slika": f"povezanost_{slugify(left)}_{slugify(right)}",
                "Spojene kategorije": collapse_note,
                "Napomena": "Oprez: dio očekivanih frekvencija je manji od 5." if min_expected < 5 else "",
            }
        )
    return pd.DataFrame(rows)


def display_test_table(tests: pd.DataFrame) -> pd.DataFrame:
    return tests[
        [
            "Varijabla 1",
            "Varijabla 2",
            "Hi-kvadrat",
            "df",
            "p-vrijednost",
            "Cramér V",
            "Najmanja očekivana frekvencija",
            "Napomena",
        ]
    ]


def generate_significant_association_outputs(df: pd.DataFrame, tests: pd.DataFrame) -> None:
    significant = tests[(tests["p-vrijednost"].notna()) & (tests["p-vrijednost"] < 0.05)].copy()
    lines = [
        "% Automatski generirano skriptom analysis/src/analyze.py",
        "U nastavku su prikazani grafovi povezanosti za parove varijabli kod kojih je hi-kvadrat test pokazao statistički značajnu povezanost na razini značajnosti $\\alpha = 0{,}05$. Prije testiranja kategorije s manje od pet opažanja spojene su u kategoriju \\textit{Ostalo (<5)}.",
        "",
    ]

    if significant.empty:
        lines.append("Nakon spajanja rijetkih kategorija nije pronađena statistički značajna povezanost.")
    else:
        for _, row in significant.iterrows():
            left = row["Ključ 1"]
            right = row["Ključ 2"]
            pair_df, _ = prepare_pair_data(df, left, right)
            figure_name = row["Slika"]
            title = f"{row['Varijabla 1']} i {row['Varijabla 2']}"
            association_heatmap(
                pair_df,
                left,
                right,
                figure_name,
                title,
                float(row["p-vrijednost"]),
                float(row["Cramér V"]),
            )
            lines.extend(
                [
                    "\\begin{figure}[H]",
                    "\\centering",
                    f"\\includegraphics[width=0.92\\textwidth]{{{figure_name}.pdf}}",
                    f"\\caption{{Povezanost varijabli {row['Varijabla 1']} i {row['Varijabla 2']} nakon spajanja rijetkih kategorija}}",
                    f"\\label{{fig:{figure_name}}}",
                    "\\end{figure}",
                    "",
                ]
            )

    (ROOT / "report" / "sections" / "generated_significant_associations.tex").write_text("\n".join(lines), encoding="utf-8")


def write_markdown_summary(df: pd.DataFrame, tests: pd.DataFrame) -> None:
    significant = tests[(tests["p-vrijednost"].notna()) & (tests["p-vrijednost"] < 0.05)].copy()
    lines = ["# Sažetak analize", "", f"Naslov: {TITLE}", "", f"Broj odgovora u analiziranom skupu: {len(df)}", ""]
    lines.append("## Statistički značajne povezanosti")
    lines.append("")
    if significant.empty:
        lines.append("Nije pronađena statistički značajna povezanost na razini značajnosti 0,05.")
    else:
        for _, row in significant.iterrows():
            lines.append(
                f"- {row['Varijabla 1']} i {row['Varijabla 2']}: p = {row['p-vrijednost']}, Cramér V = {row['Cramér V']}"
            )
    lines.append("")
    lines.append("## Napomena")
    lines.append("")
    lines.append("U izvještaju treba dodatno procijeniti jesu li statistički značajne razlike i sadržajno važne.")
    (OUTPUTS / "summary.md").write_text("\n".join(lines), encoding="utf-8")


def write_metadata(df: pd.DataFrame, p9_table: pd.DataFrame, p10_table: pd.DataFrame, tests: pd.DataFrame) -> None:
    metadata = {
        "title": TITLE,
        "team_members": TEAM_MEMBERS,
        "n_responses": int(len(df)),
        "p9_top_answer": p9_table.iloc[0].to_dict() if not p9_table.empty else None,
        "p10_top_answer": p10_table.iloc[0].to_dict() if not p10_table.empty else None,
        "significant_tests": tests[(tests["p-vrijednost"].notna()) & (tests["p-vrijednost"] < 0.05)].to_dict(orient="records"),
    }
    (OUTPUTS / "metadata.json").write_text(json.dumps(metadata, ensure_ascii=False, indent=2), encoding="utf-8")


def main() -> None:
    ensure_dirs()
    raw = pd.read_excel(DATA_PATH)
    columns = list(raw.columns)

    selected_columns = {}
    for key, exact in DEMOGRAPHICS.items():
        selected_columns[key] = find_column(columns, exact=exact)
    for key, prefix in QUESTION_PREFIXES.items():
        selected_columns[key] = find_column(columns, prefix=prefix)

    df = raw[list(selected_columns.values())].rename(columns={v: k for k, v in selected_columns.items()})
    for column in df.columns:
        df[column] = df[column].map(normalize_text)

    df["p9_short"] = df["p9"].map(P9_SHORT).fillna(df["p9"])
    df["p10_short"] = df["p10"].map(P10_SHORT).fillna(df["p10"])

    p9_order = ["Niži troškovi", "Kraća izgradnja", "Sigurnosne značajke", "Ne znam"]
    p10_order = ["Da", "Ne", "Ne znam"]

    p9_table = frequency_table(df["p9_short"], p9_order)
    p10_table = frequency_table(df["p10_short"], p10_order)
    save_table(p9_table, "p9_frekvencije")
    save_table(p10_table, "p10_frekvencije")

    for column in DEMOGRAPHICS:
        table = frequency_table(df[column])
        save_table(table, f"{column}_frekvencije")

    bar_chart(p9_table, "p9_odgovori", "P9: najveća percipirana prednost SMR tehnologije", "#2F6F8F")
    bar_chart(p10_table, "p10_odgovori", "P10: opravdanost državnih subvencija za razvoj SMR tehnologije", "#8F4A2F")

    test_df = df.rename(columns={"p9_short": "p9_kratko", "p10_short": "p10_kratko"})
    DISPLAY_NAMES["p9_kratko"] = "P9"
    DISPLAY_NAMES["p10_kratko"] = "P10"
    test_pairs = []
    for demographic in DEMOGRAPHICS:
        test_pairs.append((demographic, "p9_kratko"))
        test_pairs.append((demographic, "p10_kratko"))
    test_pairs.append(("p9_kratko", "p10_kratko"))
    tests = chi_square_tests(test_df, test_pairs)
    save_table(display_test_table(tests), "hi_kvadrat_testovi")
    generate_significant_association_outputs(test_df, tests)

    for demographic in ["spol", "dob", "obrazovanje", "zaposlenost"]:
        stacked_chart(test_df, demographic, "p9_kratko", f"p9_po_{demographic}", f"P9 prema obilježju: {DISPLAY_NAMES[demographic]}")
        stacked_chart(test_df, demographic, "p10_kratko", f"p10_po_{demographic}", f"P10 prema obilježju: {DISPLAY_NAMES[demographic]}")

    crosstab_p9_p10 = pd.crosstab(test_df["p9_kratko"], test_df["p10_kratko"], margins=True)
    crosstab_p9_p10.index.name = "P9"
    crosstab_p9_p10.columns.name = "P10"
    crosstab_p9_p10 = crosstab_p9_p10.rename(index={"All": "Ukupno"}, columns={"All": "Ukupno"})
    crosstab_p9_p10.to_csv(TABLES / "p9_p10_krizna_tablica.csv", float_format="%.2f")
    crosstab_p9_p10.to_latex(REPORT_TABLES / "p9_p10_krizna_tablica.tex", escape=False)

    legend = pd.DataFrame(
        [
            {"Oznaka": short, "Puni odgovor": full}
            for full, short in P9_SHORT.items()
        ]
        + [
            {"Oznaka": short, "Puni odgovor": full}
            for full, short in P10_SHORT.items()
            if short != full
        ]
    )
    save_table(legend, "legenda_oznaka")

    write_markdown_summary(test_df, tests)
    write_metadata(test_df, p9_table, p10_table, tests)

    print(f"Analiza završena. Obrađeno odgovora: {len(test_df)}")
    print(f"Rezultati su spremljeni u: {OUTPUTS}")


if __name__ == "__main__":
    main()
