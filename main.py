import tkinter as tk
from tkinter import messagebox
import tkinter.font as tkFont
from chess_gui import ChessGUI
import os

class ChessBotApp:
    def __init__(self, root):
        self.root = root
        self.root.title("♟ Chess Bot - İnsan vs Stockfish")
        self.root.geometry("900x700")
        self.root.configure(bg="#2b2b2b")
        
        # Varsayılan ELO
        self.selected_elo = 1200
        self.chess_gui = None
        
        # Başlangıç ekranını göster
        self.show_welcome_screen()
    
    def show_welcome_screen(self):
        """Hoş geldiniz ekranını göster"""
        # Mevcut widgetleri temizle
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Ana frame
        main_frame = tk.Frame(self.root, bg="#2b2b2b")
        main_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)
        
        # Başlık
        title_font = tkFont.Font(family="Helvetica", size=32, weight="bold")
        title = tk.Label(main_frame, text="♟ CHESS BOT ♟", font=title_font, 
                        fg="#ffffff", bg="#2b2b2b")
        title.pack(pady=20)
        
        # Hoş geldiniz metni
        welcome_font = tkFont.Font(family="Helvetica", size=14)
        welcome = tk.Label(main_frame, text="Stockfish Yapay Zekası ile Satranç Oynayın!", 
                           font=welcome_font, fg="#cccccc", bg="#2b2b2b")
        welcome.pack(pady=10)
        
        # ELO seçim frame
        elo_frame = tk.Frame(main_frame, bg="#3b3b3b", relief=tk.RAISED, bd=2)
        elo_frame.pack(pady=30, padx=20, fill=tk.X)
        
        # ELO başlığı
        elo_title = tk.Label(elo_frame, text="Bot ELO Seviyesi Seçin", 
                             font=("Helvetica", 12, "bold"), fg="#ffff00", bg="#3b3b3b")
        elo_title.pack(pady=10)
        
        # Slider frame
        slider_frame = tk.Frame(elo_frame, bg="#3b3b3b")
        slider_frame.pack(pady=10, padx=20, fill=tk.X)
        
        # ELO değeri label
        self.elo_label = tk.Label(slider_frame, text=f"ELO: {self.selected_elo}", 
                                  font=("Helvetica", 16, "bold"), fg="#00ff00", bg="#3b3b3b")
        self.elo_label.pack(side=tk.LEFT, padx=10)
        
        # Slider
        self.elo_slider = tk.Scale(slider_frame, from_=400, to=3200, orient=tk.HORIZONTAL,
                                   bg="#4b4b4b", fg="#ffffff", length=300,
                                   command=self.update_elo_display,
                                   troughcolor="#2b2b2b", highlightthickness=0)
        self.elo_slider.set(self.selected_elo)
        self.elo_slider.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)
        
        # Zorluk göstergesi
        self.difficulty_label = tk.Label(slider_frame, text="🟡 Amatör", 
                                         font=("Helvetica", 12, "bold"), fg="#ffaa00", bg="#3b3b3b")
        self.difficulty_label.pack(side=tk.LEFT, padx=10)
        
        # Bilgi kutusu
        info_frame = tk.Frame(main_frame, bg="#3b3b3b", relief=tk.SUNKEN, bd=1)
        info_frame.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)
        
        info_text = """🎯 ELO SEVİYELERİ:

🟢 400-1000: Başlangıç
    → Acemi oyuncuların pratik yapması için

🟡 1000-1600: Amatör
    → Temel stratejileri bilenler için

🔴 1600-2200: İleri
    → Deneyimli oyuncuların antrenmanı için

⚫ 2200-3200: Uzman
    → Profesyonel seviye oyuncular için"""
        
        info_label = tk.Label(info_frame, text=info_text, font=("Courier", 10),
                             fg="#cccccc", bg="#3b3b3b", justify=tk.LEFT)
        info_label.pack(padx=15, pady=15)
        
        # Başla butonu
        button_frame = tk.Frame(main_frame, bg="#2b2b2b")
        button_frame.pack(pady=20)
        
        start_button = tk.Button(button_frame, text="🎮 Oyuna Başla", 
                                font=("Helvetica", 14, "bold"), 
                                bg="#00aa00", fg="#ffffff",
                                padx=30, pady=15, cursor="hand2",
                                command=self.start_game)
        start_button.pack()
    
    def update_elo_display(self, value):
        """ELO değerini güncelle"""
        elo = int(value)
        self.selected_elo = elo
        self.elo_label.config(text=f"ELO: {elo}")
        
        # Zorluk seviyesi göster
        if elo < 1000:
            difficulty = "🟢 Başlangıç"
            color = "#00ff00"
        elif elo < 1600:
            difficulty = "🟡 Amatör"
            color = "#ffaa00"
        elif elo < 2200:
            difficulty = "🔴 İleri"
            color = "#ff6600"
        else:
            difficulty = "⚫ Uzman"
            color = "#aa0000"
        
        self.difficulty_label.config(text=difficulty, fg=color)
    
    def start_game(self):
        """Oyunu başlat"""
        # Mevcut widgetleri temizle
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Chess GUI'yi oluştur
        self.chess_gui = ChessGUI(self.root, self.selected_elo, self.show_welcome_screen)

if __name__ == "__main__":
    root = tk.Tk()
    app = ChessBotApp(root)
    root.mainloop()
