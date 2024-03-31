from drawtimeline import *
svg = Render(ignore_screen_size=False)
svg.load_data_from_csv('examples\software_log.csv', encoding='UTF-8')
svg.process_rawdata()
svg.render()
svg.save_png()
svg.save_svg()

