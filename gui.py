import customtkinter as ctk
from tkinter import messagebox
import script  # Importa o script refatorado

# Configurar o tema global
ctk.set_appearance_mode("dark")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Text-to-SQL Generator")
        
        # Obter dimensões da tela
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # Definir tamanho da janela baseado na tela (85% da tela)
        window_width = int(screen_width * 0.85)
        window_height = int(screen_height * 0.85)
        
        # Centralizar a janela
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.root.minsize(1000, 750)  # Tamanho mínimo maior
        
        # Variáveis da aplicação
        self.db = None
        self.db_engine = None
        self.schema = None
        
        # Variável para controlar rolagem contextual
        self.scrolling_widget = None
        
        # Cores personalizadas
        self.colors = {
            'primary': '#1f2937',
            'secondary': '#374151',
            'accent': '#3b82f6',
            'success': '#10b981',
            'warning': '#f59e0b',
            'danger': '#ef4444',
            'light': '#f9fafb',
            'text': '#111827'
        }
        
        # Configurar interface com rolagem
        self.setup_scrollable_ui()
        
    def setup_scrollable_ui(self):
        # Container principal
        main_container = ctk.CTkFrame(self.root, fg_color="transparent")
        main_container.pack(fill="both", expand=True, padx=15, pady=15)
        
        # Configurar grid
        main_container.grid_rowconfigure(0, weight=1)
        main_container.grid_columnconfigure(0, weight=1)
        
        # Frame scrollable principal
        self.main_scrollable = ctk.CTkScrollableFrame(
            main_container,
            orientation="vertical"
        )
        self.main_scrollable.pack(fill="both", expand=True)
        
        # Configurar a largura do frame scrollable
        self.main_scrollable.grid_columnconfigure(0, weight=1)
        
        # Configurar rolagem com mouse wheel e touchpad
        self.setup_mouse_wheel_scrolling()
        
        # Criar a interface
        self.create_ui()
        
    def setup_mouse_wheel_scrolling(self):
        """Configurar rolagem contextual com mouse wheel e touchpad"""
        def _on_mousewheel(event):
            # Se há um widget específico capturando a rolagem, usar ele
            if self.scrolling_widget:
                if self.scrolling_widget == "schema":
                    # Rolar o textbox do schema
                    self.schema_text.yview_scroll(int(-1 * self._get_scroll_delta(event)), "units")
                elif self.scrolling_widget == "results":
                    # Rolar o frame de resultados
                    self.results_scrollable._parent_canvas.yview_scroll(int(-1 * self._get_scroll_delta(event)), "units")
                return
            
            # Rolagem global padrão
            self.main_scrollable._parent_canvas.yview_scroll(int(-1 * self._get_scroll_delta(event)), "units")
        
        def _bind_to_mousewheel(event):
            # Linux
            self.root.bind_all("<Button-4>", _on_mousewheel)
            self.root.bind_all("<Button-5>", _on_mousewheel)
            # Windows/macOS
            self.root.bind_all("<MouseWheel>", _on_mousewheel)
        
        def _unbind_from_mousewheel(event):
            self.root.unbind_all("<Button-4>")
            self.root.unbind_all("<Button-5>")
            self.root.unbind_all("<MouseWheel>")
        
        # Bind eventos quando mouse entra/sai da janela
        self.root.bind('<FocusIn>', _bind_to_mousewheel)
        self.root.bind('<FocusOut>', _unbind_from_mousewheel)
        
        # Ativar rolagem inicialmente
        _bind_to_mousewheel(None)
    
    def _get_scroll_delta(self, event):
        """Obter valor de scroll normalizado para diferentes plataformas"""
        # Para Linux - mouse wheel
        if event.num == 4:
            return 1
        elif event.num == 5:
            return -1
        # Para Windows/macOS
        elif hasattr(event, 'delta'):
            return event.delta / 120
        return 0
    
    def setup_contextual_scrolling(self, widget, widget_name):
        """Configurar rolagem contextual para um widget específico"""
        def on_enter(event):
            self.scrolling_widget = widget_name
        
        def on_leave(event):
            self.scrolling_widget = None
        
        # Bind eventos de entrada e saída do mouse
        widget.bind("<Enter>", on_enter)
        widget.bind("<Leave>", on_leave)
        
        # Para CTkTextbox, também bind nos elementos internos
        if hasattr(widget, '_textbox'):
            widget._textbox.bind("<Enter>", on_enter)
            widget._textbox.bind("<Leave>", on_leave)
        
        # Para CTkScrollableFrame, bind no canvas interno
        if hasattr(widget, '_parent_canvas'):
            widget._parent_canvas.bind("<Enter>", on_enter)
            widget._parent_canvas.bind("<Leave>", on_leave)
            
    def create_ui(self):
        # Container centralizado para o conteúdo
        content_container = ctk.CTkFrame(self.main_scrollable, fg_color="transparent")
        content_container.pack(fill="x", expand=True, padx=25, pady=25)
        content_container.grid_columnconfigure(0, weight=1)
        content_container.grid_columnconfigure(1, weight=1)
        content_container.grid_columnconfigure(2, weight=1)
        
        # Frame central com largura fixa
        center_frame = ctk.CTkFrame(content_container, width=900)
        center_frame.grid(row=0, column=1, sticky="ew", padx=25)
        center_frame.grid_columnconfigure(0, weight=1)
        
        # Criar header
        self.create_header(center_frame)
        
        # Criar todas as seções
        self.create_connection_section(center_frame)
        self.create_schema_section(center_frame)
        self.create_query_section(center_frame)
        self.create_status_section(center_frame)
        self.create_sql_output_section(center_frame)
        self.create_results_section(center_frame)
        
        # Espaço final
        final_spacer = ctk.CTkFrame(center_frame, height=40, fg_color="transparent")
        final_spacer.grid(row=7, column=0, sticky="ew")
        
    def create_header(self, parent):
        # Header
        header_frame = ctk.CTkFrame(parent, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", pady=(15, 40))
        header_frame.grid_columnconfigure(0, weight=1)
        
        # Título principal
        title_label = ctk.CTkLabel(
            header_frame,
            text="Text-to-SQL Generator",
            font=ctk.CTkFont(size=32, weight="bold"),
            text_color=("#1f2937", "#ffffff")
        )
        title_label.grid(row=0, column=0, pady=(0, 12))
        
        # Subtítulo
        subtitle_label = ctk.CTkLabel(
            header_frame,
            text="Transforme perguntas em linguagem natural em consultas SQL poderosas",
            font=ctk.CTkFont(size=16),
            text_color=("#6b7280", "#9ca3af")
        )
        subtitle_label.grid(row=1, column=0)
        
    def create_connection_section(self, parent):
        # Frame de conexão
        conn_frame = ctk.CTkFrame(parent)
        conn_frame.grid(row=1, column=0, sticky="ew", padx=25, pady=20)
        conn_frame.grid_columnconfigure(1, weight=1)
        
        # Título da seção
        section_title = ctk.CTkLabel(
            conn_frame,
            text=">> Conexão com Banco de Dados",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        section_title.grid(row=0, column=0, columnspan=2, pady=(25, 20), padx=25)
        
        # Motor do banco
        ctk.CTkLabel(conn_frame, text="Motor:", font=ctk.CTkFont(weight="bold", size=14)).grid(
            row=1, column=0, padx=(25, 15), pady=10, sticky="w"
        )
        self.db_engine_combo = ctk.CTkComboBox(
            conn_frame,
            values=["postgresql", "mysql"],
            width=280,
            font=ctk.CTkFont(size=13),
            height=35
        )
        self.db_engine_combo.set("postgresql")
        self.db_engine_combo.grid(row=1, column=1, padx=(15, 25), pady=10, sticky="ew")
        
        # Usuário
        ctk.CTkLabel(conn_frame, text="Usuário:", font=ctk.CTkFont(weight="bold", size=14)).grid(
            row=2, column=0, padx=(25, 15), pady=10, sticky="w"
        )
        self.user_entry = ctk.CTkEntry(
            conn_frame,
            placeholder_text="Digite o usuário do banco",
            font=ctk.CTkFont(size=13),
            height=35
        )
        self.user_entry.insert(0, "postgres")
        self.user_entry.grid(row=2, column=1, padx=(15, 25), pady=10, sticky="ew")
        
        # Senha
        ctk.CTkLabel(conn_frame, text="Senha:", font=ctk.CTkFont(weight="bold", size=14)).grid(
            row=3, column=0, padx=(25, 15), pady=10, sticky="w"
        )
        self.password_entry = ctk.CTkEntry(
            conn_frame,
            placeholder_text="Digite a senha do banco",
            show="*",
            font=ctk.CTkFont(size=13),
            height=35
        )
        self.password_entry.grid(row=3, column=1, padx=(15, 25), pady=10, sticky="ew")
        
        # Database
        ctk.CTkLabel(conn_frame, text="Database:", font=ctk.CTkFont(weight="bold", size=14)).grid(
            row=4, column=0, padx=(25, 15), pady=10, sticky="w"
        )
        self.dbname_entry = ctk.CTkEntry(
            conn_frame,
            placeholder_text="Nome do banco de dados",
            font=ctk.CTkFont(size=13),
            height=35
        )
        self.dbname_entry.insert(0, "university")
        self.dbname_entry.grid(row=4, column=1, padx=(15, 25), pady=10, sticky="ew")
        
        # Botão de conexão
        button_frame = ctk.CTkFrame(conn_frame, fg_color="transparent")
        button_frame.grid(row=5, column=0, columnspan=2, pady=25)
        
        self.connect_button = ctk.CTkButton(
            button_frame,
            text="Conectar e Carregar Schema",
            command=self.connect_and_load_schema,
            font=ctk.CTkFont(size=14, weight="bold"),
            height=40,
            width=250
        )
        self.connect_button.pack()
        
    def create_schema_section(self, parent):
        # Frame do schema
        schema_frame = ctk.CTkFrame(parent)
        schema_frame.grid(row=2, column=0, sticky="ew", padx=25, pady=20)
        schema_frame.grid_columnconfigure(0, weight=1)
        
        # Título da seção
        section_title = ctk.CTkLabel(
            schema_frame,
            text=">> Schema do Banco de Dados",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        section_title.grid(row=0, column=0, pady=(25, 20))
        
        # Texto do schema
        self.schema_text = ctk.CTkTextbox(
            schema_frame,
            height=180,
            font=ctk.CTkFont(family="Courier", size=12),
            state="disabled"
        )
        self.schema_text.grid(row=1, column=0, padx=25, pady=(0, 25), sticky="ew")
        
        # Configurar rolagem contextual para o schema
        self.setup_contextual_scrolling(self.schema_text, "schema")
        
    def create_query_section(self, parent):
        # Frame de consulta
        query_frame = ctk.CTkFrame(parent)
        query_frame.grid(row=3, column=0, sticky="ew", padx=25, pady=20)
        query_frame.grid_columnconfigure(0, weight=1)
        
        # Título da seção
        section_title = ctk.CTkLabel(
            query_frame,
            text=">> Consulta em Linguagem Natural",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        section_title.grid(row=0, column=0, pady=(25, 20))
        
        # Frame interno para entrada e botão
        input_frame = ctk.CTkFrame(query_frame, fg_color="transparent")
        input_frame.grid(row=1, column=0, padx=25, pady=(0, 25), sticky="ew")
        input_frame.grid_columnconfigure(0, weight=1)
        
        # Entrada de texto
        self.natural_query_entry = ctk.CTkEntry(
            input_frame,
            placeholder_text="Digite sua pergunta em linguagem natural...",
            font=ctk.CTkFont(size=13),
            height=40
        )
        self.natural_query_entry.grid(row=0, column=0, padx=(0, 12), sticky="ew")
        
        # Botão de gerar
        self.generate_sql_button = ctk.CTkButton(
            input_frame,
            text="Gerar SQL",
            command=self.generate_and_execute_sql,
            state="disabled",
            font=ctk.CTkFont(size=13, weight="bold"),
            height=40,
            width=120,
            fg_color=self.colors['success'],
            hover_color="#059669"
        )
        self.generate_sql_button.grid(row=0, column=1)
        
    def create_status_section(self, parent):
        # Frame de status
        status_frame = ctk.CTkFrame(parent, fg_color="transparent")
        status_frame.grid(row=4, column=0, pady=15)
        
        self.status_label = ctk.CTkLabel(
            status_frame,
            text="* Conecte-se ao banco para começar",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=("#3b82f6", "#60a5fa")
        )
        self.status_label.pack()
        
    def create_sql_output_section(self, parent):
        # Frame de saída SQL
        sql_frame = ctk.CTkFrame(parent)
        sql_frame.grid(row=5, column=0, sticky="ew", padx=25, pady=20)
        sql_frame.grid_columnconfigure(0, weight=1)
        
        # Título da seção
        section_title = ctk.CTkLabel(
            sql_frame,
            text=">> SQL Gerada",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        section_title.grid(row=0, column=0, pady=(25, 20))
        
        # Texto de saída SQL
        self.sql_output_text = ctk.CTkTextbox(
            sql_frame,
            height=130,
            font=ctk.CTkFont(family="Courier", size=13, weight="bold"),
            text_color=("#059669", "#10b981")
        )
        self.sql_output_text.grid(row=1, column=0, padx=25, pady=(0, 25), sticky="ew")
        
    def create_results_section(self, parent):
        # Frame de resultados
        results_frame = ctk.CTkFrame(parent)
        results_frame.grid(row=6, column=0, sticky="ew", padx=25, pady=20)
        results_frame.grid_columnconfigure(0, weight=1)
        
        # Título da seção
        section_title = ctk.CTkLabel(
            results_frame,
            text=">> Resultados da Consulta",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        section_title.grid(row=0, column=0, pady=(25, 20))
        
        # Frame scrollable para resultados
        self.results_scrollable = ctk.CTkScrollableFrame(
            results_frame,
            height=220,
            label_text="Dados retornados pela consulta"
        )
        self.results_scrollable.grid(row=1, column=0, padx=25, pady=(0, 25), sticky="ew")
        
        # Container para resultados
        self.results_container = self.results_scrollable
        self.create_results_placeholder()
        
        # Configurar rolagem contextual para os resultados
        self.setup_contextual_scrolling(self.results_scrollable, "results")
        
    def create_results_placeholder(self):
        placeholder = ctk.CTkLabel(
            self.results_container,
            text="Os resultados da consulta aparecerão aqui",
            font=ctk.CTkFont(size=13),
            text_color=("#6b7280", "#9ca3af")
        )
        placeholder.pack(pady=20)
        
    def clear_results(self):
        for widget in self.results_container.winfo_children():
            widget.destroy()
            
    def display_results(self, resultados, colunas):
        self.clear_results()
        
        if not colunas:
            success_label = ctk.CTkLabel(
                self.results_container,
                text="Comando executado com sucesso!",
                font=ctk.CTkFont(size=13, weight="bold"),
                text_color=self.colors['success']
            )
            success_label.pack(pady=20)
            return
            
        # Criar cabeçalho
        header_frame = ctk.CTkFrame(self.results_container)
        header_frame.pack(fill="x", padx=12, pady=(12, 8))
        
        for i, coluna in enumerate(colunas):
            header_label = ctk.CTkLabel(
                header_frame,
                text=coluna,
                font=ctk.CTkFont(size=12, weight="bold"),
                width=140,
                anchor="w"  # Alinhamento à esquerda
            )
            header_label.grid(row=0, column=i, padx=4, pady=4, sticky="ew")
            
        # Criar linhas de dados
        if resultados:
            for row_idx, linha in enumerate(resultados):
                row_frame = ctk.CTkFrame(
                    self.results_container,
                    fg_color=("gray90", "gray20") if row_idx % 2 == 0 else "transparent"
                )
                row_frame.pack(fill="x", padx=12, pady=2)
                
                for col_idx, valor in enumerate(linha):
                    cell_text = str(valor)[:45] + "..." if len(str(valor)) > 45 else str(valor)
                    cell_label = ctk.CTkLabel(
                        row_frame,
                        text=cell_text,
                        font=ctk.CTkFont(size=11),
                        width=140,
                        anchor="w"
                    )
                    cell_label.grid(row=0, column=col_idx, padx=4, pady=4, sticky="ew")
        else:
            no_data_label = ctk.CTkLabel(
                self.results_container,
                text="Nenhum resultado encontrado",
                font=ctk.CTkFont(size=13),
                text_color=("#6b7280", "#9ca3af")
            )
            no_data_label.pack(pady=20)
            
    def connect_and_load_schema(self):
        self.db_engine = self.db_engine_combo.get().strip().lower()
        user = self.user_entry.get().strip()
        password = self.password_entry.get().strip()
        dbname = self.dbname_entry.get().strip()

        if not all([self.db_engine, user, dbname]):
            messagebox.showerror("Erro de Conexão", "Motor, Usuário e Nome do Banco de Dados são obrigatórios.")
            return

        try:
            self.status_label.configure(text="* Conectando ao banco de dados...", text_color=("#f59e0b", "#fbbf24"))
            self.root.update()
            
            self.db = script.connect_db(self.db_engine, user, password, dbname)
            messagebox.showinfo("Conexão", "Conectado ao banco de dados com sucesso!")
            
            self.status_label.configure(text="* Carregando schema...", text_color=("#f59e0b", "#fbbf24"))
            self.root.update()
            
            self.schema = script.get_schema(self.db, self.db_engine)
            self.schema_text.configure(state="normal")
            self.schema_text.delete("1.0", "end")
            self.schema_text.insert("1.0", self.schema)
            self.schema_text.configure(state="disabled")
            
            self.generate_sql_button.configure(state="normal")
            
            self.status_label.configure(text="* Pronto para consultas!", text_color=("#10b981", "#34d399"))
        except Exception as e:
            messagebox.showerror("Erro de Conexão", f"Não foi possível conectar ou carregar o schema: {e}")
            if self.db:
                self.db.close()
                self.db = None
            self.generate_sql_button.configure(state="disabled")
            self.status_label.configure(text="* Erro na conexão", text_color=("#ef4444", "#f87171"))

    def generate_and_execute_sql(self):
        natural_query = self.natural_query_entry.get().strip()
        if not natural_query:
            messagebox.showwarning("Entrada Inválida", "Por favor, digite sua pergunta em linguagem natural.")
            return
        
        if not self.db or not self.schema:
            messagebox.showerror("Erro", "Não conectado ao banco de dados ou schema não carregado.")
            return

        try:
            self.status_label.configure(text="* Gerando SQL... Isso pode levar alguns segundos.", text_color=("#f59e0b", "#fbbf24"))
            self.generate_sql_button.configure(state="disabled")
            self.root.update()
            
            self.sql_output_text.delete("1.0", "end")
            self.clear_results()
            
            sql_query = script.generate_sql(self.schema, natural_query)
            self.sql_output_text.insert("1.0", sql_query)

            self.status_label.configure(text="* Executando consulta...", text_color=("#f59e0b", "#fbbf24"))
            self.root.update()

            resultados, colunas = script.execute_sql(self.db, sql_query)
            self.display_results(resultados, colunas)
                
            self.status_label.configure(text="* Consulta concluída com sucesso!", text_color=("#10b981", "#34d399"))
        except Exception as e:
            messagebox.showerror("Erro na Consulta", f"Erro ao gerar SQL ou executar a consulta: {e}")
            error_label = ctk.CTkLabel(
                self.results_container,
                text=f"Erro: {e}",
                font=ctk.CTkFont(size=13),
                text_color=("#ef4444", "#f87171")
            )
            error_label.pack(pady=20)
            self.status_label.configure(text="* Erro na consulta", text_color=("#ef4444", "#f87171"))
        finally:
            self.generate_sql_button.configure(state="normal")

    def on_closing(self):
        if self.db:
            try:
                self.db.close()
                print("Conexão com o banco de dados fechada.")
            except Exception as e:
                print(f"Erro ao fechar a conexão com o banco: {e}")
        self.root.destroy()

if __name__ == "__main__":
    # Configurar a janela principal
    root = ctk.CTk()
    app = App(root)
    
    # Configurar o evento de fechamento
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    
    # Executar a aplicação
    root.mainloop() 