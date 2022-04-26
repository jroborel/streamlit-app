import streamlit as st
import geopandas as gpd

#import gpdvega
st.title('INDICE DE DYNAMISME DES COMMUNES')
st.text('IDAIA')

DATA_URL = (r"https://github.com/jroborel/streamlit-app/blob/main/scores_idcc1.shp")

def load_data(URL):
    data = gpd.read_file(URL)
    for i in range(2,7):
        url = fr"https://github.com/jroborel/streamlit-app/blob/main/scores_idcc{i}.shp"
        append = gpd.read_file(url)
        data = data.append(append)
    #data.geometry = data.geometry.apply(orient, args=(-1,))
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
    input = st.text_input('Tapez un nom de commune :', value="Bordeaux", max_chars=None, key=None, type="default",
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
with st.container() :
    st.subheader(f'LES 20 MEILLEURES COMMUNES DE {zonage}')
    best = zone.sort_values(by='SCORE').iloc[-21:]
    gdf = gpd.GeoDataFrame(
    best, geometry=best.geometry.centroid)
    world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
    ax = zone.plot(
    column='SCORE',legend=True)
    ax.set_axis_off()
    gdf.plot(ax=ax, color='red')
    st.pyplot()

with st.container() :
    st.write(best[list(best.columns[:-4])])
