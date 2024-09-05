import tkinter as tk
import customtkinter as ctk

class PaginaJogos:
    def __init__(self, root, on_jogo_selecionado, toggle_mode):
        self.root = root
        self.on_jogo_selecionado = on_jogo_selecionado
        self.toggle_mode = toggle_mode
        self.frame = ctk.CTkFrame(root)
        self.frame.pack(pady=20, padx=20, fill="both", expand=True)

        self.label = ctk.CTkLabel(self.frame, text="Selecione o Jogo", font=('Helvetica', 20, 'bold'))
        self.label.pack(pady=20)

        self.btn_basquete = ctk.CTkButton(self.frame, text="Basquete", command=lambda: self.on_jogo_selecionado("Basquete"))
        self.btn_basquete.pack(pady=10)

        self.btn_futsal = ctk.CTkButton(self.frame, text="Futsal", command=lambda: self.on_jogo_selecionado("Futsal"))
        self.btn_futsal.pack(pady=10)

        self.btn_volei = ctk.CTkButton(self.frame, text="Vôlei", command=lambda: self.on_jogo_selecionado("Vôlei"))
        self.btn_volei.pack(pady=10)


class PaginaPlacar:
    def __init__(self, root, nome_jogo, on_finalizar_partida):
        self.root = root
        self.nome_jogo = nome_jogo
        self.on_finalizar_partida = on_finalizar_partida

        self.pontos_azul = 0
        self.pontos_vermelho = 0

        if nome_jogo == "Basquete":
            self.tempo_partida = 10 * 60
            self.tempos = 4
        elif nome_jogo == "Futsal":
            self.tempo_partida = 10 * 60
            self.tempos = 2
        else:  # Vôlei
            self.tempos = 0

        self.tempo_restante_no_periodo = self.tempo_partida if self.tempos > 0 else 0
        self.tempo_pausado = True
        self.periodo_atual = 1
        self.comentarios = []

        if nome_jogo == "Vôlei":
            self.pontos_set_atual_azul = 0
            self.pontos_set_atual_vermelho = 0
            self.sets_azul = 0
            self.sets_vermelho = 0

        self.frame = ctk.CTkFrame(root)
        self.frame.pack(pady=20, padx=20, fill="both", expand=True)

        self.label_titulo = ctk.CTkLabel(self.frame, text=nome_jogo, font=('Helvetica', 24, 'bold'))
        self.label_titulo.pack(pady=10)

        if nome_jogo != "Vôlei":
            self.label_tempo = ctk.CTkLabel(self.frame, text=self.formatar_tempo(), font=('Helvetica', 48, 'bold'))
            self.label_tempo.pack(pady=20)

            self.btn_play_pause = ctk.CTkButton(self.frame, text="Play", command=self.toggle_play_pause, font=('Helvetica', 16, 'bold'))
            self.btn_play_pause.pack(pady=10)

        self.btn_add_ponto_azul = ctk.CTkButton(self.frame, text="+ Azul", command=lambda: self.add_ponto_azul(1), font=('Helvetica', 16, 'bold'))
        self.btn_add_ponto_azul.pack(pady=5)

        self.btn_remove_azul = ctk.CTkButton(self.frame, text="- Azul", command=self.remove_ponto_azul, font=('Helvetica', 16, 'bold'))
        self.btn_remove_azul.pack(pady=5)

        self.btn_add_ponto_vermelho = ctk.CTkButton(self.frame, text="+ Vermelho", command=lambda: self.add_ponto_vermelho(1), font=('Helvetica', 16, 'bold'))
        self.btn_add_ponto_vermelho.pack(pady=5)

        self.btn_remove_vermelho = ctk.CTkButton(self.frame, text="- Vermelho", command=self.remove_ponto_vermelho, font=('Helvetica', 16, 'bold'))
        self.btn_remove_vermelho.pack(pady=5)

        if nome_jogo == "Vôlei":
            self.label_placar_volei = ctk.CTkLabel(self.frame, text=self.formatar_placar_volei(), font=('Helvetica', 20, 'bold'))
            self.label_placar_volei.pack(pady=10)

            self.btn_finalizar_set = ctk.CTkButton(self.frame, text="Finalizar Set", command=self.finalizar_set, font=('Helvetica', 16, 'bold'))
            self.btn_finalizar_set.pack(pady=5)

        self.label_placar = ctk.CTkLabel(self.frame, text=self.formatar_placar(), font=('Helvetica', 48, 'bold'))
        self.label_placar.pack(pady=20)

        self.btn_finalizar_partida = ctk.CTkButton(self.frame, text="Finalizar Partida", command=self.finalizar_partida, font=('Helvetica', 16, 'bold'))
        self.btn_finalizar_partida.pack(pady=5)

        self.btn_add_comentario = ctk.CTkButton(self.frame, text="Adicionar Comentário", command=self.adicionar_comentario, font=('Helvetica', 16, 'bold'))
        self.btn_add_comentario.pack(pady=20)

        self.frame_comentarios = ctk.CTkFrame(self.frame)
        self.frame_comentarios.pack(pady=10, fill='both', expand=True)

    def formatar_placar(self):
        return f"{self.pontos_azul} - {self.pontos_vermelho}"

    def formatar_placar_volei(self):
        return f"Sets: {self.sets_azul} - {self.sets_vermelho}\nPontos: {self.pontos_set_atual_azul} - {self.pontos_set_atual_vermelho}"

    def formatar_tempo(self):
        minutos = self.tempo_restante_no_periodo // 60
        segundos = self.tempo_restante_no_periodo % 60
        return f"{minutos:02d}:{segundos:02d}"

    def toggle_play_pause(self):
        self.tempo_pausado = not self.tempo_pausado
        if not self.tempo_pausado:
            self.btn_play_pause.configure(text="Pause")
            self.atualizar_tempo()
        else:
            self.btn_play_pause.configure(text="Play")

    def atualizar_tempo(self):
        if not self.tempo_pausado:
            if self.tempo_restante_no_periodo > 0:
                self.tempo_restante_no_periodo -= 1
                self.label_tempo.configure(text=self.formatar_tempo())
                self.root.after(1000, self.atualizar_tempo)
            else:
                self.periodo_atual += 1
                if self.periodo_atual > self.tempos:
                    self.finalizar_partida()
                else:
                    self.tempo_restante_no_periodo = self.tempo_partida
                    self.label_tempo.configure(text=self.formatar_tempo())

    def add_ponto_azul(self, pontos):
        self.pontos_azul += pontos
        self.label_placar.configure(text=self.formatar_placar())
        if self.nome_jogo == "Vôlei":
            self.pontos_set_atual_azul += pontos
            self.label_placar_volei.configure(text=self.formatar_placar_volei())

    def add_ponto_vermelho(self, pontos):
        self.pontos_vermelho += pontos
        self.label_placar.configure(text=self.formatar_placar())
        if self.nome_jogo == "Vôlei":
            self.pontos_set_atual_vermelho += pontos
            self.label_placar_volei.configure(text=self.formatar_placar_volei())

    def remove_ponto_azul(self):
        if self.nome_jogo != "Vôlei" or self.pontos_set_atual_azul > 0:
            self.pontos_azul = max(0, self.pontos_azul - 1)
            self.label_placar.configure(text=self.formatar_placar())
            if self.nome_jogo == "Vôlei":
                self.pontos_set_atual_azul = max(0, self.pontos_set_atual_azul - 1)
                self.label_placar_volei.configure(text=self.formatar_placar_volei())

    def remove_ponto_vermelho(self):
        if self.nome_jogo != "Vôlei" or self.pontos_set_atual_vermelho > 0:
            self.pontos_vermelho = max(0, self.pontos_vermelho - 1)
            self.label_placar.configure(text=self.formatar_placar())
            if self.nome_jogo == "Vôlei":
                self.pontos_set_atual_vermelho = max(0, self.pontos_set_atual_vermelho - 1)
                self.label_placar_volei.configure(text=self.formatar_placar_volei())

    def finalizar_set(self):
        if self.pontos_set_atual_azul > self.pontos_set_atual_vermelho:
            self.sets_azul += 1
        else:
            self.sets_vermelho += 1

        self.pontos_set_atual_azul = 0
        self.pontos_set_atual_vermelho = 0

        self.label_placar_volei.configure(text=self.formatar_placar_volei())

        if self.sets_azul == 3 or self.sets_vermelho == 3:
            self.finalizar_partida()

    def finalizar_partida(self):
        self.on_finalizar_partida(self.nome_jogo, self.formatar_placar(), self.comentarios)

    def adicionar_comentario(self):
        comentario_popup = ctk.CTkToplevel(self.frame)
        comentario_popup.title("Adicionar Comentário")
        comentario_popup.geometry("400x200")

        comentario_label = ctk.CTkLabel(comentario_popup, text="Digite seu comentário:")
        comentario_label.pack(pady=10)

        comentario_texto = tk.Text(comentario_popup, height=5, width=40)
        comentario_texto.pack(pady=10)

        def salvar_comentario():
            comentario = comentario_texto.get("1.0", "end-1c")
            self.comentarios.append(comentario)
            self.exibir_comentarios()
            comentario_popup.destroy()

        btn_salvar_comentario = ctk.CTkButton(comentario_popup, text="Salvar", command=salvar_comentario)
        btn_salvar_comentario.pack(pady=10)

    def exibir_comentarios(self):
        for widget in self.frame_comentarios.winfo_children():
            widget.destroy()
        for comentario in self.comentarios:
            comentario_label = ctk.CTkLabel(self.frame_comentarios, text=comentario, wraplength=350)
            comentario_label.pack(pady=5)

