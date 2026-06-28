import re
from pathlib import Path

def clean_all_svgs_in_folder():
    # 1. Get the exact directory where this script file is sitting
    current_dir = Path(__file__).parent
    
    # 2. Find all files ending in .svg inside this folder
    svg_files = list(current_dir.glob("*.svg"))
    
    if not svg_files:
        print(f"No SVG files found in: {current_dir.resolve()}")
        return

    print(f"Scanning folder: {current_dir.resolve()}")
    print(f"Found {len(svg_files)} SVG file(s). Starting clean up...\n" + "-"*50)

    # 3. Common hardcoded background rect patterns
    patterns = [
        r'<rect[^>]*fill\s*=\s*["\']#(?:fff|ffffff|FFF|FFFFFF|white)["\'][^>]*/>',
        r'<rect[^>]*width\s*=\s*["\']100%["\'][^>]*height\s*=\s*["\']100%["\'][^>]*fill\s*=\s*["\']#[^"\']*["\'][^>]*/>'
    ]

    cleaned_count = 0

    for svg_path in svg_files:
        try:
            svg_content = svg_path.read_text(encoding="utf-8")
            
            # Run regex cleanups
            cleaned_content = svg_content
            for pattern in patterns:
                cleaned_content = re.sub(pattern, "", cleaned_content)
            
            # Only save if changes were actually made
            if cleaned_content != svg_content:
                svg_path.write_text(cleaned_content, encoding="utf-8")
                print(f"✔ Cleaned: {svg_path.name} (Background removed)")
                cleaned_count += 1
            else:
                print(f"➖ Skipped: {svg_path.name} (Already transparent or no rect layer)")
                
        except Exception as e:
            print(f"❌ Error processing {svg_path.name}: {e}")

    print("-"*50 + f"\nDone! Successfully updated {cleaned_count} files.")

if __name__ == "__main__":
    clean_all_svgs_in_folder()