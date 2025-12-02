import sys
import os
import pandas as pd

# Tambahkan root project ke path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.evaluation.data import TEST_QUESTIONS
from app.evaluation.manager import EvalManager

def main():
    print("🚀 Initializing Evaluation Manager...")
    
    # 1. Inisialisasi Manager
    manager = EvalManager()
    
    # 2. Jalankan Evaluasi
    results = manager.run_evaluation(TEST_QUESTIONS)
    
    # 3. Tampilkan Hasil Rapih
    print("\n📊 === HASIL EVALUASI RAGAS === 📊")
    df = results.to_pandas()
    
    # Konfigurasi tampilan tabel pandas agar tidak terpotong
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', 1000)
    pd.set_option('display.max_colwidth', 50) # Batasi panjang teks biar rapi
    
    print(df)
    print("\n📈 Rata-rata Skor Keseluruhan:")
    print(results)

if __name__ == "__main__":
    main()