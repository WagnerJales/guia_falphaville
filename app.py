import urllib.parse
import streamlit as st


st.title('Roteirização - Alphaville Paço do Lumiar/MA')

lot_number = st.text_input('Informe o número do lote')

if lot_number:
    destination = f"Lote {lot_number} Alphaville Paço do Lumiar Maranhão"
    encoded_dest = urllib.parse.quote(destination)
    maps_url = (
        f"https://www.google.com/maps/dir/?api=1&origin=My+Location&destination={encoded_dest}"
    )
    st.markdown(f'[Abrir rota no Google Maps]({maps_url})')

    api_key = st.secrets.get('google_maps_api_key')
    if api_key:
        iframe = (
            f"<iframe width='100%' height='450' src='https://www.google.com/maps/embed/v1/directions?key={api_key}&origin=My+Location&destination={encoded_dest}'></iframe>"
        )
        st.components.v1.html(iframe, height=450)
    else:
        st.info('Configure a chave da API do Google Maps para exibir o mapa incorporado.')
