import streamlit as st
import random

# Configuração inicial da página
st.set_page_config(page_title="Jogo da Masmorra", page_icon="🎮")

st.title("🎮 A Jornada na Masmorra")

# --- INICIALIZAÇÃO DA MEMÓRIA DO JOGO (Session State) ---
if 'passo' not in st.session_state:
    st.session_state.passo = 'inicio'  # Passos: inicio, item, masmorra, perguntas, fim
if 'jogador_nome' not in st.session_state:
    st.session_state.jogador_nome = ''
if 'personagem' not in st.session_state:
    st.session_state.personagem = ''
if 'item' not in st.session_state:
    st.session_state.item = ''
if 'porta' not in st.session_state:
    st.session_state.porta = ''
if 'perguntas' not in st.session_state:
    st.session_state.perguntas = []
if 'idx_pergunta' not in st.session_state:
    st.session_state.idx_pergunta = 0
if 'acertos' not in st.session_state:
    st.session_state.acertos = 0
if 'resultado_texto' not in st.session_state:
    st.session_state.resultado_texto = ''
if 'status_final' not in st.session_state:
    st.session_state.status_final = '' # 'vitoria' ou 'derrota'

# Banco de dados de perguntas do jogo original
dungeon_questions = [
    {'question': 'Você pode ver o céu da masmorra? (sim/não)', 'answer': 'não', 'feedback_correct': 'Correto! A masmorra é subterrânea e sem aberturas diretas.', 'feedback_incorrect': 'Errado! Você está muito abaixo da superfície, o céu é apenas uma memória.'},
    {'question': 'Você sente cheiro de ar fresco? (sim/não)', 'answer': 'não', 'feedback_correct': 'Certo! O ar aqui é abafado e antigo, com cheiro de mofo e terra.', 'feedback_incorrect': 'Incorreto! O ar da masmorra é pesado e estagnado, não há brisa fresca.'},
    {'question': 'Você pode ouvir o som de água corrente? (sim/não)', 'answer': 'sim', 'feedback_correct': 'Excelente! Goteiras e rios subterrâneos são comuns em masmorras, indicando vida e umidade.', 'feedback_incorrect': 'Não! O silêncio é quase total aqui, apenas o som distante de seus próprios passos.'},
    {'question': 'Existem criaturas que brilham na escuridão aqui? (sim/não)', 'answer': 'sim', 'feedback_correct': 'Boa! Fungos bioluminescentes, insetos estranhos e até olhos curiosos vivem nestas profundezas.', 'feedback_incorrect': 'Não! A escuridão é absoluta, sem qualquer ponto de luz natural ou criaturas brilhantes.'},
    {'question': 'A masmorra foi construída exclusivamente por humanos? (sim/não)', 'answer': 'não', 'feedback_correct': 'Genial! Muitas masmorras são formações naturais, obras de anões, elfos sombrios ou até criaturas mais antigas.', 'feedback_incorrect': 'Pense de novo! Esta masmorra tem uma origem mais antiga ou mística que a humanidade.'},
    {'question': 'Você pode encontrar ouro nas paredes da masmorra exposto? (sim/não)', 'answer': 'não', 'feedback_correct': 'Isso mesmo! O ouro geralmente está guardado em tesouros, não exposto nas paredes como um minério comum.', 'feedback_incorrect': 'Infelizmente não! Se fosse tão fácil, a masmorra já teria sido saqueada.'},
    {'question': 'Existem árvores vivas crescendo dentro da masmorra? (sim/não)', 'answer': 'não', 'feedback_correct': 'Correto! Poucas plantas sobrevivem na falta de luz solar e solo fértil.', 'feedback_incorrect': 'Não! Este é um ambiente fechado e hostil para a maioria da vida vegetal.'},
    {'question': 'A temperatura geral da masmorra é quente? (sim/não)', 'answer': 'não', 'feedback_correct': 'Exato! Masmorras são geralmente frias, úmidas e com temperaturas constantes.', 'feedback_incorrect': 'Não! O frio é constante e úmido, raramente há calor.'},
    {'question': 'Você pode respirar facilmente na maioria das áreas? (sim/não)', 'answer': 'sim', 'feedback_correct': 'Sim, por enquanto! O ar é denso, mas geralmente respirável em áreas abertas.', 'feedback_incorrect': 'Você está com dificuldades então! O ar é rarefeito em alguns pontos.'},
    {'question': 'A saída está a apenas alguns passos de distância? (sim/não)', 'answer': 'não', 'feedback_correct': 'Correto! A fuga requer esforço e inteligência. É uma jornada!', 'feedback_incorrect': 'Engano seu! A masmorra é vasta e cheia de perigos.'}
]

