import streamlit as st
import json
import requests
from datetime import datetime

# Configuração da página
st.set_page_config(
    page_title="MuscleGainer App",
    page_icon="💪",
    layout="wide"
)

# Estilo CSS personalizado
st.markdown("""
<style>
    .main {
        padding: 2rem;
    }
    .title {
        font-size: 2.5rem;
        font-weight: bold;
        color: #3366cc;
        margin-bottom: 2rem;
        text-align: center;
    }
    .subtitle {
        font-size: 1.5rem;
        color: #555;
        margin-bottom: 1rem;
    }
    .info-box {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
    .result-section {
        background-color: #e6f3ff;
        padding: 1.5rem;
        border-radius: 10px;
        margin-top: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# Função para gerar recomendações usando LLM
def gerar_recomendacao_llm(dados_usuario, tipo_recomendacao):
    try:
        prompt = f"""
        Com base nos seguintes dados do usuário:
        - Sexo: {dados_usuario['sexo']}
        - Idade: {dados_usuario['idade']} anos
        - Peso: {dados_usuario['peso']} kg
        - Altura: {dados_usuario['altura']} cm
        - Medidas dos membros: {dados_usuario['medidas']}
        - Áreas de foco: {', '.join(dados_usuario['membros_foco'])}
        - Preferência de treino: {dados_usuario['tipo_treino']}
        
        Por favor, gere uma {tipo_recomendacao} detalhada e personalizada para ganho de massa muscular.
        """
        
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": "Bearer " + st.secrets["qwen_key"],
                "Content-Type": "application/json",
                "HTTP-Referer": "https://musclegainer.com",
                "X-Title": "MuscleGainer",
            },
            data=json.dumps({
                "model": "qwen/qwen2.5-vl-72b-instruct:free",
                "messages": [
                    {"role": "system", "content": "Você é um especialista em nutrição esportiva e treinamento para hipertrofia. Forneça recomendações detalhadas, específicas e personalizadas."},
                    {"role": "user", "content": prompt},
                ],
            })
        )
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        st.error(f"Erro ao gerar recomendação: {str(e)}")
        # Fallback para recomendações básicas em caso de erro na API
        if tipo_recomendacao == "dieta":
            return gerar_dieta_fallback(dados_usuario)
        else:
            return gerar_treino_fallback(dados_usuario)

# Funções de fallback para quando a API falhar
def gerar_dieta_fallback(dados_usuario):
    sexo = dados_usuario['sexo']
    peso = dados_usuario['peso']
    
    calorias = int(peso * (37 if sexo == "Masculino" else 35))
    proteina = int(peso * 2)
    carbs = int(peso * 4)
    gordura = int(peso * 1)
    
    return f"""
    ## Recomendação Básica de Dieta para Ganho de Massa
    
    ### Calorias diárias: {calorias} kcal
    - Proteínas: {proteina}g ({proteina * 4} kcal)
    - Carboidratos: {carbs}g ({carbs * 4} kcal)
    - Gorduras: {gordura}g ({gordura * 9} kcal)
    
    ### Distribuição das refeições:
    1. **Café da manhã**: Rica em proteínas e carboidratos
    2. **Lanche da manhã**: Proteína e gorduras boas
    3. **Almoço**: Proteína, carboidratos complexos e vegetais
    4. **Lanche da tarde**: Proteína e carboidratos
    5. **Pré-treino**: Carboidratos rápidos e proteína
    6. **Pós-treino**: Proteína e carboidratos rápidos
    7. **Jantar**: Proteína e vegetais
    
    ### Alimentos recomendados:
    - **Proteínas**: frango, peixe, carne vermelha magra, ovos, whey protein
    - **Carboidratos**: arroz, batata doce, aveia, quinoa, frutas
    - **Gorduras**: azeite, abacate, castanhas, sementes
    
    Hidrate-se bem! Beba pelo menos 35ml de água por kg de peso corporal.
    """

def gerar_treino_fallback(dados_usuario):
    tipo_treino = dados_usuario['tipo_treino']
    membros_foco = dados_usuario['membros_foco']
    
    treino = "## Programa de Treino Básico para Hipertrofia\n\n"
    
    if tipo_treino == "Com aparelhos":
        treino += """
        ### Divisão de treino recomendada:
        - **Segunda**: Peito e Tríceps
        - **Terça**: Costas e Bíceps
        - **Quarta**: Descanso ou Cardio leve
        - **Quinta**: Pernas, Glúteos e Ombros
        - **Sexta**: Treino dos grupos que deseja focar mais
        - **Sábado/Domingo**: Descanso
        
        ### Princípios gerais:
        - 3-4 exercícios por grupo muscular
        - 3-4 séries por exercício
        - 8-12 repetições (foco em hipertrofia)
        - Descanso de 60-90 segundos entre séries
        - Treino com intensidade entre 70-85% de 1RM
        """
    else:
        treino += """
        ### Divisão de treino recomendada:
        - **Segunda**: Empurrar (peito, ombros, tríceps)
        - **Terça**: Puxar (costas, bíceps)
        - **Quarta**: Descanso ou Cardio leve
        - **Quinta**: Pernas, Glúteos e Core
        - **Sexta**: Circuito full body com foco nos grupos prioritários
        - **Sábado/Domingo**: Descanso
        
        ### Princípios gerais:
        - Utilizar o peso corporal e resistência progressiva
        - Variar o tempo sob tensão e ângulos de execução
        - 3-4 séries por exercício
        - 8-15 repetições (foco em hipertrofia)
        - Descanso de 60-90 segundos entre séries
        """
    
    for membro in membros_foco:
        treino += f"\n### Exercícios específicos para {membro}:\n"
        if membro == "Peito":
            if tipo_treino == "Com aparelhos":
                treino += "- Supino reto com barra\n- Crucifixo com halteres\n- Supino inclinado na máquina\n- Crossover no cabo"
            else:
                treino += "- Flexões com variações\n- Flexões declinadas\n- Flexões diamante\n- Dips entre cadeiras"
        elif membro == "Costas":
            if tipo_treino == "Com aparelhos":
                treino += "- Puxada na frente\n- Remada curvada\n- Pulldown\n- Remada unilateral com halter"
            else:
                treino += "- Barras\n- Remadas invertidas\n- Superman\n- Remada com elástico"
        elif membro == "Pernas":
            if tipo_treino == "Com aparelhos":
                treino += "- Agachamento com barra\n- Leg press\n- Cadeira extensora\n- Mesa flexora"
            else:
                treino += "- Agachamentos\n- Afundos\n- Stiff com peso corporal\n- Bulgarian split squat"
        elif membro == "Braços":
            if tipo_treino == "Com aparelhos":
                treino += "- Rosca direta\n- Rosca scott\n- Tríceps corda\n- Tríceps francês"
            else:
                treino += "- Rosca com elástico\n- Dips para tríceps\n- Flexões diamante\n- Rosca martelo com garrafa pet"
        elif membro == "Ombros":
            if tipo_treino == "Com aparelhos":
                treino += "- Desenvolvimento com halteres\n- Elevação lateral\n- Face pull\n- Desenvolvimento arnold"
            else:
                treino += "- Pike push-ups\n- Elevação lateral com garrafas\n- Elevação frontal com objetos\n- Flexões em Y"
        elif membro == "Glúteos":
            if tipo_treino == "Com aparelhos":
                treino += "- Hip thrust com barra\n- Abdução de quadril na máquina\n- Elevação pélvica\n- Coice na polia"
            else:
                treino += "- Hip thrust com peso corporal\n- Ponte de glúteos\n- Elevação de quadril unilateral\n- Fire hydrant (hidrante)"
    
    return treino

# Inicialização de variáveis de estado
if 'generate_results' not in st.session_state:
    st.session_state['generate_results'] = False

# Título principal
st.markdown('<div class="title">MuscleGainer App</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Seu assistente pessoal para ganho de massa muscular</div>', unsafe_allow_html=True)

# Criar abas
tab1, tab2 = st.tabs(["Informações do Usuário", "Resultados"])

with tab1:
    st.markdown("## Insira seus dados")
    
    col1, col2 = st.columns(2)
    
    with col1:
        sexo = st.selectbox("Sexo:", ["Masculino", "Feminino"])
        idade = st.number_input("Idade:", min_value=16, max_value=80, value=30)
        peso = st.number_input("Peso (kg):", min_value=40.0, max_value=150.0, value=70.0, step=0.1)
        altura = st.number_input("Altura (cm):", min_value=140, max_value=220, value=170)
    
    with col2:
        st.markdown("### Medidas dos membros (cm)")
        bracos = st.number_input("Braços (circunferência):", min_value=20.0, max_value=60.0, value=30.0, step=0.5)
        peito = st.number_input("Peito (circunferência):", min_value=70.0, max_value=150.0, value=90.0, step=0.5)
        cintura = st.number_input("Cintura (circunferência):", min_value=60.0, max_value=150.0, value=80.0, step=0.5)
        quadril = st.number_input("Quadril (circunferência):", min_value=70.0, max_value=150.0, value=95.0, step=0.5)
        coxas = st.number_input("Coxas (circunferência):", min_value=40.0, max_value=100.0, value=55.0, step=0.5)
        gluteos = st.number_input("Glúteos (circunferência):", min_value=70.0, max_value=150.0, value=100.0, step=0.5)
        
    st.markdown("### Objetivos")
    membros_foco = st.multiselect(
        "Quais áreas você deseja focar?",
        ["Peito", "Costas", "Pernas", "Braços", "Ombros", "Glúteos"],
        default=["Peito", "Braços"]
    )
    
    tipo_treino = st.radio(
        "Preferência de treino:",
        ["Com aparelhos", "Sem aparelhos (calistenia, elásticos, etc.)"]
    )
    
    nivel_experiencia = st.select_slider(
        "Nível de experiência:",
        options=["Iniciante", "Intermediário", "Avançado"]
    )
    
    dias_treino = st.slider("Quantos dias por semana você pode treinar?", 2, 6, 4)
    
    restricoes_alimentares = st.multiselect(
        "Restrições alimentares:",
        ["Nenhuma", "Vegetariano", "Vegano", "Intolerância à lactose", "Celíaco/Sem glúten"],
        default=["Nenhuma"]
    )
    
    medicoes = {
        "Braços": bracos,
        "Peito": peito,
        "Cintura": cintura,
        "Quadril": quadril,
        "Coxas": coxas,
        "Glúteos": gluteos
    }
    
    if st.button("Gerar Recomendações", type="primary"):
        # Salvando os dados do usuário
        dados_usuario = {
            "sexo": sexo,
            "idade": idade,
            "peso": peso,
            "altura": altura,
            "medidas": medicoes,
            "membros_foco": membros_foco,
            "tipo_treino": tipo_treino,
            "nivel": nivel_experiencia,
            "dias_treino": dias_treino,
            "restricoes": restricoes_alimentares
        }
        
        # Salvar na session state
        st.session_state['dados_usuario'] = dados_usuario
        st.session_state['generate_results'] = True
        st.session_state['dieta_recomendacao'] = None
        st.session_state['treino_recomendacao'] = None
        
        # Alterar para a aba de resultados automaticamente
        st.rerun()

with tab2:
    if 'generate_results' in st.session_state and st.session_state['generate_results']:
        dados_usuario = st.session_state['dados_usuario']
        
        st.markdown('<div class="subtitle">Suas recomendações personalizadas</div>', unsafe_allow_html=True)
        
        # Mostrar informações do usuário
        with st.expander("Resumo dos seus dados", expanded=False):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.write(f"**Sexo:** {dados_usuario['sexo']}")
                st.write(f"**Idade:** {dados_usuario['idade']} anos")
                st.write(f"**Peso:** {dados_usuario['peso']} kg")
                st.write(f"**Altura:** {dados_usuario['altura']} cm")
            
            with col2:
                st.write("**Medidas:**")
                for parte, medida in dados_usuario['medidas'].items():
                    st.write(f"- {parte}: {medida} cm")
            
            with col3:
                st.write(f"**Áreas de foco:** {', '.join(dados_usuario['membros_foco'])}")
                st.write(f"**Tipo de treino:** {dados_usuario['tipo_treino']}")
                st.write(f"**Nível:** {dados_usuario['nivel']}")
                st.write(f"**Dias de treino:** {dados_usuario['dias_treino']}")
        
        # IMC e outras métricas
        st.markdown('<div class="info-box">', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        
        # Cálculo do IMC
        imc = round(dados_usuario['peso'] / ((dados_usuario['altura']/100) ** 2), 2)
        
        with col1:
            st.subheader("Métricas")
            st.write(f"**IMC:** {imc}")
            
            if imc < 18.5:
                status_imc = "Abaixo do peso"
            elif imc < 25:
                status_imc = "Peso normal"
            elif imc < 30:
                status_imc = "Sobrepeso"
            else:
                status_imc = "Obesidade"
                
            st.write(f"**Status IMC:** {status_imc}")
            
            # Estimativa de BF% (muito simplificada)
            if dados_usuario['sexo'] == "Masculino":
                bf_est = round(1.20 * imc + 0.23 * dados_usuario['idade'] - 16.2, 1)
            else:
                bf_est = round(1.20 * imc + 0.23 * dados_usuario['idade'] - 5.4, 1)
                
            bf_est = max(5, min(bf_est, 40))  # limitar valores impossíveis
            st.write(f"**Gordura corporal estimada:** {bf_est}%")
            
        with col2:
            # Cálculo da taxa metabólica basal (TMB) usando fórmula de Harris-Benedict
            if dados_usuario['sexo'] == "Masculino":
                tmb = 88.362 + (13.397 * dados_usuario['peso']) + (4.799 * dados_usuario['altura']) - (5.677 * dados_usuario['idade'])
            else:
                tmb = 447.593 + (9.247 * dados_usuario['peso']) + (3.098 * dados_usuario['altura']) - (4.330 * dados_usuario['idade'])
                
            st.subheader("Necessidades Energéticas")
            st.write(f"**Taxa Metabólica Basal:** {int(tmb)} kcal")
            st.write(f"**Necessidade para ganho de massa:** {int(tmb * 1.5)} kcal")
            st.write(f"**Proteína diária recomendada:** {int(dados_usuario['peso'] * 2)}g")
            
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Abas para dieta e treino
        resultados_tab1, resultados_tab2 = st.tabs(["Plano Alimentar", "Programa de Treino"])
        
        with resultados_tab1:
            st.markdown('<div class="result-section">', unsafe_allow_html=True)
            
            with st.spinner("Gerando plano alimentar personalizado..."):
                if 'dieta_recomendacao' not in st.session_state or st.session_state['dieta_recomendacao'] is None:
                    st.session_state['dieta_recomendacao'] = gerar_recomendacao_llm(dados_usuario, "dieta")
                
                st.markdown(st.session_state['dieta_recomendacao'])
                
                # Opção para baixar a dieta
                dieta_texto = st.session_state['dieta_recomendacao']
                st.download_button(
                    label="Baixar Plano Alimentar",
                    data=dieta_texto,
                    file_name=f"plano_alimentar_{datetime.now().strftime('%Y%m%d')}.txt",
                    mime="text/plain"
                )
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        with resultados_tab2:
            st.markdown('<div class="result-section">', unsafe_allow_html=True)
            
            with st.spinner("Gerando programa de treino personalizado..."):
                if 'treino_recomendacao' not in st.session_state or st.session_state['treino_recomendacao'] is None:
                    st.session_state['treino_recomendacao'] = gerar_recomendacao_llm(dados_usuario, "programa de treino")
                
                st.markdown(st.session_state['treino_recomendacao'])
                
                # Opção para baixar o treino
                treino_texto = st.session_state['treino_recomendacao']
                st.download_button(
                    label="Baixar Programa de Treino",
                    data=treino_texto,
                    file_name=f"programa_treino_{datetime.now().strftime('%Y%m%d')}.txt",
                    mime="text/plain"
                )
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Dicas adicionais e considerações
        st.markdown("### Dicas importantes")
        st.info("""
            - **Consistência é a chave:** Siga o plano por pelo menos 8-12 semanas para ver resultados significativos.
            - **Progressão:** Aumente gradualmente a carga nos exercícios conforme sua força aumenta.
            - **Descanso:** Garanta 7-9 horas de sono por noite para maximizar a recuperação muscular.
            - **Hidratação:** Beba pelo menos 35ml de água por kg de peso corporal diariamente.
            - **Monitoramento:** Faça novas medidas a cada 4 semanas para acompanhar seu progresso.
        """)
        
        # Aviso sobre consulta profissional
        st.warning("""
            **Importante:** Este plano é uma sugestão baseada nas informações fornecidas. 
            Para resultados ótimos e seguros, consulte um nutricionista e um profissional de educação física.
        """)
    else:
        # Conteúdo para exibir quando o app é iniciado pela primeira vez
        st.info("👈 Por favor, preencha suas informações na aba 'Informações do Usuário' e clique em 'Gerar Recomendações' para visualizar seus resultados personalizados.")
        
        # Explicação sobre o aplicativo
        st.markdown("## Como funciona o MuscleGainer App")
        st.markdown("""
        Este aplicativo foi projetado para ajudar você a atingir seus objetivos de ganho de massa muscular, oferecendo:
        
        1. **Plano alimentar personalizado** - Com base nas suas características físicas e objetivos
        2. **Programa de treino específico** - Focado nos grupos musculares que você deseja desenvolver
        3. **Opções adaptáveis** - Com ou sem equipamentos de musculação
        4. **Métricas úteis** - Cálculos de IMC, gordura corporal estimada e necessidades calóricas
        
        Ao preencher seus dados na aba anterior, nosso sistema irá gerar recomendações personalizadas para você.
        """)
        
        # Informações adicionais
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Benefícios do ganho de massa muscular")
            st.markdown("""
            - Aumento da força e resistência física
            - Melhora do metabolismo e queima calórica
            - Prevenção de lesões e melhora da postura
            - Aumento da densidade óssea
            - Melhora da autoestima e confiança
            """)
        
        with col2:
            st.markdown("### Fatores importantes para hipertrofia")
            st.markdown("""
            - **Volume de treino adequado** - Número de séries e repetições
            - **Intensidade progressiva** - Aumento gradual das cargas
            - **Alimentação rica em proteínas** - Para reconstrução muscular
            - **Descanso adequado** - Recuperação entre treinos
            - **Consistência** - Manter a rotina a longo prazo
            """)
        
        # Informações sobre grupos musculares
        st.markdown("### Principais Grupos Musculares")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            #### Peito, Costas e Ombros
            O desenvolvimento destes músculos contribui para uma postura melhor e uma aparência mais larga e atlética.
            """)
        
        with col2:
            st.markdown("""
            #### Braços e Pernas
            Braços fortes e pernas desenvolvidas são fundamentais para um físico equilibrado e funcional, além de melhorar o desempenho em atividades diárias.
            """)
        
        with col3:
            st.markdown("""
            #### Glúteos
            Os glúteos são um dos maiores grupos musculares do corpo. Seu fortalecimento melhora a estabilidade pélvica, potência de salto e corrida, além dos benefícios estéticos.
            """)

# Rodapé
st.markdown("---")
st.markdown("MuscleGainer App | Desenvolvido para ajudar você a atingir seus objetivos de ganho de massa muscular")