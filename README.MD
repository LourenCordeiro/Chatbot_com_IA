# ChatBot de IA com Python e Streamlit

Chatbot com interface web feito em Python. Usa o **Streamlit** para a interface e o modelo **Gemini** (Google) para gerar as respostas, acessado pela biblioteca `openai` através do endpoint compatível do Google.

## Objetivo

Mostrar, de forma simples, como construir um chat com IA que:

- tem uma interface web de chat pronta, sem HTML/CSS;
- mantém o histórico da conversa durante a sessão;
- envia o contexto completo ao modelo, para que ele "lembre" do que foi dito antes.

## Tecnologias

| Tecnologia | Para que serve |
|---|---|
| [Streamlit](https://streamlit.io) | Transforma o script Python em uma página web |
| [openai](https://pypi.org/project/openai/) | Cliente HTTP para APIs de LLM no formato OpenAI |
| Gemini (`gemini-flash-lite-latest`) | Modelo de IA que gera as respostas |

## Como funciona

O ponto principal para entender o código: **o Streamlit roda o script inteiro de novo, do início, a cada interação do usuário**. Por isso o histórico fica guardado em `st.session_state`, um dicionário que sobrevive entre essas execuções.

Fluxo de uma mensagem:

1. O usuário digita algo no campo de chat.
2. O Streamlit reexecuta o script.
3. O histórico salvo é redesenhado na tela.
4. A nova mensagem é exibida e adicionada ao histórico.
5. O **histórico inteiro** é enviado ao Gemini (LLMs não têm memória entre chamadas).
6. A resposta é exibida e também salva no histórico.

## Explicação do código

### Cliente da IA

```python
modelo_ia = OpenAI(api_key=st.secrets["GEMINI_API_KEY"],
                   base_url="https://generativelanguage.googleapis.com/v1beta/openai")
```

A biblioteca é da OpenAI, mas o `base_url` aponta para o Google. O Gemini aceita requisições no mesmo formato da OpenAI, então o mesmo cliente funciona com outro provedor.

### Histórico da conversa

```python
if "lista_mensagens" not in st.session_state:
    st.session_state["lista_mensagens"] = []
```

Cria a lista de mensagens apenas na primeira execução. Nas seguintes, ela já existe e é mantida.

### Exibição do histórico

```python
for mensagem in st.session_state["lista_mensagens"]:
    st.chat_message(mensagem["role"]).write(mensagem["content"])
```

Cada mensagem é um dicionário como `{"role": "user", "content": "oi"}`. O `role` pode ser `"user"` (usuário) ou `"assistant"` (IA) e define o estilo do balão.

### Entrada do usuário

```python
mensagem_usuario = st.chat_input("Escreva sua mensagem aqui")
```

Retorna o texto quando o usuário envia, ou `None` caso contrário.

### Chamada ao modelo

```python
resposta_modelo = modelo_ia.chat.completions.create(
    messages=st.session_state["lista_mensagens"],
    model="gemini-flash-lite-latest",
)
resposta_ia = resposta_modelo.choices[0].message.content
```

Envia o histórico completo e extrai o texto da primeira resposta (`choices[0]`). A chamada é bloqueante: o script espera a resposta antes de continuar.

## Como obter a chave de acesso (API key) do Gemini

1. Acesse o **Google AI Studio**: https://aistudio.google.com/apikey
2. Faça login com sua conta Google.
3. Clique em **Create API key** (Criar chave de API).
4. Escolha um projeto do Google Cloud existente ou deixe o AI Studio criar um novo.
5. Copie a chave gerada.

> O Gemini tem um plano gratuito com limites de uso. Consulte os limites atuais na própria página do AI Studio.

### Cuidados com a chave

- **Nunca** escreva a chave diretamente no código.
- **Nunca** suba a chave para o GitHub. Quem tiver a chave pode usar sua cota (e gerar cobrança, se houver faturamento ativo).
- Se a chave vazar, apague-a no AI Studio e gere outra.

### Onde guardar a chave

Crie o arquivo `.streamlit/secrets.toml` na raiz do projeto:

```toml
GEMINI_API_KEY = "cole-sua-chave-aqui"
```

E adicione ao `.gitignore`:

```
.streamlit/secrets.toml
```

No código, leia a chave assim:

```python
api_key=st.secrets["GEMINI_API_KEY"]
```

## Como rodar

1. Instale as dependências:

   ```bash
   pip install streamlit openai
   ```

2. Configure a chave em `.streamlit/secrets.toml` (veja acima).

3. Rode o app:

   ```bash
   streamlit run app.py
   ```

4. O navegador abre em `http://localhost:8501`.
