from drawtimeline import *

svg = Render()

svg.load_data_from_csv('examples\colors.csv', encoding='cp1251')

svg.process_rawdata(normalize_time=False)

svg.render()
svg.save_svg()
svg.save_png()
