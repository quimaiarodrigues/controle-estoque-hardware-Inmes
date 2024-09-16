import tkinter as tk
from tkinter import messagebox

def debitar_componentes(projeto_list, componentes_dict):
    def debitar():
        projeto_selecionado = projeto_selecionado_var.get()
        if projeto_selecionado:
            confirmar = messagebox.askyesno("Confirmar Débito", f"Você tem certeza que deseja debitar os componentes do projeto '{projeto_selecionado}'?")
            if confirmar:
                if projeto_selecionado in componentes_dict:
                    componentes = componentes_dict[projeto_selecionado]
                    for comp in componentes:
                        if comp["quantidade_disponivel"] > 0:
                            comp["quantidade_disponivel"] -= comp["quantidade_por_placa"]
                            if comp["quantidade_disponivel"] < 0:
                                comp["quantidade_disponivel"] = 0
                    messagebox.showinfo("Info", "Componentes debitados com sucesso!")
                else:
                    messagebox.showwarning("Aviso", "Projeto não encontrado.")
                janela_debito.destroy()
            else:
                janela_debito.destroy()
        else:
            messagebox.showwarning("Aviso", "Nenhum projeto selecionado.")

    janela_debito = tk.Toplevel()
    janela_debito.title("Debitar Componentes")
    janela_debito.geometry("400x300")

    tk.Label(janela_debito, text="Selecione o Projeto:").pack(anchor="w", padx=10, pady=5)
    
    projeto_selecionado_var = tk.StringVar()
    projeto_selecionado_var.set(projeto_list[0] if projeto_list else '')  # Define um valor padrão

    projeto_combobox = tk.OptionMenu(janela_debito, projeto_selecionado_var, *projeto_list)
    projeto_combobox.pack(fill="x", padx=10, pady=5)

    frame_botoes = tk.Frame(janela_debito)
    frame_botoes.pack(pady=10)

    tk.Button(frame_botoes, text="Debitar", command=debitar).pack(side="left", padx=10)
    tk.Button(frame_botoes, text="Cancelar", command=janela_debito.destroy).pack(side="left", padx=10)
