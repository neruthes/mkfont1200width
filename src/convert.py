from fontTools.ttLib import TTCollection
import sys

def modify_full_width_glyphs(font):
    if 'hmtx' not in font or 'cmap' not in font or 'name' not in font:
        return
    
    hmtx = font['hmtx']
    # Iterate through all glyphs in the hmtx table
    # hmtx.metrics is a dict: {glyph_name: (advanceWidth, lsb)}
    
    count = 0
    for glyph_name, (width, lsb) in hmtx.metrics.items():
        # If the glyph is exactly 1000 units wide, expand it to 1200
        if width == 1000:
            # We want to keep the character centered:
            # New width 1200, original 1000. 
            # We add 200 units total. To center, shift LSB by 100.
            hmtx.metrics[glyph_name] = (1200, lsb + 100)
            count += 1
            
    if count > 0:
        print(f"  Modified {count} full-width glyphs.")
        # Update Name table
        name_table = font['name']
        for record in name_table.names:
            if record.nameID in [1, 3, 4, 6]:
                val = record.toUnicode()
                if not val.startswith("Wide1200-"):
                    record.string = "Wide1200-" + val

input_ttc = sys.argv[1]
output_ttc = sys.argv[2]

ttc = TTCollection(input_ttc)
print(f"Processing {len(ttc.fonts)} sub-fonts...")

for i, font in enumerate(ttc.fonts):
    print(f"[{i+1}] Checking: {font.get('name').getDebugName(1)}")
    try:
        modify_full_width_glyphs(font)
    except Exception as e:
        print(f"  Error processing font: {e}")

ttc.save(output_ttc)
print(f"Successfully saved to {output_ttc}")
