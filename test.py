import google.generativeai as genai

genai.configure(api_key="AQ.Ab8RN6INLCbKoLpnIf8bYBFOrydyAkk2A-Ol1sdhqAN7WlKPQg")

print("Models available:")

for model in genai.list_models():
    print(model.name)