import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import os



area_index = {
    1: 'Вінницька облать', 2: 'Волинська область', 3: 'Дніпропетровська область', 4: 'Донецька область', 5: 'Житомирська область', 6: 'Закарпатська область', 7: 'Запорізька область',
    8: 'Івано-Франківська область', 9: 'Київська область', 10: 'Кіровоградська область', 11: 'Луганська область', 12: 'Львівська область', 13: 'Миколаївська область', 14: 'Одеська область',
    15: 'Полтавська область', 16: 'Рівненська область', 17: 'Сумська область', 18: 'Тернопільська область', 19: 'Харківська область', 20: 'Херсонська область', 21: 'Хмельницька область',
    22: 'Черкаська область', 23: 'Чернівецька область', 24: 'Чернігівська область', 25: 'Крим'
}


def remake_data(directory):
    headers = ['Year', 'Week', 'SMN', 'SMT', 'VCI', 'TCI', 'VHI', 'empty']
    all_files = os.listdir(directory)
    merged = pd.DataFrame()

    for filename in all_files:
        filepath = os.path.join(directory, filename)

        try:
            df = pd.read_csv(filepath, header=1, names=headers)

            df = df[df["VHI"] != -1]

            area = filename.split("_")[2]
            df["Аrea"] = pd.to_numeric(area, errors="coerce")

            df["Year"] = df["Year"].astype(str).str.replace("<tt><pre>", "", regex=False)
            df = df[~df["Year"].str.contains('</pre></tt>', na=False)]
            df["Year"] = pd.to_numeric(df["Year"], errors="coerce")

            df.drop('empty', axis=1, inplace=True, errors="ignore")

            merged = pd.concat([merged, df], ignore_index=True)

        except Exception as erro:
            print(f"Error in file {filename}: {erro}")

    merged.drop_duplicates(inplace=True)
    merged["Аrea"] = merged["Аrea"].astype(int)
    merged = merged.sort_values(by=["Аrea", "Year", "Week"]).reset_index(drop=True)

    return merged

df = remake_data("C:/Users/Asus/OneDrive/Desktop/4 семестр/AD/lab_2/Pros_data")


defaults = {
    "index": "VHI",
    "region": list(area_index.values())[24],
    "week_range": (7, 20),
    "year_range": (2007, 2020),
    "sort_asc": False,
    "sort_desc": False,
}

for key, val in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = val

if st.button("Дефолтні фільтри"):
    for key, val in defaults.items():
        st.session_state[key] = val
    st.rerun()

col1, col2 = st.columns([1, 3])

with col1:
    st.session_state.index = st.selectbox("Індекс:", ["VCI", "TCI", "VHI"],
                                          index=["VCI", "TCI", "VHI"].index(st.session_state.index))
    st.session_state.region = st.selectbox("Область:", list(area_index.values()),
                                                index=list(area_index.values()).index(st.session_state.region))
    st.session_state.week_range = st.slider("Інтервал тижнів:", 1, 52, st.session_state.week_range)
    st.session_state.year_range = st.slider("Інтервал років:", int(df["Year"].min()), int(df["Year"].max()),
                                            st.session_state.year_range)
    st.session_state.sort_asc = st.checkbox("Сортувати за зростанням", value=st.session_state.sort_asc)
    st.session_state.sort_desc = st.checkbox("Сортувати за спаданням", value=st.session_state.sort_desc)

    if st.session_state.sort_asc and st.session_state.sort_desc:
        st.warning("Виберіть лише одне сортування.")

with col2:
    tab1, tab2, tab3 = st.tabs(["Вибрані дані", "Графік діапазон значень графік", "Графік порівняння"])

    for key, value in area_index.items():
        if value == st.session_state.region:
            region_id = key
            break

    filtered = df[
        (df["Аrea"] == region_id) &
        (df["Week"].between(*st.session_state.week_range)) &
        (df["Year"].between(*st.session_state.year_range))
        ][["Year", "Week", st.session_state.index, "Аrea"]]

    if st.session_state.sort_asc: # зростання
        filtered = filtered.sort_values(by=st.session_state.index, ascending=True)
    elif st.session_state.sort_desc: # спадання
        filtered = filtered.sort_values(by=st.session_state.index, ascending=False)

    with tab1:
        st.dataframe(filtered)

    with tab2:

        avg_by_week = filtered.groupby("Week")[st.session_state.index].mean().reset_index()
        plt.figure(figsize=(8, 4))
        sns.lineplot(data=avg_by_week, x="Week", y=st.session_state.index, marker="o")
        plt.title(f"Діапазон {st.session_state.index} по тижнях у {st.session_state.region}")
        plt.xlabel("Тиждень")
        plt.ylabel(st.session_state.index)
        plt.grid(True)
        st.pyplot(plt.gcf())

    with tab3:
        filtered_2 = df[
            (df["Week"].between(*st.session_state.week_range)) &
            (df["Year"].between(*st.session_state.year_range))
            ]

        plt.figure(figsize=(8, 4))
        filtered_2["region"] = filtered_2["Аrea"].map(area_index)

        sns.boxplot(data=filtered_2, x="region", y=st.session_state.index)
        plt.xticks(rotation=90)
        plt.title(f"Порівняння {st.session_state.index} по усіх областях")
        plt.xlabel("Область")
        plt.ylabel(st.session_state.index)
        st.pyplot(plt.gcf())