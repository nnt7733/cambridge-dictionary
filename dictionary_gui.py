import tkinter as tk
from tkinter import ttk, messagebox
import requests
from bs4 import BeautifulSoup
import pyttsx3
from deep_translator import GoogleTranslator
import google.generativeai as genai
import threading
import json
import os
from datetime import datetime
import time
import sys
import bisect

class CambridgeDictionaryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Cambridge Dictionary")
        self.root.geometry("1000x750")
        self.root.resizable(True, True)
        
        # Khởi tạo TTS engine
        try:
            self.tts_engine = pyttsx3.init()
        except:
            self.tts_engine = None
        
        # Translator với retry logic
        self.translator = GoogleTranslator(source='en', target='vi')
        # Gemini context-aware
        self.gemini_api_key = os.getenv('GEMINI_API_KEY', 'AIzaSyCz0JtTfcbSjhQ54wux1QPHvQGDGCjbzmw').strip()
        self.gemini_enabled = False
        if self.gemini_api_key:
            try:
                genai.configure(api_key=self.gemini_api_key)
                self.gemini_model = genai.GenerativeModel('gemini-1.5-flash')
                self.gemini_enabled = True
            except Exception:
                self.gemini_enabled = False
        
        # Cache để tăng tốc EXTREME
        self.translation_cache = {}
        self.word_cache = {}  # Cache cả từ đã tra
        
        # File lưu từ vựng
        self.vocab_file = "my_vocabulary.json"
        self.load_vocabulary()
        
        # Session để tái sử dụng kết nối
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
        # Load cache
        self.load_cache()
        
        # Thiết lập giao diện
        self.setup_ui()
        
    def load_cache(self):
        """Load translation cache từ file"""
        try:
            if os.path.exists('translation_cache.json'):
                with open('translation_cache.json', 'r', encoding='utf-8') as f:
                    self.translation_cache = json.load(f)
        except:
            pass
    
    def save_cache(self):
        """Lưu translation cache"""
        try:
            with open('translation_cache.json', 'w', encoding='utf-8') as f:
                json.dump(self.translation_cache, f, ensure_ascii=False, indent=2)
        except:
            pass
        
    def load_vocabulary(self):
        """Load từ vựng đã lưu"""
        try:
            if os.path.exists(self.vocab_file):
                with open(self.vocab_file, 'r', encoding='utf-8') as f:
                    self.vocabulary = json.load(f)
            else:
                self.vocabulary = []
        except:
            self.vocabulary = []
    
    def save_vocabulary(self):
        """Lưu từ vựng"""
        try:
            with open(self.vocab_file, 'w', encoding='utf-8') as f:
                json.dump(self.vocabulary, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Lỗi khi lưu từ vựng: {e}")
    
    def add_to_vocabulary(self, word, phonetic_uk, phonetic_us, definitions, ai_vi=None, ai_example_en=None):
        """Thêm từ vào danh sách ghi nhớ"""
        vocab_item = {
            'word': word,
            'phonetic_uk': phonetic_uk,
            'phonetic_us': phonetic_us,
            'definitions': definitions,
            'added_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        if ai_vi:
            vocab_item['ai_vi'] = ai_vi
        if ai_example_en:
            vocab_item['ai_example_en'] = ai_example_en
        
        for item in self.vocabulary:
            if item['word'].lower() == word.lower():
                messagebox.showinfo("Thông báo", f"Từ '{word}' đã có trong danh sách!")
                return
        
        self.vocabulary.append(vocab_item)
        self.save_vocabulary()
        messagebox.showinfo("Thành công", f"Đã thêm '{word}' vào danh sách!")
        
    def setup_ui(self):
        # Colors
        CAMBRIDGE_BLUE = "#00A7E1"
        DARK_BLUE = "#002147"
        
        # Header
        header_frame = tk.Frame(self.root, bg=DARK_BLUE, height=70)
        header_frame.pack(fill=tk.X)
        
        title_label = tk.Label(
            header_frame,
            text="Cambridge Dictionary",
            font=("Georgia", 24, "bold"),
            bg=DARK_BLUE,
            fg="white",
            pady=15
        )
        title_label.pack()
        
        # Search Frame
        search_frame = tk.Frame(self.root, bg="white", height=80)
        search_frame.pack(fill=tk.X, padx=30, pady=20)
        
        search_container = tk.Frame(search_frame, bg="white")
        search_container.pack(fill=tk.X)
        
        # Entry frame với suggestion
        entry_wrapper = tk.Frame(search_container, bg="white")
        entry_wrapper.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        self.word_entry = tk.Entry(
            entry_wrapper,
            font=("Arial", 16),
            relief=tk.SOLID,
            borderwidth=2
        )
        self.word_entry.pack(fill=tk.X, ipady=8)
        self.word_entry.bind('<Return>', lambda e: self.search_word())
        self.word_entry.bind('<KeyRelease>', self.on_key_release)
        
        # Suggestion listbox (ẩn ban đầu)
        self.suggestion_listbox = tk.Listbox(
            entry_wrapper,
            font=("Arial", 12),
            height=5,
            relief=tk.SOLID,
            borderwidth=1
        )
        self.suggestion_listbox.bind('<<ListboxSelect>>', self.on_suggestion_select)
        self.suggestion_listbox.bind('<Button-1>', self.on_suggestion_click)
        
        # History từ đã tra
        self.search_history = []
        
        # Load common words từ file
        self.common_words = self.load_common_words()
        
        self.search_btn = tk.Button(
            search_container,
            text="🔍 Search",
            font=("Arial", 14, "bold"),
            bg=CAMBRIDGE_BLUE,
            fg="white",
            relief=tk.FLAT,
            padx=25,
            pady=10,
            cursor="hand2",
            command=self.search_word
        )
        self.search_btn.pack(side=tk.LEFT, padx=(10, 0))
        
        self.add_vocab_btn = tk.Button(
            search_container,
            text="📚 Ghi nhớ",
            font=("Arial", 12),
            bg="#27AE60",
            fg="white",
            relief=tk.FLAT,
            padx=15,
            pady=10,
            cursor="hand2",
            command=self.add_current_word
        )
        self.add_vocab_btn.pack(side=tk.LEFT, padx=(10, 0))
        
        self.view_vocab_btn = tk.Button(
            search_container,
            text="📖 Xem từ vựng",
            font=("Arial", 12),
            bg="#8E44AD",
            fg="white",
            relief=tk.FLAT,
            padx=15,
            pady=10,
            cursor="hand2",
            command=self.show_vocabulary
        )
        self.view_vocab_btn.pack(side=tk.LEFT, padx=(10, 0))
        # Context input
        ctx_frame = tk.Frame(self.root, bg="white")
        ctx_frame.pack(fill=tk.X, padx=30, pady=(0, 10))
        tk.Label(ctx_frame, text="Ngữ cảnh (tùy chọn) để AI dịch chính xác hơn:", font=("Arial", 10), bg="white", fg="#555555").pack(anchor=tk.W)
        self.context_text = tk.Text(ctx_frame, height=3, wrap=tk.WORD, font=("Arial", 10))
        self.context_text.pack(fill=tk.X)
        ai_btn_frame = tk.Frame(ctx_frame, bg="white")
        ai_btn_frame.pack(fill=tk.X, pady=(6, 0))
        self.ai_translate_btn = tk.Button(ai_btn_frame, text="🤖 AI dịch theo ngữ cảnh", font=("Arial", 10, "bold"), bg="#0D47A1", fg="white", relief=tk.FLAT, padx=12, pady=6, cursor="hand2", command=self.run_ai_translate_current)
        if self.gemini_enabled:
            self.ai_translate_btn.pack(side=tk.LEFT)
        else:
            self.ai_translate_btn.configure(state=tk.DISABLED)
        
        # Main Content
        main_frame = tk.Frame(self.root, bg="white")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=(0, 20))
        
        self.result_canvas = tk.Canvas(main_frame, bg="white", highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=self.result_canvas.yview)
        self.scrollable_frame = tk.Frame(self.result_canvas, bg="white")
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.result_canvas.configure(scrollregion=self.result_canvas.bbox("all"))
        )
        
        self.result_canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.result_canvas.configure(yscrollcommand=scrollbar.set)
        
        self.result_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.result_canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        
        self.show_welcome()
        
    def _on_mousewheel(self, event):
        self.result_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
    def show_welcome(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        welcome_frame = tk.Frame(self.scrollable_frame, bg="white")
        welcome_frame.pack(pady=100)
        
        welcome_label = tk.Label(
            welcome_frame,
            text="👋 Welcome to Cambridge Dictionary",
            font=("Arial", 20, "bold"),
            bg="white",
            fg="#002147"
        )
        welcome_label.pack(pady=10)
        
        instruction_label = tk.Label(
            welcome_frame,
            text="Enter a word to search...",
            font=("Arial", 14),
            bg="white",
            fg="#666666"
        )
        instruction_label.pack()
        
    def clear_results(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
    
    def translate_text(self, text):
        """Dịch với cache - KHÔNG BAO GIỜ THẤT BẠI"""
        # Kiểm tra cache trước
        if text in self.translation_cache:
            return self.translation_cache[text]
        
        # Thử dịch với retry
        for attempt in range(2):
            try:
                translation = self.translator.translate(text)
                self.translation_cache[text] = translation
                # Lưu cache sau mỗi lần dịch thành công
                if len(self.translation_cache) % 10 == 0:
                    self.save_cache()
                return translation
            except Exception as e:
                if attempt == 0:
                    time.sleep(0.5)
                    continue
                else:
                    # Nếu fail hẳn, trả về text gốc
                    return f"[{text}]"
        
        return text
    
    def search_word(self):
        word = self.word_entry.get().strip()
        
        if not word:
            messagebox.showwarning("Warning", "Please enter a word!")
            return
        
        # Kiểm tra word cache
        if word.lower() in self.word_cache:
            print(f"⚡ Loading from cache: {word}")
            self.root.after(0, lambda: self._display_results(self.word_cache[word.lower()]))
            return
        
        self.clear_results()
        loading_label = tk.Label(
            self.scrollable_frame,
            text=f"Searching for '{word}'...",
            font=("Arial", 14),
            bg="white",
            fg="#666666"
        )
        loading_label.pack(pady=50)
        
        threading.Thread(target=self._search_word_thread, args=(word,), daemon=True).start()
    
    def _search_word_thread(self, word):
        start_time = time.time()
        word_info = self.get_word_info(word)
        elapsed = time.time() - start_time
        print(f"⏱️ Search time: {elapsed:.2f}s")
        
        if not word_info:
            self.root.after(0, lambda: self._show_error(word))
            return
        
        # Lưu vào word cache
        self.word_cache[word.lower()] = word_info
        
        # Thêm vào history (không trùng lặp)
        if word.lower() not in [w.lower() for w in self.search_history]:
            self.search_history.insert(0, word.lower())
            if len(self.search_history) > 50:  # Giữ tối đa 50 từ
                self.search_history.pop()
        
        self.root.after(0, lambda: self._display_results(word_info))
    
    def on_key_release(self, event):
        """Xử lý khi user gõ - hiển thị suggestions"""
        # Bỏ qua các phím đặc biệt
        if event.keysym in ['Return', 'Up', 'Down', 'Left', 'Right', 'Escape']:
            if event.keysym == 'Escape':
                self.hide_suggestions()
            return
        
        text = self.word_entry.get().strip().lower()
        
        if len(text) < 2:  # Chỉ suggest khi gõ từ 2 ký tự trở lên
            self.hide_suggestions()
            return
        
        # Tìm từ gợi ý
        suggestions = self.get_suggestions(text)
        
        if suggestions:
            self.show_suggestions(suggestions)
        else:
            self.hide_suggestions()
    
    def load_common_words(self):
        """Load danh sách từ phổ biến từ file common_words.txt"""
        try:
            # Xác định đường dẫn file
            if getattr(sys, 'frozen', False):
                # Chạy từ .exe (PyInstaller)
                base_path = sys._MEIPASS
            else:
                # Chạy từ .py
                base_path = os.path.dirname(os.path.abspath(__file__))
            
            file_path = os.path.join(base_path, 'common_words.txt')
            
            # Đọc file
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    words = [line.strip().lower() for line in f if line.strip()]
                print(f"✅ Loaded {len(words)} common words from file")
                return sorted(set(words))  # Remove duplicates và sort
            else:
                print(f"⚠️ File not found: {file_path}")
                return self.get_fallback_words()
        except Exception as e:
            print(f"❌ Error loading common_words.txt: {e}")
            return self.get_fallback_words()
    
    def get_fallback_words(self):
        """Fallback words nếu không load được file"""
        return sorted([
            'hello', 'world', 'computer', 'beautiful', 'wonderful',
            'amazing', 'excellent', 'important', 'different', 'interesting',
            'development', 'education', 'environment', 'government',
            'information', 'technology', 'university', 'communication'
        ])
    
    def get_suggestions(self, text):
        """Lấy danh sách từ gợi ý - OPTIMIZED với Binary Search"""
        suggestions = []
        
        # 1. Từ trong vocabulary (ưu tiên cao nhất)
        for item in self.vocabulary:
            word = item['word'].lower()
            if word.startswith(text):
                suggestions.append(word)
        
        # 2. Từ trong history
        for word in self.search_history:
            if word.startswith(text) and word not in suggestions:
                suggestions.append(word)
        
        # 3. Từ phổ biến (Binary Search cho speed!)
        if self.common_words:
            # Tìm vị trí bắt đầu với binary search
            idx = bisect.bisect_left(self.common_words, text)
            
            # Lấy tối đa 50 từ để check
            for i in range(idx, min(idx + 50, len(self.common_words))):
                word = self.common_words[i]
                if word.startswith(text):
                    if word not in suggestions:
                        suggestions.append(word)
                else:
                    break  # Không match nữa thì dừng
        
        # Giới hạn 10 suggestions, sort theo alphabet
        return sorted(set(suggestions))[:10]
    
    def show_suggestions(self, suggestions):
        """Hiển thị dropdown suggestions"""
        self.suggestion_listbox.delete(0, tk.END)
        
        for suggestion in suggestions:
            self.suggestion_listbox.insert(tk.END, suggestion)
        
        # Hiển thị listbox
        self.suggestion_listbox.pack(fill=tk.X, pady=(2, 0))
    
    def hide_suggestions(self):
        """Ẩn dropdown suggestions"""
        self.suggestion_listbox.pack_forget()
    
    def on_suggestion_select(self, event):
        """Khi chọn suggestion bằng keyboard"""
        pass
    
    def on_suggestion_click(self, event):
        """Khi click vào suggestion"""
        try:
            selection = self.suggestion_listbox.curselection()
            if selection:
                word = self.suggestion_listbox.get(selection[0])
                self.word_entry.delete(0, tk.END)
                self.word_entry.insert(0, word)
                self.hide_suggestions()
                self.search_word()
        except:
            pass
    
    def get_word_info(self, word):
        """Lấy thông tin từ Cambridge - OPTIMIZED EXTREME"""
        url = f"https://dictionary.cambridge.org/dictionary/english/{word.lower()}"
        
        try:
            response = self.session.get(url, timeout=5)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'lxml')
            
            phonetics = self._get_phonetics_fast(soup)
            definitions = self._get_definitions_fast(soup)
            
            # Dịch TỪ sang tiếng Việt (không phải definition)
            word_meaning_vi = self.translate_text(word)
            
            # Lấy audio URLs từ Cambridge
            audio_urls = self._get_audio_urls(soup)
            
            return {
                'word': word,
                'phonetic_uk': phonetics['uk'],
                'phonetic_us': phonetics['us'],
                'audio_uk': audio_urls['uk'],
                'audio_us': audio_urls['us'],
                'word_meaning_vi': word_meaning_vi,
                'definitions': definitions
            }
            
        except Exception as e:
            print(f"Error: {e}")
            return None
    
    def _translate_definitions_async(self, definitions):
        """Pre-translate các định nghĩa trong background"""
        def translate_all():
            for defn in definitions:
                # Pre-load vào cache
                self.translate_text(defn['definition'])
                for ex in defn['examples']:
                    self.translate_text(ex)
        
        # Chạy trong thread riêng, không block UI
        threading.Thread(target=translate_all, daemon=True).start()
    
    def _get_phonetics_fast(self, soup):
        """Lấy phiên âm UK và US"""
        result = {'uk': '', 'us': ''}
        
        try:
            pron_section = soup.find('div', class_='pos-header')
            if not pron_section:
                return result
            
            uk_div = pron_section.find('span', class_='uk')
            if uk_div:
                uk_ipa = uk_div.find('span', class_='ipa')
                if uk_ipa:
                    result['uk'] = uk_ipa.text.strip()
            
            us_div = pron_section.find('span', class_='us')
            if us_div:
                us_ipa = us_div.find('span', class_='ipa')
                if us_ipa:
                    result['us'] = us_ipa.text.strip()
                    
        except Exception as e:
            print(f"Error getting phonetics: {e}")
        
        return result
    
    def _get_audio_urls(self, soup):
        """Lấy URL audio từ Cambridge"""
        result = {'uk': '', 'us': ''}
        
        try:
            # Tìm audio UK
            uk_audio = soup.find('source', {'type': 'audio/mpeg', 'src': lambda x: x and 'uk' in x.lower()})
            if uk_audio and uk_audio.get('src'):
                result['uk'] = 'https://dictionary.cambridge.org' + uk_audio['src']
            
            # Tìm audio US
            us_audio = soup.find('source', {'type': 'audio/mpeg', 'src': lambda x: x and 'us' in x.lower()})
            if us_audio and us_audio.get('src'):
                result['us'] = 'https://dictionary.cambridge.org' + us_audio['src']
                
        except Exception as e:
            print(f"Error getting audio: {e}")
        
        return result
    
    def _get_definitions_fast(self, soup):
        """Lấy nghĩa - OPTIMIZED"""
        definitions = []
        
        try:
            entry_body = soup.find('div', class_='entry-body')
            if not entry_body:
                return [{'pos': '', 'definition': 'No definition found', 'examples': []}]
            
            pos_bodies = entry_body.find_all('div', class_='pos-body', limit=3)
            
            for pos_body in pos_bodies:
                pos_header = pos_body.find_previous_sibling('div', class_='pos-header')
                pos = ''
                if pos_header:
                    pos_elem = pos_header.find('span', class_='pos')
                    if pos_elem:
                        pos = pos_elem.text.strip()
                
                def_blocks = pos_body.find_all('div', class_='def-block', limit=2)
                
                for block in def_blocks:
                    def_elem = block.find('div', class_='def')
                    if def_elem:
                        definition = def_elem.text.strip()
                        
                        examples = []
                        example_elems = block.find_all('span', class_='eg', limit=2)
                        for ex in example_elems:
                            examples.append(ex.text.strip())
                        
                        definitions.append({
                            'pos': pos,
                            'definition': definition,
                            'examples': examples
                        })
                        pos = ''
            
        except Exception as e:
            print(f"Error: {e}")
        
        return definitions if definitions else [{'pos': '', 'definition': 'No definition found', 'examples': []}]
    
    def _show_error(self, word):
        self.clear_results()
        error_frame = tk.Frame(self.scrollable_frame, bg="white")
        error_frame.pack(pady=50)
        
        error_label = tk.Label(
            error_frame,
            text=f"❌ Word '{word}' not found",
            font=("Arial", 16, "bold"),
            bg="white",
            fg="#E74C3C"
        )
        error_label.pack(pady=10)
        
        hint_label = tk.Label(
            error_frame,
            text="Please check the spelling and try again.",
            font=("Arial", 12),
            bg="white",
            fg="#666666"
        )
        hint_label.pack()
    
    def _display_results(self, word_info):
        """Hiển thị kết quả - HIỂN THỊ NGAY, DỊCH SAU"""
        self.current_word_info = word_info
        self.clear_results()
        
        content_frame = tk.Frame(self.scrollable_frame, bg="white")
        content_frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=20)
        
        # Word Title với nghĩa tiếng Việt
        title_frame = tk.Frame(content_frame, bg="white")
        title_frame.pack(anchor=tk.W, pady=(0, 15))
        
        word_title = tk.Label(title_frame, text=word_info['word'].upper(), font=("Georgia", 32, "bold"), bg="white", fg="#002147")
        word_title.pack(side=tk.LEFT)
        # Placeholder AI VI label
        self.ai_vi_label = tk.Label(title_frame, text=(f"  •  {word_info['word_meaning_vi']}" if word_info.get('word_meaning_vi') else ""), font=("Arial", 20), bg="white", fg="#0D47A1")
        self.ai_vi_label.pack(side=tk.LEFT, padx=(10, 0))
        
        # Pronunciation
        pron_frame = tk.Frame(content_frame, bg="white")
        pron_frame.pack(anchor=tk.W, pady=(0, 20))
        
        if word_info['phonetic_uk']:
            uk_frame = tk.Frame(pron_frame, bg="white")
            uk_frame.pack(side=tk.LEFT, padx=(0, 30))
            
            tk.Label(uk_frame, text="UK", font=("Arial", 10, "bold"), bg="white", fg="#666666").pack(side=tk.LEFT, padx=(0, 8))
            
            tk.Button(
                uk_frame,
                text="🔊",
                font=("Arial", 16),
                bg="white",
                fg="#00A7E1",
                relief=tk.FLAT,
                cursor="hand2",
                borderwidth=0,
                command=lambda: self.play_audio(word_info.get('audio_uk', ''), word_info['word'], 'uk')
            ).pack(side=tk.LEFT)
            
            tk.Label(
                uk_frame,
                text=f"/{word_info['phonetic_uk']}/",
                font=("Arial", 15),
                bg="white",
                fg="#E74C3C"
            ).pack(side=tk.LEFT, padx=(8, 0))
        
        if word_info['phonetic_us']:
            us_frame = tk.Frame(pron_frame, bg="white")
            us_frame.pack(side=tk.LEFT)
            
            tk.Label(us_frame, text="US", font=("Arial", 10, "bold"), bg="white", fg="#666666").pack(side=tk.LEFT, padx=(0, 8))
            
            tk.Button(
                us_frame,
                text="🔊",
                font=("Arial", 16),
                bg="white",
                fg="#00A7E1",
                relief=tk.FLAT,
                cursor="hand2",
                borderwidth=0,
                command=lambda: self.play_audio(word_info.get('audio_us', ''), word_info['word'], 'us')
            ).pack(side=tk.LEFT)
            
            tk.Label(
                us_frame,
                text=f"/{word_info['phonetic_us']}/",
                font=("Arial", 15),
                bg="white",
                fg="#E74C3C"
            ).pack(side=tk.LEFT, padx=(8, 0))
        
        # Separator
        tk.Frame(content_frame, height=2, bg="#E0E0E0").pack(fill=tk.X, pady=15)
        
        # Definitions
        for idx, definition in enumerate(word_info['definitions'], 1):
            self._display_definition(content_frame, idx, definition)
        # Auto AI translate if available
        if self.gemini_enabled:
            self.root.after(120, self.run_ai_translate_current)
    
    def _display_definition(self, parent, idx, definition):
        """Hiển thị định nghĩa với nghĩa tiếng Việt"""
        def_container = tk.Frame(parent, bg="white")
        def_container.pack(fill=tk.X, pady=15, anchor=tk.W)
        
        # Part of speech
        if definition['pos']:
            tk.Label(
                def_container,
                text=definition['pos'],
                font=("Arial", 13, "bold"),
                bg="white",
                fg="#0D47A1"  # Màu xanh Cambridge
            ).pack(anchor=tk.W, pady=(0, 10))
        
        # Definition row
        def_row = tk.Frame(def_container, bg="white")
        def_row.pack(fill=tk.X, pady=(0, 10))
        
        # Left: English
        left_frame = tk.Frame(def_row, bg="white")
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 20))
        
        en_def_frame = tk.Frame(left_frame, bg="white")
        en_def_frame.pack(fill=tk.X)
        
        tk.Label(
            en_def_frame,
            text=f"{idx}.",
            font=("Arial", 12, "bold"),
            bg="white",
            fg="#002147"
        ).pack(side=tk.LEFT, anchor=tk.N, padx=(0, 8))
        
        tk.Label(
            en_def_frame,
            text=definition['definition'],
            font=("Arial", 12),
            bg="white",
            fg="#002147",
            wraplength=350,
            justify=tk.LEFT
        ).pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Right: Vietnamese - PLACEHOLDER trước, cập nhật sau
        right_frame = tk.Frame(def_row, bg="#F0F4FF", relief=tk.SOLID, borderwidth=1)
        right_frame.pack(side=tk.LEFT, fill=tk.BOTH)
        
        vi_label = tk.Label(
            right_frame,
            text="🇻🇳  Đang dịch...",
            font=("Arial", 11),
            bg="#F0F4FF",
            fg="#1565C0",  # Xanh Cambridge đậm hơn
            wraplength=280,
            justify=tk.LEFT,
            padx=12,
            pady=8
        )
        vi_label.pack()
        
        # Dịch và cập nhật trong background
        def update_translation():
            vi_def = self.translate_text(definition['definition'])
            vi_label.config(text=f"🇻🇳  {vi_def}")
        
        threading.Thread(target=update_translation, daemon=True).start()
        
        # Examples
        if definition['examples']:
            for ex in definition['examples']:
                ex_frame = tk.Frame(left_frame, bg="white")
                ex_frame.pack(fill=tk.X, pady=(5, 0), padx=(25, 0))
                
                tk.Label(
                    ex_frame,
                    text=f"• {ex}",
                    font=("Arial", 11, "italic"),
                    bg="white",
                    fg="#666666",
                    wraplength=320,
                    justify=tk.LEFT
                ).pack(anchor=tk.W)
                
                # Vietnamese example - placeholder
                vi_ex_label = tk.Label(
                    ex_frame,
                    text="  ...",
                    font=("Arial", 10),
                    bg="white",
                    fg="#1976D2",  # Xanh Cambridge
                    wraplength=320,
                    justify=tk.LEFT
                )
                vi_ex_label.pack(anchor=tk.W, pady=(2, 0))
                
                # Update trong background
                def update_ex_translation(ex_text=ex, label=vi_ex_label):
                    vi_ex = self.translate_text(ex_text)
                    label.config(text=f"  {vi_ex}")
                
                threading.Thread(target=update_ex_translation, daemon=True).start()

    def run_ai_translate_current(self):
        if not self.gemini_enabled or not hasattr(self, 'current_word_info'):
            return
        word = self.current_word_info['word']
        context = self.context_text.get('1.0', tk.END).strip()
        defs_en = [d.get('definition', '') for d in self.current_word_info.get('definitions', [])][:3]

        def worker():
            vi, example_en = self.ai_translate_with_context(word, defs_en, context)
            if vi:
                self.ai_vi_label.config(text=f"  •  {vi}")
            self.current_ai_vi = vi
            self.current_ai_example_en = example_en
        threading.Thread(target=worker, daemon=True).start()

    def ai_translate_with_context(self, word: str, defs_en: list, context: str):
        try:
            prompt = (
                "You are a bilingual English-Vietnamese lexicographer. Given an English headword, its brief glosses, "
                "and an optional user-provided context, produce: (1) a concise Vietnamese meaning of the headword "
                "that best fits the context (≤6 words), and (2) one short English example sentence that naturally uses the word. "
                "Output as JSON: {\"vi_meaning\": string, \"example_en\": string}.\n\n"
                f"Headword: {word}\nGlosses: {defs_en}\nContext: {context or '(none)'}\n"
            )
            resp = self.gemini_model.generate_content(prompt)
            text = (getattr(resp, 'text', None) or '').strip()
            vi, ex = None, None
            import json as _json, re as _re
            m = _re.search(r"\{[\s\S]*\}", text)
            if m:
                try:
                    obj = _json.loads(m.group(0))
                    vi = obj.get('vi_meaning')
                    ex = obj.get('example_en')
                except Exception:
                    pass
            if not vi and text:
                vi = text.split('\n')[0][:60]
            if not ex:
                ex = f"{word.capitalize()} is used naturally in this context."
            return (vi.strip() if vi else None), (ex.strip() if ex else None)
        except Exception:
            return None, None
    
    def play_audio(self, audio_url, word, region='uk'):
        """Phát audio từ Cambridge hoặc fallback sang TTS"""
        if audio_url:
            threading.Thread(target=self._play_cambridge_audio, args=(audio_url,), daemon=True).start()
        else:
            # Fallback: dùng TTS
            if self.tts_engine:
                threading.Thread(target=self._pronounce_thread, args=(word,), daemon=True).start()
    
    def _play_cambridge_audio(self, audio_url):
        """Phát audio từ Cambridge"""
        try:
            import pygame
            import io
            
            # Download audio
            response = self.session.get(audio_url, timeout=5)
            audio_data = io.BytesIO(response.content)
            
            # Play audio
            pygame.mixer.init()
            pygame.mixer.music.load(audio_data)
            pygame.mixer.music.play()
            
            # Đợi phát xong
            while pygame.mixer.music.get_busy():
                time.sleep(0.1)
                
        except Exception as e:
            print(f"Error playing audio: {e}")
            # Fallback sang TTS nếu lỗi
    
    def _pronounce_thread(self, word):
        """Fallback TTS"""
        try:
            if self.tts_engine:
                self.tts_engine.say(word)
                self.tts_engine.runAndWait()
        except Exception as e:
            print(f"Error: {e}")
    
    def add_current_word(self):
        if hasattr(self, 'current_word_info'):
            self.add_to_vocabulary(
                self.current_word_info['word'],
                self.current_word_info['phonetic_uk'],
                self.current_word_info['phonetic_us'],
                self.current_word_info['definitions'],
                getattr(self, 'current_ai_vi', None),
                getattr(self, 'current_ai_example_en', None)
            )
        else:
            messagebox.showwarning("Cảnh báo", "Vui lòng tra từ trước!")
    
    def export_to_excel(self, clear_after_export=False):
        """Export từ vựng ra Excel cho Quizlet"""
        if not self.vocabulary:
            messagebox.showwarning("Cảnh báo", "Chưa có từ vựng nào để export!")
            return
        
        try:
            from openpyxl import Workbook
            from openpyxl.styles import Font, Alignment, PatternFill
            from tkinter import filedialog
            
            # Hỏi có xóa từ sau khi export không
            if not clear_after_export:
                clear_after_export = messagebox.askyesno(
                    "Xóa từ vựng?",
                    "Bạn có muốn XÓA TẤT CẢ từ vựng sau khi export không?\n\n"
                    "✅ Yes: Export rồi xóa hết\n"
                    "❌ No: Giữ nguyên từ vựng"
                )
            
            # Chọn nơi lưu file
            file_path = filedialog.asksaveasfilename(
                defaultextension=".xlsx",
                filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")],
                initialfile="my_vocabulary_quizlet.xlsx"
            )
            
            if not file_path:
                return
            
            # Tạo workbook
            wb = Workbook()
            ws = wb.active
            ws.title = "Vocabulary"
            
            # Header
            ws['A1'] = "Từ vựng / Cụm từ (Exam dưới)"
            ws['B1'] = "Nghĩa"
            
            # Style header
            header_font = Font(bold=True, size=12)
            header_fill = PatternFill(start_color="4CAF50", end_color="4CAF50", fill_type="solid")
            
            ws['A1'].font = header_font
            ws['B1'].font = header_font
            ws['A1'].fill = header_fill
            ws['B1'].fill = header_fill
            
            # Điều chỉnh độ rộng cột
            ws.column_dimensions['A'].width = 50
            ws.column_dimensions['B'].width = 40
            
            # Thêm dữ liệu
            row = 2
            for item in self.vocabulary:
                word = item['word']
                phonetic_uk = item.get('phonetic_uk', '')
                phonetic_us = item.get('phonetic_us', '')
                definitions = item.get('definitions', [])
                
                # Lấy ví dụ: ưu tiên AI example nếu có
                example = item.get('ai_example_en') or ""
                if not example and definitions and definitions[0].get('examples'):
                    example = definitions[0]['examples'][0]
                
                # Cột A: Từ + IPA + Example
                cell_a_text = f"{word}"
                if phonetic_uk or phonetic_us:
                    ipa = phonetic_uk if phonetic_uk else phonetic_us
                    cell_a_text += f" /{ipa}/"
                if example:
                    cell_a_text += f"\nExam: {example}"
                
                # Cột B: Nghĩa tiếng Việt - ưu tiên ai_vi nếu có
                meaning_vi = item.get('ai_vi') or self.translate_text(word)
                
                ws[f'A{row}'] = cell_a_text
                ws[f'B{row}'] = meaning_vi
                
                # Style cells
                ws[f'A{row}'].alignment = Alignment(wrap_text=True, vertical='top')
                ws[f'B{row}'].alignment = Alignment(wrap_text=True, vertical='top')
                
                row += 1
            
            # Lưu file
            wb.save(file_path)
            
            # Thông báo thành công
            word_count = len(self.vocabulary)
            messagebox.showinfo(
                "Thành công", 
                f"✅ Đã export {word_count} từ vào file:\n{file_path}\n\n"
                "Bạn có thể import file này vào Quizlet!"
            )
            
            # Xóa từ vựng nếu user chọn
            if clear_after_export:
                self.vocabulary = []
                self.save_vocabulary()
                messagebox.showinfo(
                    "Đã xóa",
                    f"🗑️ Đã xóa {word_count} từ vựng cũ!\n\n"
                    "Bạn có thể bắt đầu lưu từ mới."
                )
            
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể export: {str(e)}")
    
    def show_vocabulary(self):
        vocab_window = tk.Toplevel(self.root)
        vocab_window.title("Danh sách từ vựng")
        vocab_window.geometry("700x500")
        
        tk.Label(
            vocab_window,
            text=f"📚 Từ vựng của tôi ({len(self.vocabulary)} từ)",
            font=("Arial", 16, "bold"),
            bg="#8E44AD",
            fg="white",
            pady=15
        ).pack(fill=tk.X)
        
        list_frame = tk.Frame(vocab_window)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        vocab_listbox = tk.Listbox(list_frame, font=("Arial", 12), yscrollcommand=scrollbar.set)
        vocab_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=vocab_listbox.yview)
        
        for item in self.vocabulary:
            vocab_listbox.insert(tk.END, f"{item['word']}  -  {item['added_date']}")
        
        btn_frame = tk.Frame(vocab_window)
        btn_frame.pack(fill=tk.X, padx=20, pady=(0, 20))
        
        def view_word():
            selection = vocab_listbox.curselection()
            if selection:
                word = self.vocabulary[selection[0]]['word']
                self.word_entry.delete(0, tk.END)
                self.word_entry.insert(0, word)
                vocab_window.destroy()
                self.search_word()
        
        def delete_word():
            selection = vocab_listbox.curselection()
            if selection:
                idx = selection[0]
                word = self.vocabulary[idx]['word']
                if messagebox.askyesno("Xác nhận", f"Xóa '{word}'?"):
                    del self.vocabulary[idx]
                    self.save_vocabulary()
                    vocab_listbox.delete(idx)
                    tk.Label(
                        vocab_window,
                        text=f"📚 Từ vựng của tôi ({len(self.vocabulary)} từ)",
                        font=("Arial", 16, "bold"),
                        bg="#8E44AD",
                        fg="white",
                        pady=15
                    ).pack(fill=tk.X)
        
        def delete_all():
            if not self.vocabulary:
                messagebox.showinfo("Thông báo", "Danh sách đã trống!")
                return
            
            count = len(self.vocabulary)
            if messagebox.askyesno(
                "⚠️ Xác nhận xóa TẤT CẢ", 
                f"Bạn chắc chắn muốn xóa TẤT CẢ {count} từ?\n\n"
                "Hành động này KHÔNG THỂ hoàn tác!"
            ):
                self.vocabulary = []
                self.save_vocabulary()
                vocab_listbox.delete(0, tk.END)
                messagebox.showinfo("Đã xóa", f"🗑️ Đã xóa {count} từ!")
                vocab_window.destroy()
        
        tk.Button(
            btn_frame, 
            text="Xem từ", 
            font=("Arial", 11), 
            bg="#3498DB", 
            fg="white", 
            padx=20, 
            pady=8, 
            command=view_word
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        tk.Button(
            btn_frame, 
            text="Xóa 1 từ", 
            font=("Arial", 11), 
            bg="#E74C3C", 
            fg="white", 
            padx=15, 
            pady=8, 
            command=delete_word
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        tk.Button(
            btn_frame, 
            text="🗑️ Xóa TẤT CẢ", 
            font=("Arial", 11, "bold"), 
            bg="#C0392B", 
            fg="white", 
            padx=15, 
            pady=8, 
            command=delete_all
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        tk.Button(
            btn_frame, 
            text="📥 Export Excel", 
            font=("Arial", 11, "bold"), 
            bg="#27AE60", 
            fg="white", 
            padx=20, 
            pady=8, 
            command=self.export_to_excel
        ).pack(side=tk.LEFT)


def main():
    root = tk.Tk()
    app = CambridgeDictionaryApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
