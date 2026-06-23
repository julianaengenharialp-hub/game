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
    
    itens disponíveis = options_map[st.session_state.personagem]
    item_escolhido = st.radio("Escolha seu item de sobrevivência:", itens disponíveis)
    
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
            
            # Mapeamento de resultados idêntico ao seu jogo original
            outcomes_map = {
                ('mago', 'adaga', 'esquerda'): ["Com sua adaga mística, você desvia de armadilhas mágicas e encontra uma antiga inscrição com um enigma.", "A adaga do mago brilhou, revelando um caminho que leva a um teste de intelecto."],
                ('mago', 'adaga', 'direita'): ["A adaga do mago não foi páreo para o golem de pedra. Mas o golem parece interessado em uma charada...", "Sua adaga mágica se quebra al tentar abrir uma porta proibida, mas o feitiço que te possui o desafia com perguntas."],
                ('mago', 'adaga', 'meio'): ["Usando sua adaga para canalizar energia, você abre um portal para uma câmara com desafios mentais!", "A adaga mágica serve como chave para um cofre lendário, mas ele exige respostas para ser aberto."],
                ('mago', 'poção mágica', 'esquerda'): ["Você bebe a poção mágica e se torna intangível, passando pelas paredes para uma sala cheia de charadas!", "A poção mágica revela um mapa invisível que leva a um teste de inteligência."],
                ('mago', 'poção mágica', 'direita'): ["A poção mágica te transforma em um sapo. Um slime gigante te come, mas você ouve uma voz: 'Responda para se libertar!'", "A poção mágica faz você levitar até o teto, onde fica preso para sempre... a menos que responda a três perguntas difíceis."],
                ('mago', 'poção mágica', 'meio'): ["A poção mágica abre uma passagem secreta para um jardim encantado, mas para atravessá-lo você deve responder a um oráculo!", "Ao derramar a poção na porta do meio, ela se desintegra, revelando uma série de pergaminhos com perguntas."],
                ('guerreiro', 'espada', 'esquerda'): ["Com sua espada afiada, você corta as videiras que bloqueiam a porta e encontra um guardião que só responde a perguntas!", "Sua espada lendária repele um bando de lobos famintos, mas a saída está trancada por uma fechadura que exige um código (de perguntas)."],
                ('guerreiro', 'espada', 'direita'): ["Sua espada se prende na rocha e um ogro te esmaga, mas ele te oferece uma chance de escapar se responder às suas charadas!", "Você tenta derrubar a porta com a espada, mas ela vibra e explode, revelando um espírito que te desafia em um duelo de inteligência."],
                ('guerreiro', 'espada', 'meio'): ["Com sua espada, você derrota um cavaleiro espectral e reivindica um baú de tesouros, mas ele está selado por um feitiço que exige respostas!", "Sua espada corta um selo mágico na porta, revelando uma sala do tesouro de um antigo rei, protegida por enigmas."],
                ('guerreiro', 'lança', 'esquerda'): ["Com la lança, você desarma um mecanismo à distância e a porta se abre para uma sala de testes!", "Sua lança é perfeita para alcançar uma alavanca escondida, liberando uma saída secreta, mas um espectro surge com perguntas."],
                ('guerreiro', 'lança', 'direita'): ["A lança não serve contra os escorpiões gigantes. Você é picado, mas um ancião aparece e diz que sua vida será poupada se você responder a seus enigmas!", "Você tenta usar a lança para forçar a porta, mas ela ativa uma armadilha de espinhos que te empala, porém uma voz misteriosa oferece uma chance de escapar com perguntas."],
                ('guerreiro', 'lança', 'meio'): ["Você usa a lança para perfurar um dragão adormecido que guarda um tesouro colossal, mas o dragão te desafia com enigmas antes de ceder!", "A ponta da lança ativa um hieróglifo, revelando um salão do tesouro há muito esquecido, que exige a resolução de charadas."],
                ('lavrador', 'machado', 'esquerda'): ["Com o machado, você derruba a porta de madeira velha e encontra uma sala com um velho sábio que propõe desafios!", "Seu machado de lavrador é surpreendentemente eficaz para cortar as raízes que bloqueiam o caminho para a liberdade, mas um duende exigente aparece com perguntas."],
                ('lavrador', 'machado', 'direita'): ["O machado ricocheteia e atinge sua própria cabeça, mas você acorda com uma série de perguntas sobre a masmorra, a única forma de acordar de verdade!", "Você tenta cortar um barril suspeito com o machado, mas ele explode em gás tóxico. Uma figura sombria oferece um antídoto em troca de respostas."],
                ('lavrador', 'machado', 'meio'): ["Você usa o machado para quebrar um barril, encontrando um mapa para um tesouro escondido, mas o mapa contém enigmas que precisam ser resolvidos!", "O machado é a ferramenta ideal para quebrar uma parede frágil, revelando uma pequena câmara com moedas de ouro, mas para abri-la, você precisa responder a um guardião."],
                ('lavrador', 'pá', 'esquerda'): ["Com a pá, você escava um túnel sob a porta e rasteja para uma câmara com um quebra-cabeça de terra!", "A pá é a chave para desenterrar uma passagem oculta que leva para fora da masmorra, mas um espírito da terra te desafia com perguntas."],
                ('lavrador', 'pá', 'direita'): ["Você tenta cavar sob a porta, mas o chão cede e você cai em um abismo sem fim! Uma voz ecoa: 'Sua única esperança são as minhas charadas!'", "A pá não consegue remover as pedras que bloqueiam a porta, mas uma mensagem secreta surge na parede oferecendo uma chance com perguntas."],
                ('lavrador', 'pá', 'meio'): ["Com a pá, você desenterrar um baú de tesouros enterrado sob a porta do meio, mas ele só abre com a resposta para um enigma antigo!", "A pá do lavrador se revela útil para escavar um local marcado 'X' no chão, onde um tesouro espera, mas um gnome guardião exige respostas."]
            }
            
            chave = (st.session_state.personagem, st.session_state.item, st.session_state.porta)
            if chave in outcomes_map:
                st.session_state.resultado_texto = random.choice(outcomes_map[chave])
                # Prepara e embaralha as perguntas para a próxima fase
                perguntas_jogo = dungeon_questions.copy()
                random.shuffle(perguntas_jogo)
                st.session_state.perguntas = perguntas_jogo
                st.session_state.passo = 'perguntas'
                st.rerun()
            else:
                st.session_state.resultado_texto = "Um erro bizarro acontece e você é teleportado para uma dimensão de gelatina."
                st.session_state.status_final = 'derrota'
                st.session_state.passo = 'fim'
                st.rerun()

