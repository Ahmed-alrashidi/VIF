"""
Project: Visual Identity Fingerprint (VIF)
Version: 1.0.0 (Stable Release)
Author: Eng. Ahmed Hamad Al-Rashidi
License: Non-Commercial & Academic Use Only (Patent Pending: SAIP 57168910)
Date: December 11, 2025

Description:
Module for intelligently merging the VIF fingerprint with existing PDF or Image documents.
Uses transparency calibration (0.35) for optimal mobile camera detection.
"""

import fitz  # PyMuPDF
from PIL import Image, ImageEnhance
import os
import sys

# --- SETTINGS ---
OUTPUT_DIR = "vif_output"
FINGERPRINT_PATH = os.path.join(OUTPUT_DIR, "fingerprint_highres.png")
WATERMARK_OPACITY = 0.35  
SCALE_PERCENT = 0.85      

def make_transparent_watermark(input_path, opacity):
    try:
        img = Image.open(input_path).convert("RGBA")
        alpha = img.split()[3]
        alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
        img.putalpha(alpha)
        temp_path = os.path.join(OUTPUT_DIR, "temp_wm.png")
        img.save(temp_path, "PNG")
        return temp_path
    except Exception as e:
        print(f"❌ Error creating watermark: {e}")
        return None

def protect_document(input_file):
    if not os.path.exists(FINGERPRINT_PATH):
        print(f"❌ Error: '{FINGERPRINT_PATH}' not found. Run VIF_Generator.py first.")
        return

    ext = input_file.split('.')[-1].lower()
    base_name = os.path.basename(input_file)
    output_filename = os.path.join(OUTPUT_DIR, f"Protected_{base_name}")
    
    # Ensure PDF output extension
    if ext in ['jpg', 'jpeg', 'png']:
        output_filename = os.path.splitext(output_filename)[0] + ".pdf"

    wm_path = make_transparent_watermark(FINGERPRINT_PATH, WATERMARK_OPACITY)
    if not wm_path: return

    print(f"⚙️  Protecting '{base_name}'...")
    
    try:
        if ext == 'pdf':
            doc = fitz.open(input_file)
            for page in doc:
                page_rect = page.rect
                wm_img = fitz.open(wm_path)
                wm_width = page_rect.width * SCALE_PERCENT
                wm_height = wm_width * (wm_img[0].rect.height / wm_img[0].rect.width)
                x = (page_rect.width - wm_width) / 2
                y = (page_rect.height - wm_height) / 2
                rect = fitz.Rect(x, y, x + wm_width, y + wm_height)
                page.insert_image(rect, filename=wm_path, overlay=True)
            doc.save(output_filename)
            doc.close()

        elif ext in ['jpg', 'jpeg', 'png']:
            base_img = Image.open(input_file).convert("RGBA")
            watermark = Image.open(wm_path).convert("RGBA")
            wm_w = int(base_img.width * SCALE_PERCENT)
            aspect = watermark.height / watermark.width
            wm_h = int(wm_w * aspect)
            watermark = watermark.resize((wm_w, wm_h), Image.Resampling.LANCZOS)
            x = (base_img.width - wm_w) // 2
            y = (base_img.height - wm_h) // 2
            final = Image.new("RGBA", base_img.size)
            final = Image.alpha_composite(base_img, final)
            final.paste(watermark, (x, y), watermark)
            final.convert("RGB").save(output_filename, "PDF")
        else:
            print("❌ Unsupported format. Please use PDF, JPG, or PNG.")
            return

        print(f"✅ Secure Document Created: {output_filename}")
        
    except Exception as e:
        print(f"❌ Processing Error: {e}")
    finally:
        if os.path.exists(wm_path): os.remove(wm_path)

if __name__ == "__main__":
    if not os.path.exists(OUTPUT_DIR): os.makedirs(OUTPUT_DIR)

    # Check for command line arguments first
    if len(sys.argv) > 1:
        target = sys.argv[1]
    else:
        target = input("📄 Enter path to document (PDF/JPG): ").strip().strip("'").strip('"')

    if os.path.exists(target):
        protect_document(target)
    else:
        print("❌ File not found.")