class PaginaResultado:
    def __init__(self, root, resultados, mostrar_pagina_jogos):
        self.root = root
        self.resultados = resultados
        self.mostrar_pagina_jogos = mostrar_pagina_jogos

        self.frame = ctk.CTkFrame(root)
        self.frame.pack(pady=20, padx=20, fill="both", expand=True)

        self.label = ctk.CTkLabel(self.frame, text="Resultados", font=('Helvetica', 20, 'bold'))
        self.label.pack(pady=10)

        for resultado in resultados:
            label_resultado = ctk.CTkLabel(self.frame, text=resultado, font=('Helvetica', 16))
            label_resultado.pack(pady=5)

        btn_voltar = ctk.CTkButton(self.frame, text="Voltar", command=self.mostrar_pagina_jogos, font=('Helvetica', 16, 'bold'), text_color="#99AAB5")
        btn_voltar.pack(pady=10)

class App:
    def __init__(self, root):
        self.root = root
        self.resultados = []

        ctk.set_appearance_mode("dark")  # Inicia com modo escuro
        ctk.set_default_color_theme("blue")

        self.root.title("Placar de Jogos")
        self.root.geometry("400x800")

        self.mostrar_pagina_jogos()

    def toggle_mode(self):
        current_mode = ctk.get_appearance_mode()
        new_mode = "light" if current_mode == "dark" else "dark"
        ctk.set_appearance_mode(new_mode)
        self.pagina_jogos.atualizar_texto_botao(new_mode)  # Atualiza o texto do botão

        # Atualiza a cor de fundo dos frames
        self.pagina_jogos.frame.configure(bg=ctk.get_color("background"))
        if hasattr(self, 'pagina_placar'):
            self.pagina_placar.frame.configure(bg=ctk.get_color("background"))
        if hasattr(self, 'pagina_resultado'):
            self.pagina_resultado.frame.configure(bg=ctk.get_color("background"))

    def mostrar_pagina_jogos(self):
        self.limpar_frame()
        self.pagina_jogos = PaginaJogos(self.root, self.jogo_selecionado, self.toggle_mode)

    def jogo_selecionado(self, nome_jogo):
        self.limpar_frame()
        self.pagina_placar = PaginaPlacar(self.root, nome_jogo, self.finalizar_partida)

    def finalizar_partida(self, nome_jogo, placar, comentarios):
        resultado = f"{nome_jogo}: {placar}\nComentários: {'; '.join(comentarios)}"
        self.resultados.append(resultado)
        self.mostrar_pagina_resultado()

    def mostrar_pagina_resultado(self):
        self.limpar_frame()
        self.pagina_resultado = PaginaResultado(self.root, self.resultados, self.mostrar_pagina_jogos)

    def limpar_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()

root = ctk.CTk()
app = App(root)
root.mainloop()