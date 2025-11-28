"""
Script para verificar qué modelos de Gemini están disponibles con tu API key
"""

import google.generativeai as genai

# Coloca tu API key aquí temporalmente (BÓRRALA después)
API_KEY = ""

genai.configure(api_key=API_KEY)

print("=" * 60)
print("MODELOS DISPONIBLES EN TU CUENTA DE GEMINI:")
print("=" * 60)

try:
    for model in genai.list_models():
        if 'generateContent' in model.supported_generation_methods:
            print(f"\n✓ {model.name}")
            print(f"  Display name: {model.display_name}")
            print(f"  Description: {model.description[:100]}...")
except Exception as e:
    print(f"Error listando modelos: {e}")

print("\n" + "=" * 60)
