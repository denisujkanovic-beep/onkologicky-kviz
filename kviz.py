import streamlit as st

# 1. NASTAVENÍ VZHLEDU STRÁNKY
st.set_page_config(page_title="Onkologický Kvíz", page_icon="🩺", layout="centered")

# Definice všech otázek do přehledné struktury
OTAZKY = [
    {
        "id": 1, "otazka": "Optimální příprava před ozařováním v oblasti pánve je?",
        "moznosti": ["Prázdný močový měchýř", "Plný močový měchýř, vyprázdněný konečník", "Žládná příprava není nutná"], "spravna": "b"
    },
    {
        "id": 2, "otazka": "Radioterapie se nejčastěji u nádoru GIT využívá u?",
        "moznosti": ["Karcinomu žaludku", "Karcinomu tenkého střeva", "Karcinomu konečníku a řiti"], "spravna": "c"
    },
    {
        "id": 3, "otazka": "Metastázy karcinomu prostaty nejčastěji míří do:",
        "moznosti": ["Jater", "Kostí", "Mozku"], "spravna": "b"
    },
    {
        "id": 4, "otazka": "Základní léčba lokálně pokročilého karcinomu hrdla děložního je:",
        "moznosti": ["Chirurgie", "Chemoradioterapie + brachyterapie", "Pouze brachyterapie"], "spravna": "b"
    },
    {
        "id": 5, "otazka": "Nejčastější dětské nádory jsou:",
        "moznosti": ["Mozkové nádory, neuroblastomy, sarkomy", "Leukémie, kostní nádory, hepatoblastomy", "Leukémie, mozkové nádory, lymfomy"], "spravna": "c"
    },
    {
        "id": 6, "otazka": "FDG-PET/CT se nejvíce využívá u:",
        "moznosti": ["Stagingu karcinomu plic", "Karcinomu prostaty", "Benigních nádorů"], "spravna": "a"
    },
    {
        "id": 7, "otazka": "Co znamenají 4R radiobiologie?",
        "moznosti": ["Reparace, redistribuce, reoxygenace, repopulace", "Reakce, regenerace, reoperace, rehydratace", "Reparace, resekce, reoxygenace, redukce"], "spravna": "a"
    },
    {
        "id": 8, "otazka": "Kdy zahajujeme nutriční podporu u onkologického pacienta?",
        "moznosti": ["Až při těžké malnutrici", "Co nejdříve", "Není nutná"], "spravna": "b"
    },
    {
        "id": 9, "otazka": "Co je sekundární prevence?",
        "moznosti": ["Prevence vzniku nemoci", "Screening a včasný záchyt", "Léčba komplikací"], "spravna": "b"
    },
    {
        "id": 10, "otazka": "Co znamená afterloading v brachyterapii?",
        "moznosti": ["Manuální zavedení zdroje", "Automatické zavedení zdroje do katétrů", "Nepoužívá se"], "spravna": "b"
    },
    {
        "id": 11, "otazka": "Kde nejčastěji metastazuje karcinom prostaty?",
        "moznosti": ["Játra", "Kosti", "Plíce"], "spravna": "b"
    },
    {
        "id": 12, "otazka": "Jakou techniku radioterapie bychom nejspíše zvolili pro ozařování v oblasti hlavy a krku?",
        "moznosti": ["VMAT SIB", "2 protilehlá pole", "2 šikmá pole"], "spravna": "a"
    }
]

# 2. INICIALIZACE STAVU APLIKACE (PAMĚŤ)
if "aktualni_otazka" not in st.session_state:
    st.session_state.aktualni_otazka = 0
if "skore" not in st.session_state:
    st.session_state.skore = 0
if "odpovezeno" not in st.session_state:
    st.session_state.odpovezeno = False

# Hlavní nadpis aplikace
st.title("🩺 Onkologický & Radioterapeutický Kvíz")

celkem_otazek = len(OTAZKY)
index = st.session_state.aktualni_otazka

# 3. ZOBRAZENÍ KVÍZU (Pokud nejsme na konci)
if index < celkem_otazek:
    aktualni = OTAZKY[index]
    
    # Indikátor postupu (Progress Bar)
    procento_hotovo = index / celkem_otazek
    st.progress(procento_hotovo, text=f"Otázka {index + 1} z {celkem_otazek}")
    
    # Stylový kontejner pro samotnou otázku
    with st.container(border=True):
        st.markdown(f"### {aktualni['otazka']}")
        
        # Formátování odpovědí do st.radio
        volby = [
            f"a) {aktualni['moznosti']}",
            f"b) {aktualni['moznosti']}",
            f"c) {aktualni['moznosti']}"
        ]
        
        vyber = st.radio(
            "Vyberte správnou odpověď:",
            volby,
            index=None,
            key=f"radio_{index}",
            disabled=st.session_state.odpovezeno
        )
        
        # Tlačítko pro ověření odpovědi
        if vyber and not st.session_state.odpovezeno:
            if st.button("Potvrdit odpověď", type="primary"):
                st.session_state.odpovezeno = True
                pismeno_volby = vyber[0] # Vezme první znak ('a', 'b', nebo 'c')
                
                if pismeno_volby == aktualni["spravna"]:
                    st.session_state.skore += 1
                st.rerun()

        # Zobrazení výsledku po potvrzení
        if st.session_state.odpovezeno:
            pismeno_volby = vyber[0] if vyber else ""
            if pismeno_volby == aktualni["spravna"]:
                st.success("✅ Správně!")
            else:
                st.error(f"❌ Špatně! Správná odpověď byla: **{aktualni['spravna']})**")
            
            # Tlačítko pro posun na další otázku
            if st.button("Další otázka ➡️"):
                st.session_state.aktualni_otazka += 1
                st.session_state.odpovezeno = False
                st.rerun()

# 4. ZOBRAZENÍ KONEČNÉHO VÝSLEDKU
else:
    st.balloons() # Efekt padajících balónků při dokončení
    st.header("🎯 Kvíz úspěšně dokončen!")
    
    skore = st.session_state.skore
    
    # Výpočet známky podle vaší stupnice
    if skore >= 11:
        znamka = "1 ⭐"
    elif skore >= 9:
        znamka = "2 👍"
    elif skore >= 7:
        znamka = "3 🙂"
    elif skore >= 5:
        znamka = "4 ⚠️"
    else:
        znamka = "5 ❌"
        
    # Stylové zobrazení výsledků
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="Dosažené skóre", value=f"{skore} / {celkem_otazek}")
    with col2:
        st.metric(label="Výsledná známka", value=znamka)
        
    # Tlačítko pro restart kvízu
    if st.button("Spustit kvíz znovu 🔄"):
        st.session_state.aktualni_otazka = 0
        st.session_state.skore = 0
        st.session_state.odpovezeno = False
        st.rerun()
