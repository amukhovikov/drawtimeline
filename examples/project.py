from drawtimeline import *

svg = Render()

svg.load_data_from_csv('project.csv', encoding='utf-8')

svg.process_rawdata()
svg.render()
svg.save_svg()
svg.save_png()
