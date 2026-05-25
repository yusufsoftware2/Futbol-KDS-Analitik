import cv2
import numpy as np
# Bilgisayarlı görü ve segmentasyon için gerekli kütüphaneler
# Not: Gerçek senaryoda 'from ultralytics import YOLO' kullanılmaktadır.

class FootballAnalyticKDS:
    def __init__(self, frame_width=1920, frame_height=1080):
        # Saha ölçeklendirme katsayısı (Piksel -> Metre dönüşümü için)
        self.scale_factor_x = 105.0 / frame_width  # Standart saha uzunluğu: 105m
        self.scale_factor_y = 68.0 / frame_height  # Standart saha genişliği: 68m
        
    def segment_objects(self, frame):
        """
        YOLOv8-Seg modelini simüle eden ve video karesindeki 
        oyuncu koordinatları ile takım etiketlerini dönen fonksiyon.
        """
        # Test ve gösterim amacıyla simüle edilmiş oyuncu koordinatları (x, y)
        # Takım 0: Ev Sahibi, Takım 1: Deplasman
        simulated_detections = [
            {"id": 1, "team": 0, "coords": (400, 300)},
            {"id": 2, "team": 0, "coords": (450, 320)},
            {"id": 3, "team": 0, "coords": (600, 350)}, # En ileri oyuncu T0
            {"id": 4, "team": 0, "coords": (200, 280)}, # En geri oyuncu T0
            {"id": 5, "team": 1, "coords": (700, 500)},
            {"id": 6, "team": 1, "coords": (850, 520)},
        ]
        return simulated_detections

    def calculate_tactical_metrics(self, detections, target_team=0):
        """
        Segmente edilen oyuncuların koordinatlarından Takım Boyu ve Eni hesaplar.
        """
        team_coords = [obj["coords"] for obj in detections if obj["team"] == target_team]
        
        if len(team_coords) < 2:
            return 0, 0
            
        x_coords = [c[0] for c in team_coords]
        y_coords = [c[1] for c in team_coords]
        
        # Piksel farklarını metreye dönüştürme
        team_length = (max(x_coords) - min(x_coords)) * self.scale_factor_x
        team_width = (max(y_coords) - min(y_coords)) * self.scale_factor_y
        
        return round(team_length, 2), round(team_width, 2)

    def evaluate_kds_rules(self, team_length, team_width):
        """
        Hesaplanan metriklere göre Karar Destek Sistemi uyarıları üretir.
        """
        decision_outputs = []
        
        # Kural 1: Takım Boyu Kontrolü
        if team_length > 45.0:
            decision_outputs.append("KRITIK UYARI: Takım boyu çok uzadı (>45m)! Bloklar arası mesafeyi daraltın.")
        else:
            decision_outputs.append("DURUM NORMAL: Takım boyu kompakt yapıda.")
            
        # Kural 2: Takım Eni Kontrolü
        if team_width < 25.0:
            decision_outputs.append("TAKTIK ONERI: Takım çok dar alanda sıkıştı (<25m)! Oyunu kanatlara yayın.")
        else:
            decision_outputs.append("DURUM NORMAL: Saha yayılımı dengeli.")
            
        return decision_outputs

# --- Sistemin Çalıştırılması (Main Executable) ---
if __name__ == "__main__":
    # Örnek bir video karesi oluşturma (Sanal Saha)
    dummy_frame = np.zeros((1080, 1920, 3), dtype=np.uint8)
    
    # KDS Nesnesini Başlatma
    kds_system = FootballAnalyticKDS()
    
    # 1. Aşama: Segmentasyon ve Tespit Çıktılarının Alınması
    detections = kds_system.segment_objects(dummy_frame)
    
    # 2. Aşama: Metriklerin Hesaplanması (Takım 0 İçin)
    t_length, t_width = kds_system.calculate_tactical_metrics(detections, target_team=0)
    
    # 3. Aşama: Karar Destek Sisteminin Çalıştırılması
    kds_decisions = kds_system.evaluate_kds_rules(t_length, t_width)
    
    # Sonuçların Konsola Yazdırılması (Raporlama)
    print(f"--- ANALIZ SONUÇLARI ---")
    print(f"Hesaplanan Takım Boyu: {t_length} Metre")
    print(f"Hesaplanan Takım Eni: {t_width} Metre")
    print(f"--- KDS SISTEM CIKTILARI ---")
    for decision in kds_decisions:
        print(f"- {decision}")