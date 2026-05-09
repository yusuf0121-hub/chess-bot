import tkinter as tk
import tkinter.font as tkFont
from tkinter import messagebox, scrolledtext
import chess
from stockfish_engine import StockfishEngine
import threading

class ChessGUI:
    def __init__(self, root, elo, return_to_menu):
        self.root = root
        self.elo = elo
        self.return_to_menu = return_to_menu
        self.board = chess.Board()
        self.engine = StockfishEngine(elo)
        self.selected_square = None
        self.valid_moves = []
        self.move_history = []
        self.game_over = False
        self.bot_thinking = False
        
        # Ana frame
        self.main_frame = tk.Frame(root, bg="#2b2b2b")
        self.main_frame.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
        
        # Başlık
        title_font = tkFont.Font(family="Helvetica", size=16, weight="bold")
        title = tk.Label(self.main_frame, text="♟ Chess Bot - İnsan vs Stockfish", 
                        font=title_font, fg="#ffffff", bg="#2b2b2b")
        title.pack(pady=10)
        
        # Alt frame - Tahta ve sağ panel
        game_frame = tk.Frame(self.main_frame, bg="#2b2b2b")
        game_frame.pack(expand=True, fill=tk.BOTH)
        
        # Sol - Satranç tahtası
        board_frame = tk.Frame(game_frame, bg="#2b2b2b")
        board_frame.pack(side=tk.LEFT, padx=10, pady=10)
        
        self.canvas = tk.Canvas(board_frame, width=480, height=480, bg="#1a1a1a")
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.on_square_click)
        
        # Sağ panel
        right_frame = tk.Frame(game_frame, bg="#3b3b3b", width=300)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10)
        right_frame.pack_propagate(False)
        
        # Durum
        status_label = tk.Label(right_frame, text="Oyun Durumu", 
                               font=("Helvetica", 12, "bold"), fg="#ffff00", bg="#3b3b3b")
        status_label.pack(pady=5)
        
        self.status_text = tk.Label(right_frame, text="Beyaz oyuncusu sırasında...", 
                                   font=("Helvetica", 10), fg="#cccccc", bg="#3b3b3b",
                                   wraplength=280, justify=tk.LEFT)
        self.status_text.pack(pady=5)
        
        # Hamle geçmişi
        moves_label = tk.Label(right_frame, text="Hamle Geçmişi", 
                              font=("Helvetica", 12, "bold"), fg="#ffff00", bg="#3b3b3b")
        moves_label.pack(pady=5)
        
        self.moves_text = scrolledtext.ScrolledText(right_frame, height=6, width=35,
                                                   bg="#2b2b2b", fg="#00ff00",
                                                   font=("Courier", 9))
        self.moves_text.pack(pady=5, padx=5, fill=tk.BOTH, expand=True)
        self.moves_text.config(state=tk.DISABLED)
        
        # Bot Sohbeti
        chat_label = tk.Label(right_frame, text="Bot Sohbeti", 
                             font=("Helvetica", 12, "bold"), fg="#ffff00", bg="#3b3b3b")
        chat_label.pack(pady=5)
        
        self.chat_text = scrolledtext.ScrolledText(right_frame, height=6, width=35,
                                                  bg="#2b2b2b", fg="#00aaff",
                                                  font=("Courier", 9))
        self.chat_text.pack(pady=5, padx=5, fill=tk.BOTH, expand=True)
        self.chat_text.config(state=tk.DISABLED)
        
        # ELO Bilgisi
        elo_label = tk.Label(right_frame, text=f"Bot ELO: {self.elo}", 
                            font=("Helvetica", 11, "bold"), fg="#ff00ff", bg="#3b3b3b")
        elo_label.pack(pady=10)
        
        # Butonlar
        button_frame = tk.Frame(right_frame, bg="#3b3b3b")
        button_frame.pack(pady=10, fill=tk.X, padx=5)
        
        undo_button = tk.Button(button_frame, text="↶ Geri Al", 
                               bg="#ff8800", fg="#ffffff", font=("Helvetica", 10),
                               command=self.undo_move)
        undo_button.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        menu_button = tk.Button(button_frame, text="📋 Menu", 
                               bg="#0088ff", fg="#ffffff", font=("Helvetica", 10),
                               command=self.return_to_menu_click)
        menu_button.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        self.draw_board()
        self.add_chat_message("Bot", "Hoş geldin! Ben Stockfish'im. Başlayabilirsin!")
    
    def draw_board(self):
        """Satranç tahtasını çiz"""
        self.canvas.delete("all")
        
        colors = ["#f0d9b5", "#baca44"]  # Açık ve koyu renkler
        piece_symbols = {
            'P': '♙', 'N': '♘', 'B': '♗', 'R': '♖', 'Q': '♕', 'K': '♔',
            'p': '♟', 'n': '♞', 'b': '♝', 'r': '♜', 'q': '♛', 'k': '♚'
        }
        
        square_size = 60
        
        for row in range(8):
            for col in range(8):
                square = chess.square(col, 7 - row)
                x0 = col * square_size
                y0 = row * square_size
                x1 = x0 + square_size
                y1 = y0 + square_size
                
                # Kare rengi
                color_idx = (row + col) % 2
                color = colors[color_idx]
                
                # Seçili kareyi vurgula
                if square == self.selected_square:
                    color = "#baca44" if color_idx == 0 else "#a89d38"
                elif square in self.valid_moves:
                    color = "#7ec926"
                
                self.canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="#666")
                
                # Taş
                piece = self.board.piece_at(square)
                if piece:
                    symbol = piece_symbols[piece.symbol()]
                    text_color = "#ffffff" if piece.color else "#000000"
                    self.canvas.create_text(x0 + square_size/2, y0 + square_size/2,
                                          text=symbol, font=("Arial", 36, "bold"),
                                          fill=text_color)
                
                # Koordinatlar
                if col == 0:
                    self.canvas.create_text(5, y0 + square_size - 5, text=str(8 - row),
                                          font=("Arial", 8), fill="#666")
                if row == 7:
                    self.canvas.create_text(x1 - 5, y1 - 5, text=chr(97 + col),
                                          font=("Arial", 8), fill="#666")
        
        # Oyun durumunu güncelle
        self.update_status()
    
    def on_square_click(self, event):
        """Kareye tıklanma olayı"""
        if self.game_over or self.bot_thinking:
            return
        
        col = event.x // 60
        row = event.y // 60
        
        if col < 0 or col > 7 or row < 0 or row > 7:
            return
        
        square = chess.square(col, 7 - row)
        
        if self.selected_square is None:
            # Taş seç
            piece = self.board.piece_at(square)
            if piece and piece.color == chess.WHITE:
                self.selected_square = square
                self.valid_moves = [move.to_square for move in self.board.legal_moves 
                                   if move.from_square == square]
        else:
            # Hamle yap
            if square == self.selected_square:
                self.selected_square = None
                self.valid_moves = []
            else:
                move = chess.Move(self.selected_square, square)
                if move in self.board.legal_moves:
                    self.make_move(move)
                    self.selected_square = None
                    self.valid_moves = []
                    self.bot_move()
                else:
                    self.selected_square = None
                    self.valid_moves = []
        
        self.draw_board()
    
    def make_move(self, move):
        """Hamle yap"""
        self.board.push(move)
        self.move_history.append(move)
        self.moves_text.config(state=tk.NORMAL)
        move_san = self.board.san(move)
        self.moves_text.insert(tk.END, f"{len(self.move_history)}. {move_san}\n")
        self.moves_text.config(state=tk.DISABLED)
        self.moves_text.see(tk.END)
    
    def bot_move(self):
        """Bot hamle yap (threaded)"""
        if self.board.is_game_over():
            self.end_game()
            return
        
        self.bot_thinking = True
        self.status_text.config(text="Bot düşünüyor...")
        
        # Threading kullan
        thread = threading.Thread(target=self._bot_move_thread)
        thread.start()
    
    def _bot_move_thread(self):
        """Bot hamle thread'inde"""
        try:
            move = self.engine.get_best_move(self.board)
            if move:
                self.make_move(move)
                
                # Bot mesajı
                messages = [
                    "İyi hamle! Ama ben hala kazanacağım!",
                    "Hmm, ilginç bir hamle...",
                    "Beni hafife alma, çok güçlüyüm!",
                    "Güzel ama yetersiz!",
                    "Stratejini okuyabiliyorum!",
                    "Bravo! Ama ben daha iyiyim.",
                    "Bu hamle bana yardımcı oldu.",
                    "Zamanın bitti, benim sıram!"
                ]
                import random
                msg = random.choice(messages)
                self.add_chat_message("Bot", msg)
                
                if self.board.is_game_over():
                    self.end_game()
        except:
            pass
        finally:
            self.bot_thinking = False
            self.draw_board()
    
    def add_chat_message(self, sender, message):
        """Sohbet mesajı ekle"""
        self.chat_text.config(state=tk.NORMAL)
        self.chat_text.insert(tk.END, f"{sender}: {message}\n\n")
        self.chat_text.config(state=tk.DISABLED)
        self.chat_text.see(tk.END)
    
    def update_status(self):
        """Oyun durumunu güncelle"""
        if self.board.is_game_over():
            self.end_game()
        else:
            player = "Beyaz (Sen)" if self.board.turn else "Siyah (Bot)"
            status = f"{player} sırasında...\n"
            
            if self.board.is_check():
                status += "Kral tehdit altında!"
            
            self.status_text.config(text=status)
    
    def end_game(self):
        """Oyunu bitir"""
        self.game_over = True
        
        if self.board.is_checkmate():
            if self.board.turn:
                result = "Bot Kazandı! Şah Matt!"
                self.add_chat_message("Bot", "Kazandım! İyi oynadın ama ben daha iyi!")
            else:
                result = "Sen Kazandın! Şah Matt!"
                self.add_chat_message("Bot", "Tebrik ederim! Çok iyi oynadın!")
        elif self.board.is_stalemate():
            result = "Berabere - Stalemate!"
            self.add_chat_message("Bot", "Berabere! Sana daha çalışman gerek.")
        elif self.board.is_insufficient_material():
            result = "Berabere - Yetersiz Malzeme!"
            self.add_chat_message("Bot", "Berabere! İyi mücadele etti.")
        else:
            result = "Oyun Bitti!"
        
        self.status_text.config(text=result)
        messagebox.showinfo("Oyun Bitti", result)
    
    def undo_move(self):
        """Son hamleyi geri al"""
        if len(self.move_history) > 0 and not self.game_over:
            # İnsan hamlesini geri al
            self.board.pop()
            self.move_history.pop()
            
            # Bot hamlesini geri al
            if len(self.move_history) > 0:
                self.board.pop()
                self.move_history.pop()
            
            # Hamle geçmişini güncelle
            self.moves_text.config(state=tk.NORMAL)
            self.moves_text.delete(1.0, tk.END)
            for i, move in enumerate(self.move_history):
                self.moves_text.insert(tk.END, f"{i+1}. {self.board.san(move)}\n")
            self.moves_text.config(state=tk.DISABLED)
            
            self.draw_board()
    
    def return_to_menu_click(self):
        """Menüye dön"""
        if messagebox.askyesno("Menüye Dön", "Oyunu bırakmak istediğinize emin misiniz?"):
            self.engine.quit()
            for widget in self.root.winfo_children():
                widget.destroy()
            self.return_to_menu()
