# sgr_anonymizer/model_loader.py
import os
from pathlib import Path
from llama_cpp import Llama
from dotenv import load_dotenv

load_dotenv()

def get_or_download_model(
    repo_id: str = None,
    filename: str = "Qwen2.5-7B-Instruct-Q4_K_M.gguf",
    local_dir: str = "models"
) -> str:
    model_dir = Path(local_dir)
    model_path = model_dir / filename
    if not model_path.exists():
        raise FileNotFoundError(f"Модель не найдена: {model_path}. Поместите GGUF-файл в папку models/.")
    return str(model_path)

def load_llm(model_path: str, n_ctx: int = 4096) -> Llama:
    use_gpu = os.getenv("USE_GPU", "0") == "1"
    n_gpu_layers = -1 if use_gpu else 0  # ← только 0 для CPU
    return Llama(
        model_path=model_path,
        n_ctx=n_ctx,
        n_gpu_layers=n_gpu_layers,  # ← 0 = только CPU
        n_threads=8,
        verbose=False
    )