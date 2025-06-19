import json
import os
from datetime import datetime

class RecordManager:
    def __init__(self):
        self.records_file = "battleship_records.json"
        self.records = self.load_records()
    
    def load_records(self):
        """Загрузка рекордов из файла"""
        try:
            if os.path.exists(self.records_file):
                with open(self.records_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except:
            pass
        
        return {
            "vs_computer": {"time": None, "date": None, "player_name": None},
            "vs_player": {"time": None, "date": None, "player_name": None}
        }
    
    def save_records(self):
        """Сохранение рекордов"""
        try:
            with open(self.records_file, 'w', encoding='utf-8') as f:
                json.dump(self.records, f, ensure_ascii=False, indent=4)
        except:
            pass