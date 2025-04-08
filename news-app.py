from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import requests
from PIL import Image, ImageTk
import webbrowser
import threading
import io
import os

apiKey = '32afaec36d0370bb9774687c2450ba35'

class NewsApp:
    def __init__(self, root):
        self.root = root
        self.root.geometry('1100x700')
        self.root.title("News Application")
        self.root.config(bg='#e6f0ff')
        self.newsCategoryButton = []
        self.active_button = None

        self.newsCategory = [
            ("world", "🌍"),
            ("nation", "🏛️"),
            ("business", "💼"),
            ("sports", "🏅"),
            ("technology", "💻"),
            ("entertainment", "🎬"),
            ("health", "🩺")
        ]

        title = Label(self.root, text="📰 Daily News Digest", font=("Segoe UI", 30, "bold"), pady=10, bg='#005792', fg='white')
        title.pack(fill=X)

        F1 = LabelFrame(self.root, text="Categories", font=("Segoe UI", 18, "bold"), bg='#003366', fg='white')
        F1.place(x=20, y=80, width=230, height=560)

        for topic, icon in self.newsCategory:
            btn_text = f"{icon} {topic.title()}"
            b = Button(F1, text=btn_text, width=20, bd=2, font=("Segoe UI", 12), bg='#d1ecf1', fg='black',
                       activebackground="#0c5460", activeforeground="white")
            b.grid(padx=10, pady=5)
            b.bind('<Button-1>', lambda e, btn=b: threading.Thread(target=self.Newsarea, args=(e,), daemon=True).start())
            b.bind('<Enter>', lambda e, btn=b: btn.config(bg='#87cefa'))
            b.bind('<Leave>', lambda e, btn=b: self.reset_button_color(btn))
            self.newsCategoryButton.append(b)

        F2 = Frame(self.root, bd=2, bg='white')
        F2.place(x=270, y=80, relwidth=0.7, relheight=0.82)

        self.canvas = Canvas(F2, bg='white')
        self.scroll_y = Scrollbar(F2, orient=VERTICAL, command=self.canvas.yview)
        self.scrollable_frame = Frame(self.canvas, bg='white')

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scroll_y.set)

        self.canvas.pack(side=LEFT, fill=BOTH, expand=True)
        self.scroll_y.pack(side=RIGHT, fill=Y)

        self.display_welcome()

    def reset_button_color(self, button):
        if button != self.active_button:
            button.config(bg='#add8e6', fg='black')

    def display_welcome(self):
        Label(self.scrollable_frame, text="Select a category to load news.", font=("Segoe UI", 18), bg='white', fg='#003f5c').pack(pady=20)

    def open_link(self, url):
        webbrowser.open_new(url)

    def Newsarea(self, event):
        topic_text = event.widget.cget('text')
        topic = topic_text.split(' ', 1)[1].lower()
        url = f'https://gnews.io/api/v4/top-headlines?topic={topic}&lang=en&apikey={apiKey}'

        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        for btn in self.newsCategoryButton:
            btn.config(bg='#add8e6', fg='black')
        event.widget.config(bg='#005792', fg='white')
        self.active_button = event.widget

        Label(self.scrollable_frame, text=f"Top Headlines - {topic.title()}", font=("Segoe UI", 22, "bold"), bg='white', fg='#005792').pack(pady=10)

        try:
            response = requests.get(url)
            data = response.json()

            if 'articles' in data and len(data['articles']) > 0:
                for article in data['articles']:
                    frame = Frame(self.scrollable_frame, bg='#e6f0ff', bd=1, relief=SOLID, padx=10, pady=10)
                    frame.pack(fill=X, padx=10, pady=10)

                    if article.get('image'):
                        try:
                            img_data = requests.get(article['image']).content
                            img = Image.open(io.BytesIO(img_data))
                            img = img.resize((120, 80))
                            photo = ImageTk.PhotoImage(img)
                            img_label = Label(frame, image=photo, bg='#e6f0ff')
                            img_label.image = photo
                            img_label.pack(side=LEFT, padx=10)
                        except:
                            pass

                    text_frame = Frame(frame, bg='#e6f0ff')
                    text_frame.pack(fill=BOTH, expand=True)

                    Label(text_frame, text=article['title'], font=("Segoe UI", 14, "bold"), wraplength=700, bg='#e6f0ff', justify=LEFT).pack(anchor='w')
                    Label(text_frame, text=article['description'], font=("Segoe UI", 11), wraplength=700, bg='#e6f0ff', justify=LEFT, fg='#333').pack(anchor='w', pady=2)

                    link = Label(text_frame, text="Read more...", font=("Segoe UI", 10, "underline"), fg="blue", bg='#e6f0ff', cursor="hand2")
                    link.pack(anchor='w')
                    link.bind("<Button-1>", lambda e, url=article['url']: self.open_link(url))
            else:
                Label(self.scrollable_frame, text="No news articles available.", font=("Segoe UI", 14), bg='white').pack(pady=20)
        except Exception as e:
            messagebox.showerror("Error", f"Could not fetch news.\nDetails: {str(e)}")

# Run the app
root = Tk()
obj = NewsApp(root)
root.mainloop()


