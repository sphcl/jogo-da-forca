import random
import time
from tkinter import *

def add_margem_superior(janela):
    #carrega a imagem e redimensiona conforme necessário
    nuvens_image = PhotoImage(file="imagens/nuvens.png").zoom(3)

    #cria uma label para a imagem
    nuvens_label = Label(janela, image=nuvens_image, background="#d4e2e4")
    nuvens_label.image = nuvens_image  #mantém uma referência para evitar garbage collection
    nuvens_label.pack(side=TOP, fill=X)

#sorteia a palavra e coloca os tracinhos correspondentes
def revelar_letra_aleatoria(estadoatual, palavra_secreta):
    letras_faltantes = [i for i, letra in enumerate(estadoatual) if letra == '_']
    if letras_faltantes:
        indice = random.choice(letras_faltantes)
        estadoatual[indice] = palavra_secreta[indice]
    return estadoatual

#lê as palavras e as dicas do arquivo
def ler_palavras_dicas(arquivo):
    palavras_dicas = []
    with open(arquivo, 'r', encoding='utf-8') as file:
        linhas = file.readlines()
        palavra = ''
        dicas = []
        for linha in linhas:
            linha = linha.strip()
            if linha.startswith('P:'):
                if palavra and dicas:
                    palavras_dicas.append((palavra, dicas))
                palavra = linha[2:]
                dicas = []
            elif linha.startswith('D:'):
                dicas.append(linha[2:])
        #adiciona a última palavra e suas dicas
        if palavra and dicas:
            palavras_dicas.append((palavra, dicas))
    return palavras_dicas

#função jogo
def jogo():
    global palavra, estadoatual, tentativas, letrasescolhidas, chances, resultado, tempo_inicio, tempo_limite, dicas_usadas, dicas, max_dicas

    palavras_dicas = ler_palavras_dicas('jogo.txt')
    palavra, dicas = random.choice(palavras_dicas)

    tentativas = 0
    chances = 6
    letrasescolhidas = []
    estadoatual = ["_"] * len(palavra)
    resultado = ""

    dicas_usadas = 0
    max_dicas = len(dicas)

    tempo_limite = 600  #600s = 10min
    tempo_inicio = time.time()

    #resetar as partes do corpo do boneco
    for parte in partes_corpo:
        canvas.itemconfig(parte, state='hidden')

    atualizar_interface()
    verificar_tempo()

#interface para mostrar o estado atual do jogo
def atualizar_interface():
    tentativas_label.config(text="Tentativas restantes: " + str(chances - tentativas), background="#d4e2e4")
    letras_label.config(text="Letras escolhidas: " + ", ".join(letrasescolhidas), background="#d4e2e4")
    resultado_label.config(text=resultado, background="#d4e2e4")
    dicas_label.config(text=f"Dicas usadas: {dicas_usadas}\nDicas restantes: {max_dicas - dicas_usadas}\n★ Dica 1: {dicas[0]}", background="#d4e2e4")
    estado_label.config(text="Estado atual da palavra: " + " ".join(estadoatual), background="#d4e2e4")
    
#verificar o tempo 
def verificar_tempo():
    tempo_atual = time.time()
    tempo_decorrido = tempo_atual - tempo_inicio
    if tempo_decorrido >= tempo_limite:
        resultado_label.config(text="Você perdeu! O tempo acabou. :( ")
        perguntar_jogar_novamente()
        return

    if tentativas < chances and "_" in estadoatual:
        janela_jogo.after(1000, verificar_tempo)  #verificar a cada segundo

def selecionar_letra(letra):
    global tentativas, resultado

    #verificar se a letra já foi escolhida
    if letra in letrasescolhidas:
        resultado = "Você já escolheu essa letra. Tente novamente."
    else:
        letrasescolhidas.append(letra)

        if letra in palavra:
            resultado = "Parabéns! A letra faz parte da palavra secreta. :)"
            for i in range(len(palavra)):
                if letra == palavra[i]:
                    estadoatual[i] = letra
        else:
            resultado = "Que pena, você errou. :("
            tentativas += 1
            if tentativas <= chances:
                desenhar_parte_corpo(tentativas)

        #ao não ter mais tracinhos o jogador ganhou
        if "_" not in estadoatual:
            resultado = "Você ganhou o jogo, meus parabéns! x) "
            perguntar_jogar_novamente()
        elif tentativas == chances:
            resultado = f"Você perdeu. :( A palavra secreta era '{palavra}'."
            perguntar_jogar_novamente()

    atualizar_interface()

#função para adicionar partes do boneco ao errar uma letra
def desenhar_parte_corpo(tentativas):
    if tentativas - 1 < len(partes_corpo):
        canvas.itemconfig(partes_corpo[tentativas - 1], state='normal')

