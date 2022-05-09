import streamlit as st
import pandas as pd

#import gpdvega
st.title('INDICE DE DYNAMISME DES COMMUNES')
st.text('IDAIA')

DATA_URL = (r"https://github.com/jroborel/streamlit-app/blob/main/scores_idcc1.csv?raw=true")

@st.cache(allow_output_mutation=True)
def load_data(URL):
    data = pd.read_csv(URL)
    for i in range(2,21):
        url = fr"https://github.com/jroborel/streamlit-app/blob/main/scores_idcc{i}.csv?raw=true"
        append = pd.read_csv(url)
        data = data.append(append)
    data.drop(columns='geometry',inplace=True)
    return data



data = load_data(DATA_URL)
st.set_option('deprecation.showPyplotGlobalUse', False)


zones= {
    'LA REGION':'NOM_REG',
    "LA ZONE D'EMPLOI":'LIBZE2020',
    "L'AIRE D'ATTRACTION":"LIBAAV2020"
}
with st.sidebar:
    st.write("INDICE COMMUNAL")
    input = st.text_input('Tapez un nom de commune :', value="Bruges", max_chars=None, key=None, type="default",
                          help=None, autocomplete=None, on_change=None, args=None,
                          kwargs=None, placeholder=None, disabled=False
                          )
    selected = st.selectbox('Choisissez une commune:', data[data.NOM_COM_M.str.contains(input.upper())].NOM_COM_M,
                            index=0, key=None, help=None, on_change=None,
                            args=None, kwargs=None, disabled=False
                            )
    zonage = st.selectbox('Choisissez une aire:', list(zones.keys()),
                            index=0, key=None, help=None, on_change=None,
                            args=None, kwargs=None, disabled=False
                            )

def choix_commune(df,input,aire):

    zone_com = df[df.NOM_COM_M==input][zones[aire]].values[0]
    zone = df[df[zones[aire]]==zone_com]
    return zone

zone = choix_commune(data,selected,zonage)
with st.container() :
    col1, col2 = st.columns(2)
    with col1:
        st.subheader(f"SCORE DE LA COMMUNE")
        st.write(str(int(data[data.NOM_COM_M==selected]['SCORE'].values[0])))

    with col2:
        st.subheader(f"SCORE MOYEN DE {zonage}")
        st.write(str(int(zone.SCORE.mean())))

st.write(data[data.NOM_COM_M==selected][list(data.columns[:-4])])
st.subheader(f'SCORE DES 10 MEILLEURS SCORES DE {zonage}')
st.write(zone.sort_values(by='POPULATION',ascending=False).iloc[:11])