# --- PASSO 4: FASE DE PERGUNTAS ---
elif st.session_state.passo == 'perguntas':
    st.write(st.session_state.resultado_texto)
    st.write("---")
    st.write("### 🧠 Desafio de Inteligência")
    st.write(f"Você precisa responder corretamente a **2 perguntas** para escapar. Limite de 10 tentativas.")
    st.write(f"Progresso atual: **{st.session_state.acertos} / 2 acertos** | Tentativa atual: **{st.session_state.idx_pergunta + 1} de 10**")
    
    # Pega a pergunta atual baseado no índice mestre
    q_atual = st.session_state.perguntas[st.session_state.idx_pergunta]
    
    st.info(q_atual['question'])
    resposta_usuario = st.radio("Sua resposta:", ["sim", "não"], key=f"req_{st.session_state.idx_pergunta}")
    
    if st.button("Enviar Resposta"):
        if resposta_usuario == q_atual['answer']:
            st.success(q_atual['feedback_correct'])
            st.session_state.acertos += 1
        else:
            st.error(q_atual['feedback_incorrect'])
            
        # Atualiza contadores
        st.session_state.idx_pergunta += 1
        
        # Verifica condições de vitória ou derrota
        if st.session_state.acertos >= 2:
            st.session_state.status_final = 'vitoria'
            st.session_state.passo = 'fim'
        elif st.session_state.idx_pergunta >= 10:
            st.session_state.status_final = 'derrota'
            st.session_state.passo = 'fim'
            
        st.button("Continuar") # Botão apenas para recarregar a tela e processar o fluxo

# --- PASSO 5: TELA DE FINAL DE JOGO ---
elif st.session_state.passo == 'fim':
    if st.session_state.status_final == 'vitoria':
        st.balloons()
        st.success(f"🎉 Parabéns, {st.session_state.jogador_nome}! Você respondeu às perguntas corretamente e provou seu intelecto. A masmorra se revela e você encontra a liberdade!")
    else:
        st.error(f"💀 Game Over, {st.session_state.jogador_nome}. A masmorra não revelou seus segredos e você está perdido para sempre.")
        
    if st.button("Jogar Novamente 🔄"):
        # Reseta todas as variáveis para recomeçar
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()