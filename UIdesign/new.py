import google.generativeai as genai

genai.configure(api_key="AIzaSyCsxihphRnek2p2B7qx3NBM4T3nUwpwwLo")

models = genai.list_models()
for model in models:
    print(model.name, model.supported_generation_methods)
