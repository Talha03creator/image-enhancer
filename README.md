# 🎨 AI Image Enhancer

![Project Status](https://img.shields.io/badge/Status-Active-success)
![Python](https://img.shields.io/badge/Python-3.10+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.95+-009688)
![OpenCV](https://img.shields.io/badge/OpenCV-4.7+-5C3EE8)
![License](https://img.shields.io/badge/License-MIT-green)

A professional, fully offline **AI Image Enhancer** web application built with Python and FastAPI. This tool allows users to upload images and apply various enhancements like sharpening, denoising, and brightness correction with instant comparisons.

---

## 📖 Description

**AI Image Enhancer** is a robust web-based tool designed to improve image quality using OpenCV-powered algorithms. Unlike cloud-based tools, this application runs **100% locally** on your machine, ensuring complete privacy and security for your photos. It features a modern, responsive UI with **Light/Dark modes**, a before/after comparison slider, and a full dashboard for managing your enhancement history.

---

## ✨ Features

*   **⚡ Auto Enhancement**: Intelligent improvement of image quality with a single click.
*   **🔆 Brightness & Contrast**: Fine-tune lighting and dynamic range.
*   **🔪 Smart Sharpening**: enhance edges and details without adding noise.
*   **🔇 Denoise (Noise Reduction)**: Remove grain from low-light photos.
*   **🔍 Zoom Preview**: Inspect enhancements up close.
*   **🌗 Before/After Comparison**: Interactive slider to see the difference instantly.
*   **📂 Drag & Drop Upload**: Seamless file handling.
*   **🔐 Authentication System**: Secure Login and Signup functionality.
*   **📜 History Dashboard**: Access and download your previously enhanced images.
*   **🌓 Light/Dark Mode**: Eye-friendly themes for day and night usage.
*   **🚀 Fully Offline**: No API keys required; all processing happens on your device.

---

## 📸 Comparison Preview

<!-- Placeholder for comparison screenshot -->
![Comparison Preview](https://via.placeholder.com/800x400?text=Before+%2F+After+Comparison+Slider)

---

## 🛠️ Tech Stack

*   **Backend Framework**: [FastAPI](https://fastapi.tiangolo.com/) (Python)
*   **Image Processing**: [OpenCV](https://opencv.org/) & NumPy
*   **Database**: SQLite (SQLAlchemy)
*   **Frontend**: HTML5, CSS3 (Custom Variables), JavaScript (Vanilla)
*   **Authentication**: JWT (JSON Web Tokens) with Passlib

---

## 🚀 Installation

Follow these steps to set up the project locally:

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/Talha03creator/image-enhancer.git
    cd image-enhancer
    ```

2.  **Create a Virtual Environment**
    ```bash
    python -m venv venv
    
    # Windows
    venv\Scripts\activate
    
    # Mac/Linux
    source venv/bin/activate
    ```

3.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the Application**
    ```bash
    uvicorn backend.main:app --reload
    ```
    The server will start at `http://127.0.0.1:8000`.

---

## 📖 Usage

1.  Open your browser and navigate to `http://127.0.0.1:8000`.
2.  **Sign Up** for a new account.
3.  Go to the **Dashboard** and upload an image (Drag & Drop or Browse).
4.  Select an enhancement filter (e.g., *Sharpen* or *Denoise*).
5.  Click **Enhance Image**.
6.  Use the **Slider** to compare the Original vs. Enhanced result.
7.  Click **Download** to save the result.

---

## 📂 Folder Structure

```text
image-enhancer/
├── backend/                # FastAPI Backend Logic
│   ├── main.py             # App Entry Point & API Routes
│   ├── auth.py             # Authentication Routes & Logic
│   ├── database.py         # DB Connection
│   ├── models.py           # SQLAlchemy Data Models
│   ├── schemas.py          # Pydantic Schemas
│   └── enhancer.py         # OpenCV Image Processing Logic
│
├── static/                 # Static Assets (CSS, JS, Images)
│   ├── style.css           # Global Styles & Theme Variables
│   ├── script.js           # Dashboard Logic
│   ├── theme.js            # Light/Dark Mode Logic
│   └── ...
│
├── templates/              # HTML Templates (Jinja2)
│   ├── landing.html        # Home/Landing Page
│   ├── dashboard.html      # User Dashboard
│   ├── login.html          # Login Page
│   └── register.html       # Registration Page
│
├── uploads/                # Stores Original Uploaded Images
├── outputs/                # Stores Processed Images
├── sql_app.db              # SQLite Database
├── requirements.txt        # Python Dependencies
└── README.md               # Project Documentation
```

---

## 🔮 Future Improvements

*   [ ] Integration with Deep Learning models (Super-Resolution / GANs).
*   [ ] Cloud storage support for history (AWS S3).
*   [ ] Batch processing for multiple images.
*   [ ] Mobile-friendly PWA version.

---

## 👨‍💻 Author

**Talha Ansari**

*   **LinkedIn**: [Connect with me](https://www.linkedin.com/in/muhammad-talha-6278463a1)

---

## 📄 License

This project is licensed under the **MIT License**. You are free to use, modify, and distribute it.
