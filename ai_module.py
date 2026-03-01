from google import genai
from google.genai import types

class GeminiAI:
    def __init__(self, api_key):
        self.client = genai.Client(api_key=api_key)
        self.text_model = 'gemini-2.5-flash-lite' 
        self.image_model = 'gemini-3.1-flash-image-preview'

    # 기사 제목에 대한 한 줄 요약 생성
    def get_summary(self, keyword):
        prompt = f"'{keyword}'에 대한 최신 이슈나 의미를 한 줄(50자 이내)로 요약해 줘."
        response = self.client.models.generate_content(
            model=self.text_model,
            contents=prompt,
        )
        return response.text.strip()

    # 블로그 제목과 본문 생성
    def get_blog_post(self, keyword, base_prompt):
        full_prompt = base_prompt.replace("{keyword}", keyword)
        response = self.client.models.generate_content(
            model=self.text_model,
            contents=full_prompt,
        )
        content = response.text
        title = content.split('\n')[0].replace("#", "").strip()
        safe_title = "".join(c for c in title if c not in r'\/:*?"<>|')[:30]
        if not safe_title:
            safe_title = keyword
        return title, safe_title, content

    # 이미지 생성 및 추출
    def get_image_bytes(self, keyword):
        prompt = f"주제: {keyword}. 이 주제를 잘 나타내는 현대적이고 세련된 블로그 썸네일 이미지를 실사 느낌으로 그려줘. 글자는 넣지 마."
        
        try:
            # 나노 바나나는 generate_images가 아닌 generate_content를 사용해야 함!
            response = self.client.models.generate_content(
                model=self.image_model,
                contents=[prompt]
            )
            
            # 응답 후보군(candidates) 중 첫 번째 결과의 파트(parts)에서 이미지 데이터(inline_data) 찾기
            if response.candidates and response.candidates[0].content.parts:
                for part in response.candidates[0].content.parts:
                    if part.inline_data:
                        return part.inline_data.data
            
            raise Exception("응답에서 이미지 데이터를 찾을 수 없습니다.")
                
        except Exception as e:
            # 상세 에러 메시지를 포함하여 예외 던지기
            raise Exception(f"나노 바나나 이미지 생성 실패: {e}")
        