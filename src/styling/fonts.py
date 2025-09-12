from pathlib import Path
from matplotlib import font_manager

# Get the directory where this script is located
script_dir = Path(__file__).parent

# Set font paths
font_base_path = script_dir.parent / 'static' / 'fonts'
light_font_path = font_base_path / 'Futura-Light.ttf'
medium_font_path = font_base_path / 'Futura-Medium.ttf'
medium_italic_font_path = font_base_path / 'Futura-MediumItalic.ttf'
bold_font_path = font_base_path / 'Futura-Bold.ttf'
condensed_medium_font_path = font_base_path / 'Futura-CondensedMedium.ttf'
condensed_bold_font_path = font_base_path / 'Futura-CondensedExtraBold.ttf'

# Load fonts
font_manager.fontManager.addfont(str(light_font_path))
font_manager.fontManager.addfont(str(medium_font_path))
font_manager.fontManager.addfont(str(medium_italic_font_path))
font_manager.fontManager.addfont(str(bold_font_path))
font_manager.fontManager.addfont(str(condensed_medium_font_path))
font_manager.fontManager.addfont(str(condensed_bold_font_path))

# Create font properties
light_prop = font_manager.FontProperties(fname=str(light_font_path))
medium_prop = font_manager.FontProperties(fname=str(medium_font_path))
medium_italic_prop = font_manager.FontProperties(fname=str(medium_italic_font_path))
bold_prop = font_manager.FontProperties(fname=str(bold_font_path))
condensed_medium_prop = font_manager.FontProperties(fname=str(condensed_medium_font_path))
condensed_bold_prop = font_manager.FontProperties(fname=str(condensed_bold_font_path))

fonts = {
    'light': light_prop,
    'medium': medium_prop,
    'medium_italic': medium_italic_prop,
    'bold': bold_prop,
    'condensed_medium': condensed_medium_prop,
    'condensed_bold': condensed_bold_prop,
}