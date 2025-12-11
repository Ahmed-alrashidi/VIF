"""
Project: Visual Identity Fingerprint (VIF)
Version: 1.0.0 (Stable Release)
Author: Eng. Ahmed Hamad Al-Rashidi
License: Non-Commercial & Academic Use Only (Patent Pending: SAIP 57168910)
Date: December 11, 2025

Description:
Core module for generating constructive watermarking text mosaics.
Mobile Optimized (v11.5) with High-Contrast Logic.
"""

import io
import hashlib
import os
import sys
from datetime import datetime, timezone
import cairosvg
from PIL import Image, ImageDraw, ImageFont, ImageChops, ImageFilter
from fpdf import FPDF

# --- CONFIGURATION ---
DEFAULT_LOGO = "LOGO.svg"
OUTPUT_DIR = "vif_output"

class VisualFingerprintGenerator:
    def __init__(self, canvas_size=(2480, 3508)):
        self.canvas_size = canvas_size
        self.font_size = 28  # Mobile Optimized
        self.COLOR_FG = (0, 100, 0, 255) # Dark Green
        self.font = self._load_best_font()

    def _load_best_font(self):
        """Smart font loader for Windows/Linux/Mac"""
        fonts_to_try = [
            "/usr/share/fonts/truetype/liberation/LiberationMono-Bold.ttf", # Linux/Colab
            "arialbd.ttf", # Windows
            "Arial Bold.ttf", # Mac
            "DejaVuSans-Bold.ttf"
        ]
        for font_path in fonts_to_try:
            try:
                return ImageFont.truetype(font_path, self.font_size)
            except:
                continue
        print("⚠️ Warning: System bold font not found. Using default raster font.")
        return ImageFont.load_default()

    def generate_data_string(self, user_id, device_id):
        if not device_id: device_id = "UNK"
        ts = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        return f"U#{user_id}   D#{device_id}   T#{ts}      "

    def _svg_to_mask(self, svg_bytes):
        png_bytes = cairosvg.svg2png(bytestring=svg_bytes, scale=4)
        img = Image.open(io.BytesIO(png_bytes)).convert("RGBA")
        alpha = img.split()[3].resize(self.canvas_size, Image.Resampling.LANCZOS)
        # Using Odd number (31) for MaxFilter to avoid even-kernel errors
        dilated_mask = alpha.filter(ImageFilter.MaxFilter(31))
        return dilated_mask

    def _generate_text_wall(self, text, width, height):
        txt_layer = Image.new('L', (width, height), 0)
        draw = ImageDraw.Draw(txt_layer)

        bbox = self.font.getbbox(text)
        text_w = bbox[2] - bbox[0]
        text_h = bbox[3] - bbox[1]
        
        # Safety check for default font which might return 0
        if text_h == 0: text_h = 20
        if text_w == 0: text_w = 100

        line_height = int(text_h * 1.6) 

        y = -100
        row = 0
        while y < height:
            repeats = int(width / text_w) + 2
            full_line = text * repeats
            x_offset = 0 if row % 2 == 0 else -int(text_w / 2)
            
            # Double Pass for Artificial Bold
            draw.text((x_offset, y), full_line, font=self.font, fill=255)
            draw.text((x_offset + 1, y), full_line, font=self.font, fill=255)

            y += line_height
            row += 1
        return txt_layer

    def create_fingerprint(self, svg_bytes, user_id, device_id):
        print(f"⚙️  Generating VIF Fingerprint for User: {user_id}...")
        data_str = self.generate_data_string(user_id, device_id)
        shape_mask = self._svg_to_mask(svg_bytes)
        w, h = self.canvas_size
        text_texture = self._generate_text_wall(data_str, w, h)

        final_mask = ImageChops.multiply(shape_mask, text_texture)
        final_image = Image.new('RGBA', self.canvas_size, (255, 255, 255, 0))
        solid_color = Image.new('RGBA', self.canvas_size, self.COLOR_FG)
        final_image.paste(solid_color, (0,0), mask=final_mask)
        return final_image, data_str

def main():
    if not os.path.exists(OUTPUT_DIR): os.makedirs(OUTPUT_DIR)
    
    logo_path = DEFAULT_LOGO
    if not os.path.exists(logo_path):
        logo_path = input("⚠️ LOGO.svg not found. Enter path to SVG logo: ").strip().strip('"')
    
    if not os.path.exists(logo_path):
        print("❌ Error: Logo file required to proceed.")
        return

    with open(logo_path, "rb") as f:
        svg_data = f.read()

    # Simulation Data
    user_id = "109207"
    device_id = "WS-RIY-01"

    gen = VisualFingerprintGenerator()
    final_img, raw_data = gen.create_fingerprint(svg_data, user_id, device_id)
    
    # Save Assets
    png_path = os.path.join(OUTPUT_DIR, "fingerprint_highres.png")
    pdf_path = os.path.join(OUTPUT_DIR, "Secure_Document_Auto.pdf")
    
    final_img.save(png_path)
    print(f"✅ Fingerprint saved: {png_path}")

    # Generate PDF Preview
    pdf = FPDF(format='A4')
    pdf.add_page()
    target_width_mm = 190
    x_pos = (210 - target_width_mm) / 2
    pdf.image(png_path, x=x_pos, y=50, w=target_width_mm)
    
    pdf.set_font("Helvetica", size=8)
    data_hash = hashlib.sha256(raw_data.encode()).hexdigest()
    pdf.text(10, 290, f"Digital Forensics Hash: {data_hash}")
    
    pdf.output(pdf_path)
    print(f"✅ Verification PDF saved: {pdf_path}")

if __name__ == "__main__":
    main()
