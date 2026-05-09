import chess
from stockfish import Stockfish
import os

class StockfishEngine:
    def __init__(self, elo):
        """Stockfish motorunu başlat"""
        self.elo = elo
        self.skill_level = self._elo_to_skill_level(elo)
        
        try:
            # Stockfish'i başlat
            self.engine = Stockfish(
                depth=self.skill_level * 2,
                threads=4,
                parameters={
                    "Skill Level": self.skill_level,
                    "UCI_LimitStrength": True,
                    "UCI_Elo": elo
                }
            )
        except Exception as e:
            print(f"Hata: Stockfish bulunamadı. {e}")
            print("Lütfen Stockfish'i yükleyin:")
            print("  Windows: https://stockfishchess.org/download/")
            print("  macOS: brew install stockfish")
            print("  Ubuntu: sudo apt-get install stockfish")
            raise
    
    def _elo_to_skill_level(self, elo):
        """ELO'yu Stockfish Skill Level'a çevir"""
        # ELO 400-3200 -> Skill Level 0-20
        # Her 140 ELO = 1 Skill Level
        if elo < 1000:
            return min(5, (elo - 400) // 120)
        elif elo < 1600:
            return min(10, (elo - 1000) // 60 + 5)
        elif elo < 2200:
            return min(17, (elo - 1600) // 40 + 10)
        else:
            return 20
    
    def get_best_move(self, board):
        """En iyi hamleyi bul"""
        try:
            self.engine.set_fen_position(board.fen())
            
            # Düşünme süresi ELO'ya göre
            if self.elo < 1000:
                time_limit = 0.5
            elif self.elo < 1600:
                time_limit = 1
            elif self.elo < 2200:
                time_limit = 1.5
            else:
                time_limit = 2
            
            best_move_uci = self.engine.get_best_move()
            
            if best_move_uci:
                move = chess.Move.from_uci(best_move_uci)
                return move
            return None
        except Exception as e:
            print(f"Hamle hesaplanırken hata: {e}")
            return None
    
    def get_evaluation(self, board):
        """Pozisyonu değerlendir"""
        try:
            self.engine.set_fen_position(board.fen())
            return self.engine.get_evaluation()
        except:
            return None
    
    def quit(self):
        """Motoru kapat"""
        try:
            self.engine.quit()
        except:
            pass
