# Visual Identity Fingerprint (VIF) 🛡️

[![Patent Pending](https://img.shields.io/badge/Patent-Pending-blue?style=flat-square)](https://www.saip.gov.sa/)
[![License](https://img.shields.io/badge/License-Non--Commercial-red?style=flat-square)](#license)
[![Release](https://img.shields.io/badge/Release-v1.0.0-green?style=flat-square)](#)

> **Official Finalist Project | Absher Tuwaiq Hackathon 2025** 🇸🇦

**Visual Identity Fingerprint (VIF)** is a cybersecurity system designed to combat document leakage. By leveraging **Constructive Watermarking** and **Computer Vision**, VIF transforms an organization's official logo into a covert, intelligent tracking tool containing verified metadata.

---

## 🚀 Key Features

* **Constructive Watermarking:** The logo is reconstructed using data-infused text mosaics instead of solid pixels.
* **Forensic Engine v1.0:** Advanced recovery using Spectral Isolation (HSV), Morphological Welding, and CLAHE algorithms.
* **Ground Truth Verification:** Automated validation system that compares extracted data against system logs to confirm attribution.
* **High Recovery Rate:** Uses statistical consensus to recover User IDs and Device signatures from partial data fragments.

---

## 🛠️ Technology Stack

* **Core:** Python 3.10+
* **Image Processing:** OpenCV, Pillow (PIL), NumPy
* **Vector Graphics:** CairoSVG
* **AI-OCR:** Tesseract 5 (LSTM Neural Nets)
* **PDF Manipulation:** PyMuPDF (Fitz)

---

## 📂 Repository Structure

| File | Description |
| :--- | :--- |
| `VIF_Generator.py` | Generates the secure fingerprint from raw metadata using constructive text layering. |
| `VIF_Overlay.py` | Merges the fingerprint intelligently with PDF/Image documents. |
| `VIF_Forensic_Scanner.py` | **(The Engine)** Analyzes evidence, extracts EXIF data, and recovers hidden text using AI-OCR. |
| `LICENSE` | Custom Non-Commercial License (Patent Protection). |

---

## ⚠️ Intellectual Property Notice

This software is the technical implementation of a patent-pending invention filed with the **Saudi Authority for Intellectual Property (SAIP)**.

* **Invention Title:** Visual Identity Fingerprint (VIF)
* **Application Number:** `57168910`
* **Filing Date:** 2025-10-26
* **Author:** Eng. Ahmed Hamad Al-Rashidi

> **Legal Warning:** Any unauthorized commercial use, reproduction, or deployment of the algorithms described herein is a violation of intellectual property laws.

## 📜 License

This project is licensed under a **Custom Non-Commercial & Academic Use License**.
You are free to view and study the code for educational purposes only.
See the [LICENSE](LICENSE) file for full terms.

---
<div align="center">
  <sub>Made with ❤️ in Buraydah, Al-Qassim | KSA 🌴</sub><br>
  <sub>Absher Tuwaiq Hackathon 2025</sub>
</div>
