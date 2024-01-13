import tkinter as tk
from tkinter import filedialog, messagebox, colorchooser, scrolledtext, ttk
from PIL import Image, ImageDraw, ImageFont
import pytesseract
from googletrans import Translator
from langdetect import detect
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import os
from gtts import gTTS
import tempfile
from spellchecker import SpellChecker
from tkinter.ttk import Progressbar
import time
BG = "#F9F1E4"  # You can use any valid color code here



window = tk.Tk()
window.title("Text Processing App")
window.configure(bg="#DDECFF")

# Customize window size
window.geometry("800x600")

# Create a custom font
custom_font = ("Helvetica", 14)
custom_font = ("Helvetica", 14)
ll=tk.Label(window, bg=BG, font=("Times New Roman", 18, 'bold'))
tk.Label(ll,text="S",font=('',20,'bold'),fg="red").pack(side='left')
tk.Label(ll,text="T",fg="#5D6D7E",font=('',15,'bold')).pack(side='left')
tk.Label(ll,text="U",fg="#5D6D7E",font=('',15,'bold')).pack(side='left')
tk.Label(ll,text="D",fg="#5D6D7E",font=('',15,'bold')).pack(side='left')
tk.Label(ll,text="Y",fg="#5D6D7E",font=('',15,'bold')).pack(side='left')

tk.Label(ll,text=" H",fg="red",font=('',20,'bold')).pack(side='left')
tk.Label(ll,text="E",fg="#5D6D7E",font=('',15,'bold')).pack(side='left')
tk.Label(ll,text="L",fg="#5D6D7E",font=('',15,'bold')).pack(side='left')
tk.Label(ll,text="P",fg="#5D6D7E",font=('',15,'bold')).pack(side='left')
tk.Label(ll,text="E",fg="#5D6D7E",font=('',15,'bold')).pack(side='left')
tk.Label(ll,text="R !",fg="#5D6D7E",font=('',15,'bold')).pack(side='left')
tk.Label(ll,text="                 @ANONYMOUS HELPER !",fg="black",font=('',15,'bold')).pack(side='left')
ll.pack()

# Create a scrolled text box for larger text
text_box = scrolledtext.ScrolledText(window, wrap=tk.WORD, font=custom_font)
text_box.pack(pady=1, fill="both")

# Initialize spell checker
spell = SpellChecker()

# Function to convert text to an image
def text_to_image():
    try:
        text = text_box.get("1.0", tk.END)

        # Create a new image with a white background
        image = Image.new("RGB", (800, 600), "white")
        draw = ImageDraw.Draw(image)

        # Use a font (you can change the font and size)
        font = ImageFont.load_default()
        font_size = 20
        font = ImageFont.truetype("arial.ttf", font_size)

        # Set initial position for drawing text
        x, y = 10, 10

        # Split the text into lines and draw each line on the image
        for line in text.split("\n"):
            draw.text((x, y), line, fill="black", font=font)
            y += font_size + 5  # Adjust spacing between lines

        # Ask the user for the directory to save the image
        save_directory = filedialog.askdirectory()
        if save_directory:
            save_path = f"{save_directory}/text_image.png"
            image.save(save_path)
            messagebox.showinfo("Info", f"Text converted to image and saved as '{save_path}'.")
    except Exception as e:
        messagebox.showwarning('', f'{type(e).__name__}')

# Function to open an image and convert it to text
def image_to_text():
    try:
        pytesseract.pytesseract.tesseract_cmd = r"D:\PROJECTS PYTHON\NMC_COLLAGE_PROJECTS\PROJECT_8_IT\New folder\tesseract.exe"
        file_path = filedialog.askopenfilename()
        if file_path:
            image = Image.open(file_path)
            text = pytesseract.image_to_string(image)
            text_box.delete("1.0", tk.END)
            text_box.insert(tk.END, text)
    except Exception as e:
        messagebox.showwarning('', f'{type(e).__name__}')

