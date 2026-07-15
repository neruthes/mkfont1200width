import os
import sys
from fontTools.ttLib import TTFont, TTCollection

def modify_full_width_glyphs(font):
    # Disable heavy outline recalculations immediately on load
    font.recalcBBoxes = False
    font.recalcTimestamp = False

    if 'hmtx' not in font or 'cmap' not in font or 'name' not in font or 'head' not in font:
        return
    
    # Dynamically detect full-width size (usually 1000 for OTF/CFF, 2048 for TTF)
    full_width_target = font['head'].unitsPerEm
    padding = int(full_width_target * 0.2) 
    new_width = full_width_target + padding
    lsb_shift = int(padding / 2)

    hmtx = font['hmtx']
    count = 0
    for glyph_name, (width, lsb) in hmtx.metrics.items():
        if width == full_width_target:
            hmtx.metrics[glyph_name] = (new_width, lsb + lsb_shift)
            count += 1
            
    print(f"  Modified {count} full-width glyphs (Target width: {full_width_target} -> {new_width}).")
        
    # 1. Update the 'name' table 
    name_table = font['name']
    records_to_update = []
    for record in name_table.names:
        if record.nameID in [1, 3, 4, 6, 16, 17]:
            try:
                val = record.toUnicode()
                if not val.startswith("Wide1200-") and not val.startswith("Wide1200"):
                    records_to_update.append((val, record.nameID, record.platformID, record.platEncID, record.langID))
            except Exception:
                continue
                
    for val, nameID, platformID, platEncID, langID in records_to_update:
        new_val = "Wide1200-" + val
        if nameID == 6:
            new_val = "Wide1200-" + val.replace(" ", "")
            
        name_table.setName(new_val, nameID, platformID, platEncID, langID)
    
    # 2. Update CFF PostScript names if it's an OTF font with CFF outlines
    if 'CFF ' in font:
        try:
            cff = font['CFF '].cff
            if hasattr(cff, 'fontNames') and len(cff.fontNames) > 0:
                old_ps_name = cff.fontNames[0]
                if not old_ps_name.startswith("Wide1200"):
                    cff.fontNames[0] = "Wide1200-" + old_ps_name.replace(" ", "")
            
            if len(cff.topDictIndex) > 0:
                top_dict = cff.topDictIndex[0]
                if hasattr(top_dict, 'FontName') and top_dict.FontName:
                    if not top_dict.FontName.startswith("Wide1200"):
                        top_dict.FontName = "Wide1200-" + top_dict.FontName.replace(" ", "")
        except Exception as e:
            print(f"  Warning: Failed to update internal CFF table names: {e}")

def main():
    if len(sys.argv) < 3:
        print("Usage: python script.py <input_font> <output_font>")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2]
    
    _, ext = os.path.splitext(input_path.lower())
    
    if ext == '.ttc':
        print(f"Processing TTC collection: {input_path}")
        ttc = TTCollection(input_path)
        print(f"Processing {len(ttc.fonts)} sub-fonts...")
        
        for i, font in enumerate(ttc.fonts):
            print(f"[{i+1}] Checking: {font.get('name').getDebugName(1)}")
            try:
                modify_full_width_glyphs(font)
            except Exception as e:
                print(f"  Error processing font: {e}")
                
        print("Saving TTC collection (a few seconds)...")
        ttc.save(output_path)
        
    elif ext in ['.ttf', '.otf']:
        print(f"Processing single font ({ext.upper()}): {input_path}")
        try:
            # Setting recalcBBoxes=False here covers single fonts on load
            font = TTFont(input_path, recalcBBoxes=False, recalcTimestamp=False)
            print(f"Checking: {font.get('name').getDebugName(1)}")
            modify_full_width_glyphs(font)
            font.save(output_path)
        except Exception as e:
            print(f"  Error processing font: {e}")
            sys.exit(1)
            
    else:
        print(f"Unsupported file extension: {ext}. Please use .ttc, .ttf, or .otf.")
        sys.exit(1)

    print(f"Successfully saved to {output_path}")

if __name__ == "__main__":
    main()
