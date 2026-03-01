from google import genai

api_key = "본인 API 키"
client = genai.Client(api_key=api_key)

print("=== 사용 가능한 텍스트 모델 (Gemini) ===")
for m in client.models.list():
    if "gemini" in m.name.lower():
        print(m.name)

print("\n=== 사용 가능한 이미지 모델 (Imagen) ===")
for m in client.models.list():
    if "imagen" in m.name.lower():
        print(m.name)
        