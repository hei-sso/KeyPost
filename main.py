import tkinter as tk
from tkinter import messagebox, scrolledtext
from tkinter import ttk
import threading
from controller import run_automation

class BlogApp:
    def __init__(self, root):
        self.root = root
        self.root.title("KeyPost")
        self.root.geometry("600x700")

        # API Key 입력
        tk.Label(root, text="Gemini API Key:").pack(pady=(10, 0))
        self.api_entry = tk.Entry(root, width=60, show="*")
        self.api_entry.pack(pady=5)

        # 키워드(글) 개수 선택 창
        tk.Label(root, text="생성할 블로그 글 개수 (1~30개):").pack(pady=(10, 0))
        self.keyword_count_var = tk.IntVar(value=10) # 기본값은 10개로 설정
        self.count_combobox = ttk.Combobox(root, textvariable=self.keyword_count_var, values=list(range(1, 31)), width=10, state="readonly")
        self.count_combobox.pack(pady=5)

        # 프롬프트 입력창
        tk.Label(root, text="블로그 작성 프롬프트 (수정 가능):").pack(pady=(10, 0))
        self.prompt_text = scrolledtext.ScrolledText(root, width=70, height=15)
        self.prompt_text.pack(pady=5)
        
        default_prompt = (
            "당신은 인기 있는 네이버 블로거입니다.\n"
            "다음 주제에 대해 사람들의 이목을 끄는 정보성 블로그 글을 작성해 주세요.\n\n"
            "[작성 규칙]\n"
            "1. 글의 첫 줄은 무조건 '새로 생성한 제목'으로 작성하세요. (예: 늘어나는 2030 녹내장, 스마트폰이 원인?)\n"
            "2. 제목에는 '안녕하세요' 같은 인사말이나 블로거 소개를 절대 넣지 마세요.\n"
            "3. 두 번째 줄부터 본문을 시작하며, 서론, 본론, 결론으로 나누어 이모지와 함께 친근하게 작성하세요.\n"
            "4. 마지막에는 글의 내용과 관련된 해시태그로 마무리하세요.\n\n"
            "주제: {keyword}"
        )
        self.prompt_text.insert(tk.END, default_prompt)

        # 로그 출력창
        tk.Label(root, text="진행 상황:").pack(pady=(10, 0))
        self.log_text = scrolledtext.ScrolledText(root, width=70, height=10, state=tk.DISABLED)
        self.log_text.pack(pady=5)

        # 시작 버튼
        self.start_btn = tk.Button(root, text="프로그램 시작", command=self.start_process, bg="#4CAF50", fg="white", font=("Arial", 12, "bold"))
        self.start_btn.pack(pady=15)

    # 컨트롤러에서 보내는 메시지를 GUI 창에 출력
    def log(self, message):
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)
        self.root.update()

    # 작업이 끝나면 버튼을 다시 활성화
    def enable_button(self):
        self.start_btn.config(state=tk.NORMAL)

    def start_process(self):
        api_key = self.api_entry.get().strip()
        base_prompt = self.prompt_text.get("1.0", tk.END).strip()
        
        # 콤보박스에서 선택한 숫자 가져오기
        try:
            num_keywords = self.keyword_count_var.get()
        except Exception:
            num_keywords = 10

        if not api_key:
            messagebox.showwarning("경고", "API Key를 입력해 주세요.")
            return
        if not base_prompt:
            messagebox.showwarning("경고", "프롬프트를 입력해 주세요.")
            return

        self.start_btn.config(state=tk.DISABLED)
        self.log_text.config(state=tk.NORMAL)
        self.log_text.delete("1.0", tk.END)
        self.log_text.config(state=tk.DISABLED)
        
        # 컨트롤러에 선택한 개수(num_keywords)를 함께 전달
        thread = threading.Thread(
            target=run_automation, 
            args=(api_key, base_prompt, num_keywords, self.log, self.enable_button)
        )
        thread.daemon = True
        thread.start()

if __name__ == "__main__":
    root = tk.Tk()
    app = BlogApp(root)
    root.mainloop()
    