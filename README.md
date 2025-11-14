# **PyTranslator**

PyTranslator is a small desktop application I built using **Python** and **Tkinter** to translate text between multiple languages. The goal was to create a lightweight and simple translator that works locally with a clean user interface and quick responses.

---

## **About the Project**

I wanted a desktop translator that didn’t require opening a browser and could translate text instantly. PyTranslator lets you:

* Choose a source and target language
* Enter text and translate it with one click
* Clear the input/output quickly
* Copy translated text
* Use a simple and minimal Tkinter interface

The app uses a translation library/API in the backend to fetch accurate results.

---

## **Tech Used**

* **Python 3**
* **Tkinter** (for the GUI)
* **googletrans / deep-translator** (based on what the user installs)
* **Requests** (API calls)

---

## **Features**

* Easy-to-use desktop UI
* Supports multiple languages
* Instant translation
* Copy and clear buttons
* Error handling for empty or invalid inputs

---

## **Project Structure**

```
PyTranslator/
│── main.py          # Main Tkinter app
│── translator.py    # Handles translation logic
│── assets/          # Icons or images (optional)
│── requirements.txt
│── README.md
```

---

## **How to Run**

1. Install the required libraries:

   ```bash
   pip install -r requirements.txt
   ```

2. Start the app:

   ```bash
   python main.py
   ```

---

## **Why I Built This**

This project helped me get more comfortable with:

* Building GUIs with Tkinter
* Working with APIs
* Structuring small Python applications
* Handling user input and improving usability

It’s a fun project and a handy tool to keep on your desktop.

---

## **Future Ideas**

* Add text-to-speech
* Add language auto-detection
* Add a history section
* Dark mode UI
* Turn it into a standalone `.exe` / `.app`

---
