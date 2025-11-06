from .core_sgr_fixed import SGRFixedAnonymizer

# Для обратной совместимости
SGRAnonymizer = SGRFixedAnonymizer

__all__ = ["SGRFixedAnonymizer", "SGRAnonymizer"]