from llama_cpp import Llama
llm = Llama(model_path="models/Qwen2.5-7B-Instruct-Q4_K_M.gguf", n_gpu_layers=1, vocab_only=True)
print("✅ GPU поддержка работает!")