# Function to translate text to the selected language
def translate_text():
    try:
        text = text_box.get("1.0", tk.END)
        detected_language = detect(text)
        target_language = selected_language.get()  # Get the selected language from the combo box

        if detected_language != target_language:
            translator = Translator()
            translated_text = translator.translate(text, src=detected_language, dest=target_language)
            text_box.delete("1.0", tk.END)
            text_box.insert(tk.END, translated_text.text)
        else:
            messagebox.showinfo("Info", "Text is already in the selected language.")
    except Exception as e:
        messagebox.showwarning('', f'{type(e).__name__}')

# Function to correct English words
import language_tool_python

# Initialize the LanguageTool API
tool = language_tool_python.LanguageTool('en-US')

def correct_english():
    try:
        text = text_box.get("1.0", tk.END)

        # Correct the text using the LanguageTool API
        corrected_text = tool.correct(text)

        # Clear the text box
        text_box.delete("1.0", tk.END)
        text_box.insert(tk.END, corrected_text)
    except Exception as e:
        messagebox.showwarning('', f'{type(e).__name__}')

# Function to save text
def save_text():
    text = text_box.get("1.0", tk.END)
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
    if file_path:
        with open(file_path, "w") as file:
            file.write(text)
        messagebox.showinfo("Info", "Text saved successfully!")

# Function to clear the text box
def clear_text():
    text_box.delete("1.0", tk.END)

# Function to count words
def count_words():
    text = text_box.get("1.0", tk.END)
    words = text.split()
    word_count = len(words)
    messagebox.showinfo("Word Count", f"Total words: {word_count}")

# Function to toggle dark mode
def toggle_dark_mode():
    bg_color = text_box.cget("bg")
    if bg_color == "white":
        text_box.configure(bg="black", fg="white")
    else:
        text_box.configure(bg="white", fg="black")

# Function to speak the text using text-to-speech
def speak_text():
    try:
        text = text_box.get("1.0", tk.END)

        # Detect the language of the text
        detected_language = detect(text)

        # Generate the text-to-speech audio file with the detected language
        tts = gTTS(text=text, lang=detected_language)
        audio_file = tempfile.NamedTemporaryFile(suffix=".mp3", delete=False)
        tts.save(audio_file.name)

        # Close the audio file
        audio_file.close()

        # Play the audio file (you need a media player installed)
        os.system(f"start {audio_file.name}")
    except Exception as e:
        messagebox.showwarning('', f'{type(e).__name__}')

# Function to change text color
def change_text_color():
    color = colorchooser.askcolor()[1]
    text_box.configure(fg=color)

# Function to save text to a PDF file
def save_to_pdf():
    try:
        text = text_box.get("1.0", tk.END)

        # Split the text into lines
        lines = text.split('\n')

        file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")])
        if file_path:
            c = canvas.Canvas(file_path, pagesize=letter, pageCompression=True)
            c.drawString(100, 750, "Text Processing App - PDF Export")
            c.drawString(100, 730, "-" * 40)

            # Write each line of text on the first page
            y_position = 700  # Initial Y position
            line_height = 12  # Adjust as needed for line spacing
            for line in lines:
                if y_position < 50:  # Check if we need a new page
                    c.showPage()  # Start a new page
                    c.drawString(100, 750, "Text Processing App - PDF Export")
                    c.drawString(100, 730, "-" * 40)
                    y_position = 700  # Reset Y position for the new page
                c.drawString(100, y_position, line)
                y_position -= line_height

            c.save()
            messagebox.showinfo("Info", "Text saved as PDF successfully!")
    except Exception as e:
        messagebox.showerror('', f'{type(e).__name__}')

def calculate_type_speed():
    global speed_checker_active
    if not speed_checker_active:
        # Start the speed checker
        speed_checker_active = True
        typing_start_time = time.time()
        typed_word_count = 0
        while speed_checker_active:
            text = text_box.get("1.0", tk.END)
            words = text.split()
            typed_word_count = len(words)
            elapsed_time = time.time() - typing_start_time
            update_speed_meter(typed_word_count, elapsed_time)
            if elapsed_time > 0:
                typing_speed = int(typed_word_count / (elapsed_time / 60))  # Words per minute
                typing_speed_label.config(text=f"Typing Speed: {typing_speed} wpm")
            window.update()  # Update the GUI
            # Check if a paragraph is complete (you can adjust the threshold)
            if '\n\n' in text:
                speed_checker_active = False
    else:
        # Stop the speed checker
        speed_checker_active = False
        typing_speed_label.config(text="Speed Checker Stopped")
        typing_speed_progress["value"] = 0  # Reset the progress bar

