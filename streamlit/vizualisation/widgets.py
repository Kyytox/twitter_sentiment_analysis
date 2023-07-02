import streamlit as st

# element selector radio for the frequency of the graph
def _get_freq_option(index):
    lst_options = ['par jour', 'tout les 3 jours', 'par semaine', 'par mois']    
    freq_option = st.radio('Fréquence de temps :', lst_options, index=0, horizontal=True, key=index)

    print("freq_option", freq_option)

    # use match case to select the frequency of the graph
    if freq_option == 'par jour':
        return 'D'
    elif freq_option == 'tout les 3 jours':
        return '3D'
    elif freq_option == 'par semaine':
        return 'W'
    elif freq_option == 'par mois':
        return 'M'
    else:
        return 'D'