#função dicas
def pedir_dica():
    global dicas_usadas, tentativas, resultado
    if dicas_usadas < len(dicas) - 1:  #-1 para excluir a primeira dica que já foi exibida
        resultado = f"Dica {dicas_usadas + 2}: {dicas[dicas_usadas + 1]}"  #próxima dica disponível
        dicas_usadas += 1
    else:
        if dicas_usadas < len(dicas):
            resultado = f"Essa foi a última dica disponível: {dicas[dicas_usadas]}"
        else:
            resultado = "Você já usou todas as dicas disponíveis."
            resultado = f"Você perdeu. :( A palavra secreta era '{palavra}'."
            perguntar_jogar_novamente()
    atualizar_interface()

#ao pedir umas letra o jogador perde duas dicas
def revelar_letra():
    global dicas_usadas, resultado
    if dicas_usadas + 2 <= max_dicas:
        revelar_letra_aleatoria(estadoatual, palavra)
        resultado = "Uma letra foi revelada: " + " ".join(estadoatual)
        dicas_usadas += 2
    else:
        resultado = "Você já usou todas as dicas disponíveis."
    atualizar_interface()

#janela para perguntar se o jogador deseja jogar novamente
def perguntar_jogar_novamente():
    janela_jogo.after(1000, mostrar_janela_pergunta)  #mostrar a pergunta após um segundo

def mostrar_janela_pergunta():
    global janela_pergunta

    janela_pergunta = Toplevel(janela_jogo)
    janela_pergunta.title("Jogar Novamente")
    janela_pergunta.geometry("250x100")
    janela_pergunta.configure(background="#d4e2e4")

    pergunta_label = Label(janela_pergunta, text="Você deseja jogar novamente? (s/n)", background="#d4e2e4", foreground="#00798c", font=("FONTSPRING DEMO", 10))
    pergunta_label.pack(pady=10)

    resposta_entry = Entry(janela_pergunta)
    resposta_entry.pack(pady=5)

    confirmar_button = Button(janela_pergunta, text="Confirmar", fg="#ff8673", bg="#013838", command=lambda: tratar_resposta(resposta_entry.get()))
    confirmar_button.pack(pady=5)

#função para as respostas s = recomeca, n = janela de agradecimento fechar_jogo
def tratar_resposta(resposta):
    if resposta.lower() == 's':
        janela_pergunta.destroy()
        jogo()
    elif resposta.lower() == 'n':
        janela_pergunta.destroy()
        fechar_jogo()

def fechar_jogo():
    janela_jogo.destroy()
    janela_agradecimento = Tk()
    janela_agradecimento.configure(background="#d4e2e4")
    janela_agradecimento.geometry("700x630")

    #carregando a imagem de diálogo
    dialogo_image = PhotoImage(file="imagens/dialogo.png").subsample(1)

    #frame para conter a imagem e o botão de fechar
    frame_conteudo = Frame(janela_agradecimento, background="#d4e2e4")
    frame_conteudo.pack(expand=True)

    #label para a imagem de diálogo
    dialogo_image_label = Label(frame_conteudo, image=dialogo_image, background="#d4e2e4")
    dialogo_image_label.pack(pady=0)

    #botão para fechar a janela
    fechar_button = Button(frame_conteudo, text="Fechar", command=janela_agradecimento.destroy, font=("Tiny5", 15), fg="#ff8673", bg="#013838")
    fechar_button.pack(pady=0)

    janela_agradecimento.mainloop()

#janela do jogo
def abrir_janela_inicial():
    global janela_inicial

    janela_inicial = Tk()
    janela_inicial.title("Jogo da Forca")
    janela_inicial.geometry("750x480")
    janela_inicial.configure(background="#d4e2e4") 


    add_margem_superior(janela_inicial)

    frame_imagens = Frame(janela_inicial, background="#d4e2e4")
    frame_imagens.pack()
  
    logo = PhotoImage(file="imagens/logo.png")
    planetinha = PhotoImage(file="imagens/planetinha.png")

    logo = logo.subsample(3)
    planetinha = planetinha.subsample(6)

    frame_imagens.grid_rowconfigure(0, weight=1)
    frame_imagens.grid_columnconfigure(0, weight=1)
    frame_imagens.grid_columnconfigure(2, weight=1)

    label_planetinha_esq = Label(frame_imagens, image=planetinha, background="#d4e2e4")
    label_planetinha_esq.grid(row=0, column=0, padx=10, pady=20)

    label_logo = Label(frame_imagens, image=logo, background="#d4e2e4")
    label_logo.grid(row=0, column=1, padx=10, pady=20)

    label_planetinha_dir = Label(frame_imagens, image=planetinha, background="#d4e2e4")
    label_planetinha_dir.grid(row=0, column=2, padx=10, pady=20)

    #adiciona o botão "Começar"
    botao_comecar = Button(janela_inicial, text="Começar", command=abrir_janela_introducao, font=("Tiny5", 15), fg="#ff8673", bg="#013838")
    botao_comecar.pack(pady=10)

    #mantém a referência à imagem para evitar que ela seja coletada pelo garbage collector
    label_logo.image = logo

    janela_inicial.mainloop()

def abrir_janela_introducao():
    janela_inicial.destroy()
    abrir_janela()