# Function to update the speed meter
def update_speed_meter(typed_word_count, elapsed_time):
    if elapsed_time > 0:
        typing_speed = int(typed_word_count / (elapsed_time / 60))  # Words per minute
        typing_speed_progress["value"] = typing_speed

supported_languages = [
    "en", "es", "fr", "de", "it", "ja", "ko", "nl", "pl", "pt",
    "ru", "zh-CN", "ar", "tr", "vi", "el", "he", "th", "hi", "sv", "ta"  # Added Tamil
]

# Create a StringVar to store the selected language
selected_language = tk.StringVar()

# Create a function to handle language selection
def on_language_select(event):
    selected_language.set(language_combobox.get())

# Create the language combo box
# Create a label for the language combo box
language_label = tk.Label(window, text="Select Language:", font=custom_font, bg=BG)
language_label.pack(side="top")
language_combobox = ttk.Combobox(window, values=supported_languages)
language_combobox.set("en")  # Set the default language to English
language_combobox.pack(pady=5,side="top")
language_combobox.bind("<<ComboboxSelected>>", on_language_select)

# Create two frames for button organization
button_line1 = tk.Frame(window, bg=BG)
button_line1.pack()
button_line2 = tk.Frame(window, bg=BG)
button_line2.pack()

# Create buttons with custom styling
image_button = tk.Button(button_line1, text="Image to Text",bg=BG, command=image_to_text, font=custom_font, height=3, width=20)
translate_button = tk.Button(button_line1, text="Translate Text",bg=BG, command=translate_text, font=custom_font, height=3, width=20)
correct_button = tk.Button(button_line1, text="Correct English", bg=BG, command=correct_english, font=custom_font, height=3, width=20)
save_button = tk.Button(button_line1, text="Save Text", bg=BG, command=save_text, font=custom_font, height=3, width=20)
clear_button = tk.Button(button_line1, text="Clear Text", bg=BG, command=clear_text, font=custom_font, height=3, width=20)

# Organize the first five buttons in one line
image_button.grid(row=0, column=0)
translate_button.grid(row=0, column=1)
correct_button.grid(row=0, column=2)
save_button.grid(row=0, column=3)
clear_button.grid(row=0, column=4)

word_count_button = tk.Button(button_line1, text="Word Count", bg=BG, command=count_words, font=custom_font, height=3, width=20)
dark_mode_button = tk.Button(button_line2, text="Toggle Dark Mode", bg=BG, command=toggle_dark_mode, font=custom_font, height=3, width=20)
speak_button = tk.Button(button_line2, text="Speak Text", bg=BG, command=speak_text, font=custom_font, height=3, width=20)
color_button = tk.Button(button_line2, text="Change Text Color", bg=BG, command=change_text_color, font=custom_font, height=3, width=20)
save_pdf_button = tk.Button(button_line2, text="Save to PDF", bg=BG, command=save_to_pdf, font=custom_font, height=3, width=20)
text_to_image_button = tk.Button(button_line2, text="Text to Image",bg=BG, command=text_to_image, font=custom_font, height=3, width=20)
text_to_image_button.grid(row=0, column=6)
# Organize the remaining buttons in the second line
word_count_button.grid(row=0, column=5)
dark_mode_button.grid(row=0, column=1)
speak_button.grid(row=0, column=2)
color_button.grid(row=0, column=3)
save_pdf_button.grid(row=0, column=4)

# Create a progress bar to display typing speed
typing_speed_progress = Progressbar(window, orient="horizontal", length=200, mode="determinate")
typing_speed_progress.pack()

# Create a label for typing speed
typing_speed_label = tk.Label(window, text="", font=custom_font)
typing_speed_label.pack(side="top")

# Create a button to start/stop the speed checker
speed_checker_active = False
speed_checker_button = tk.Button(button_line2, text="Speed Checker",bg=BG, command=calculate_type_speed, font=custom_font, height=3, width=20)
speed_checker_button.grid(row=0, column=5)

# Start the Tkinter main loop
window.mainloop()