# --- PASSO 1: TELA DE INÍCIO (Nome e Personagem) ---
if st.session_state.passo == 'inicio':
    nome = st.text_input("Olá aventureiro! Qual é o seu nome?")
    
    st.write("### Primeiro, escolha seu destino! Que tipo de aventureiro você é?")
    personagem = st.selectbox("Escolha seu personagem:", ["", "Mago", "Guerreiro", "Lavrador"])
    
    if st.button("Iniciar Jornada"):
        if nome.strip() == "" or personagem == "":
            st.warning("Por favor, digite seu nome e escolha um personagem!")
        else:
            st.session_state.jogador_nome = nome
            st.session_state.personagem = personagem.lower()
            st.session_state.passo = 'item'
            st.rerun()

# --- PASSO 2: ESCOLHA DO ITEM ---
elif st.session_state.passo == 'item':
    st.write(f"### Bem-vindo(a), {st.session_state.jogador_nome}! Sua jornada começa agora.")
    st.write(f"Você escolheu a classe: **{st.session_state.personagem.capitalize()}**")
    
    options_map = {
        'mago': ["Adaga", "Poção Mágica"],
        'guerreiro': ["Espada", "Lança"],
        'lavrador': ["Machado", "Pá"]
    }
    
    itens_disponiveis = options_map[st.session_state.personagem]
    item_escolhido = st.radio("Escolha seu item de sobrevivência:", itens_disponiveis)
    
    if st.button("Confirmar Item"):
        st.session_state.item = item_escolhido.lower()
        st.session_state.passo = 'masmorra'
        st.rerun()

# --- PASSO 3: A MASMORRA E AS PORTAS ---
elif st.session_state.passo == 'masmorra':
    st.info(f"Você empunha sua {st.session_state.item}. Ótima escolha, {st.session_state.personagem.capitalize()} {st.session_state.jogador_nome}!")
    
    st.write("---")
    st.write("Você se encontra em uma masmorra escura e fria. Há três portas à sua frente.")
    st.write("Uma é a **Porta Esquerda**, outra é a **Porta Direita** e uma terceira é a **Porta do Meio**.")
    
    porta = st.selectbox("Qual porta você escolhe?", ["", "Esquerda", "Direita", "Meio"])
    
    if st.button("Abrir Porta"):
        if porta == "":
            st.warning("Escolha uma porta para prosseguir!")
        else:
            st.session_state.porta = porta.lower()
            
            outcomes_map = {
                ('mago', 'adaga', 'esquerda'): ["Com sua adaga mística, você desvia de armadilhas mágicas e encontra uma antiga inscrição com um enigma.", "A adaga do mago brilhou, revelando um caminho que leva a um teste de intelecto."],
                ('mago', 'adaga', 'direita'): ["A adaga do mago não foi páreo para o golem de pedra. Mas o golem parece interessado em uma charada...", "Sua adaga mágica se quebra ao tentar abrir uma porta proibida, mas o feitiço que te possui o desafia com perguntas."],
                ('mago', 'adaga', 'meio'): ["Usando sua adaga para canalizar energia, você abre um portal para uma câmara com desafios mentais!", "A adaga mágica serve como chave para um cofre lendário, mas ele exige respostas para ser aberto."],
                ('mago', 'poção mágica', 'esquerda'): ["Você bebe a poção mágica e se torna intangível, passando pelas paredes para uma sala cheia de charadas!", "A poção mágica reveals um mapa invisível que leva a um teste de inteligência."],
                ('mago', 'poção mágica', 'direita'): ["A poção mágica te transforma em um sapo. Um slime gigante te come, mas você ouve uma voz: 'Responda para se libertar!'", "A poção mágica faz você levitar até o teto, onde fica preso para sempre... a menos que responda a três perguntas difíceis."],
                ('mago', 'poção mágica', 'meio'):