#janela de introdução
def abrir_janela():
    global janela, tentativas_label, letras_label, resultado_label, dicas_label, estado_label, canvas, partes_corpo, janela_jogo

    janela = Tk()
    janela.configure(background="#d4e2e4")
    janela.title("Jogo da forca - Introdução")
    janela.geometry("850x480")

    add_margem_superior(janela)

    #labels para mostrar a introdução
    introducao_label = Label(janela, text="Introdução ao Jogo da Forca", padx=10, pady=10, foreground="#6e0d25", font=("Playfair Display Black", 20), background="#d4e2e4")
    introducao_label.pack()

    #texto de introdução
    texto_introducao = (
        "★ ｡･::･ﾟ Seja bem vindo ao jogo da forca da Yas e da Soso! ｡･::･ﾟ★\n"
        "★ O seu objetivo é tentar acertar a palavra secreta com base nas dicas.\n"
        "★ Não utilize palavras com acento.\n"
        "★ Caso você acerte, a letra será adicionada.\n"
        "★ Você tem direito a 6 dicas e pode solicitar que uma letra seja revelada,\n" 
        "mas ao fazer isso, perde 2 dicas.\n"
        "★ Caso você erre, você tem no máximo 6 tentativas.\n"
        "★ Você tem 20 minutos para descobrir a palavra, se ultrapassar o limite de \n"
        "tempo você perderá automaticamente."
    )
    texto_label = Label(janela, text=texto_introducao, padx=10, pady=10, justify=LEFT, foreground="#00798c", font=("Pixelify Sans", 10), background="#d4e2e4")
    texto_label.pack(pady=20, padx=20)

    #botão para iniciar o jogo
    iniciar_button = Button(janela, text="Iniciar Jogo", command=iniciar_jogo, font=("Tiny5", 15), fg="#ff8673", bg="#013838")
    iniciar_button.pack(pady=25, padx=25)

    janela.mainloop()

def iniciar_jogo():
    global janela_jogo, tentativas_label, letras_label, resultado_label, dicas_label, estado_label, canvas, partes_corpo

    janela.destroy()

    janela_jogo = Tk()
    janela_jogo.configure(background="#d4e2e4")
    janela_jogo.title("Jogo da Forca")
    janela_jogo.geometry("700x650")

    tentativas_label = Label(janela_jogo, text="", foreground="#6e0d25", font=("Playfair Display Black", 12))
    letras_label = Label(janela_jogo, text="", foreground="#6e0d25", font=("Playfair Display Black", 12))
    resultado_label = Label(janela_jogo, text="", foreground="#6e0d25", font=("Playfair Display Black", 12))
    dicas_label = Label(janela_jogo, text="", foreground="#6e0d25", font=("Playfair Display Black", 12))
    estado_label = Label(janela_jogo, text="", foreground="#6e0d25", font=("Playfair Display Black", 12))

    tentativas_label.pack()
    letras_label.pack()
    resultado_label.pack()
    dicas_label.pack()
    estado_label.pack()

    #canvas para desenhar o boneco da forca
    canvas = Canvas(janela_jogo, width=200, height=250, background="#d4e2e4")
    canvas.pack(pady=20)

    #base do boneco
    canvas.create_line(50, 230, 150, 230, width=2)
    canvas.create_line(100, 230, 100, 50, width=2)
    canvas.create_line(100, 50, 150, 50, width=2)
    canvas.create_line(150, 50, 150, 70, width=2)

    #partes do corpo do boneco (escondidas inicialmente)
    head = canvas.create_oval(140, 70, 160, 90, width=2, state='hidden')
    body = canvas.create_line(150, 90, 150, 150, width=2, state='hidden')
    left_arm = canvas.create_line(150, 110, 130, 130, width=2, state='hidden')
    right_arm = canvas.create_line(150, 110, 170, 130, width=2, state='hidden')
    left_leg = canvas.create_line(150, 150, 130, 190, width=2, state='hidden')
    right_leg = canvas.create_line(150, 150, 170, 190, width=2, state='hidden')

    partes_corpo = [head, body, left_arm, right_arm, left_leg, right_leg]

    #botões para as letras do alfabeto
    letras_frame = Frame(janela_jogo)
    letras_frame.pack()

    alfabeto = 'abcdefghijklmnopqrstuvwxyz'
    for letra in alfabeto:
        button = Button(letras_frame, text=letra, command=lambda l=letra: selecionar_letra(l), font=("Pixelify Sans Bold", 12), fg="#ff8673", bg="#013838")
        button.pack(side=LEFT)

    #botão para pedir dica
    dica_button = Button(janela_jogo, text="Pedir Dica", command=pedir_dica, font=("Pixelify Sans Bold", 12), fg="#ff8673", bg="#013838")
    dica_button.pack(pady=5)

    #botão para revelar uma letra
    revelar_button = Button(janela_jogo, text="Revelar Letra", command=revelar_letra, font=("Pixelify Sans Bold", 12), fg="#ff8673", bg="#013838")
    revelar_button.pack(pady=5)

    jogo()  #iniciar o jogo

#iniciar a aplicação com a janela inicial
abrir_janela_inicial()