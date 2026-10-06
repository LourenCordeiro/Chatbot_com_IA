#título
#campo de mensagem
#Quando o usuário digitar uma mensagem, o chatbot deve seguir os seguintes passos:
#1 - Mostrar a mensagem na conversa
#2 - Pegar a mensagem do usuário e enviar para IA responder
#3 - Mostrar a resposta da IA na conversa

#Ferramentas que serão utilizadas: Streamlit(ferramenta que cria interfaces web e OpenAI(IA)
#Ferramentas streamlit: st.write, st.text_input, st.button
#comando no terminal: streamlit run main.py (faz o código rodar no navegador)
#Ferramentas OpenAI: openai.ChatCompletion.create 

import streamlit as st
from openai import OpenAI

modelo_ia = OpenAI(api_key="SUA CHAVE AQUI",
                        base_url="https://generativelanguage.googleapis.com/v1beta/openai")

st.write("## ChatBot De IA usando Python")
#Criar o histórico da conversa
if not "lista _mensagens" in st.session_state:
    st.session_state["lista _mensagens"] = []

#exibir o histórico de mensagem
for mensagem in st.session_state["lista _mensagens"]:
    role = mensagem["role"]
    content = mensagem["content"]
    st.chat_message(role).write(content)

mensagem_usuario = st.chat_input("Escreva sua mensagem aqui") 

if mensagem_usuario:
    #comando para mostrar a mensagem do usuário na conversa
    #Vai usar as duas opções: "user"(usuário) ou "assistant"(inteligência artificial)
    st.chat_message("user").write(mensagem_usuario) 
    mensagem = {"role": "user", "content": mensagem_usuario}
    st.session_state["lista _mensagens"].append(mensagem)

    #resposta da IA
    resposta_modelo = modelo_ia.chat.completions.create(
        messages=st.session_state["lista _mensagens"],
        model="gemini-flash-lite-latest",
    ) 
    resposta_ia = resposta_modelo.choices[0].message.content 
    #exibir a resposta da IA na tela
    st.chat_message("assistant").write(resposta_ia)
    mensagem_ia = {"role": "assistant", "content": resposta_ia}
    st.session_state["lista _mensagens"].append(mensagem_ia)

#manter o histórico da conversa(criar memória)
#tornar as respostas da IA mais personalizadas 