from renderlib import *

svg = Render(max_screen_width=1200, stretch_to_screen=True, ignore_screen_size=False)

#svg.load_data_from_csv('RWA_19032024_corp_peresch.csv')
#svg.load_data_from_csv('RWA_19032024_corp.csv')
#svg.load_data_from_csv('RWA_19032024.csv')
svg.load_data_from_csv('render_input_RWA.csv')

svg.process_raw_data(normalize_time=False)

svg.render()
svg.save_svg()
svg.save_png()
