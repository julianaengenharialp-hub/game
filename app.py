# --- PASSO 2: ESCOLHA DO ITEM ---
elif st.session_state.passo == 'item':
    st.write(f"### Bem-vindo(a), {st.session_state.jogador_nome}! Sua jornada começa agora.")
    st.write(f"Você escolheu a classe: **{st.session_state.personagem.capitalize()}**")
    
    options_map = {
        'mago': ["Adaga", "Poção Mágica"],
        'guerreiro': ["Espada", "Lança"],
        'lavrador': ["Machado", "Pá"]
    }
    
    # CORREÇÃO AQUI: Nome da variável alterado para "itens_disponiveis"
    itens_disponiveis = options_map[st.session_state.personagem]
    item_escolhido = st.radio("Escolha seu item de sobrevivência:", itens_disponiveis)
    
    if st.button("Confirmar Item"):
        st.session_state.item = item_escolhido.lower()
        st.session_state.passo = 'masmorra'
        st.rerun()