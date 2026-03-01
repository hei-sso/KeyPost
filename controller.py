import data_module
from ai_module import GeminiAI
import time

def run_automation(api_key, base_prompt, num_keywords, log_callback, on_finish):
    try:
        ai = GeminiAI(api_key)
        
        # 1단계: 주제 수집, 요약 생성 및 엑셀 우선 저장
        log_callback(f"▶ 1단계: 실시간 트렌드 기사 제목 수집 중... (목표: {num_keywords}개)")
        keywords = data_module.fetch_trending_keywords(num_keywords)
        
        # 수집된 키워드가 없으면 에러를 띄우고 여기서 바로 함수 종료 (return)
        if not keywords:
            log_callback("\n[Error] 키워드 수집 불가: 네이버 뉴스 수집에 실패했습니다. 작업을 중단합니다.")
            return

        log_callback(f"총 {len(keywords)}개의 주제 수집 완료. 한 줄 요약을 시작합니다.\n")
        data_list = []

        for idx, keyword in enumerate(keywords, start=1):
            log_callback(f"[요약 {idx}/{len(keywords)}] '{keyword}' 요약 중...")
            try:
                summary = ai.get_summary(keyword)
                log_callback("  └ 요약 완료.")
            except Exception as e:
                summary = "요약 실패"
                log_callback(f"  └ [Error] 요약 생성 실패: {e}")

            data_list.append({"번호": idx, "키워드": keyword, "한줄요약": summary})
            
            if idx < len(keywords):
                time.sleep(12) 

        excel_name = "블로그_트렌드_수집결과.xlsx"
        data_module.save_to_excel(data_list, excel_name)
        log_callback(f"\n★ 1단계 완료! '{excel_name}' 파일이 안전하게 저장되었습니다. ★\n")

        # 2단계: 저장된 목록을 바탕으로 블로그 및 이미지 생성
        log_callback("▶ 2단계: 수집된 주제로 블로그 포스팅 생성을 시작합니다.\n")
        
        for item in data_list:
            idx = item["번호"]
            keyword = item["키워드"]
            
            log_callback(f"[글 {idx}/{len(data_list)}] '{keyword}' 작성 중...")
            
            try:
                title, safe_title, content = ai.get_blog_post(keyword, base_prompt)
                data_module.save_blog_text(idx, safe_title, title, content)
                log_callback("  └ 글 작성 및 파일 저장 완료.")
            except Exception as e:
                safe_title = "".join(c for c in keyword if c not in r'\/:*?"<>|')[:30] 
                log_callback(f"  └ [Error] 글 작성 실패: {e}")

            try:
                image_bytes = ai.get_image_bytes(keyword)
                if image_bytes:
                    data_module.save_image(idx, safe_title, image_bytes)
                    log_callback("  └ 이미지 생성 및 파일 저장 완료.")
                else:
                    log_callback("  └ [Error] 생성된 이미지가 없습니다.")
            except Exception as e:
                log_callback(f"  └ [Error] 이미지 생성 실패: {e}")
                
            if idx < len(data_list):
                log_callback("  └ 속도 제한 방지를 위해 30초 대기 중...\n")
                time.sleep(30)

        log_callback("\n🎉 모든 자동화 작업이 성공적으로 끝났습니다!")

    except Exception as e:
        log_callback(f"\n치명적인 오류 발생: {e}")
    finally:
        on_finish()
        