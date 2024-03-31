# drawtimeline 4.1

import drawsvg 
import csv
import json
from config import *

       
# Tile - класс для ячеек с данными
class Tile:

    def __init__(self, rowid, start, finish, real_start, real_finish, duration, color, caption, font_size, rx, opacity):
        self.rowid = rowid
        self.start = start
        self.finish = finish
        self.real_start = real_start
        self.real_finish = real_finish
        self.duration = duration
        self.color = color
        self.border_color = colors[color]['border']
        self.fill_color = colors[color]['fill']
        self.stroke_color = colors[color]['stroke']
        self.caption = caption[0]
        self.caption2 = caption[1]
        self.font_size = font_size
        self.rx = rx
        self.opacity = opacity

    def __str__(self):
        return f"<Start:{self.start} finish:{self.finish} caption:'{self.caption}' duration:{self.duration}>"



# Data_area - класс для блока данных с набором отрисовываемых временных шкал
class Data_area:

    def __init__(self, id, time_start, time_finish):
        
        # ID
        self.id = id
        self.time_start = time_start
        self.time_finish = time_finish
        
        self.tiles = []
    
    def __str__(self):
        return f'Data_area #{self.id}, Time {repr(self.time_start)} - {repr(self.time_finish)}'



# Render - основной класс для отрисовки
class Render:

    # 0 шаг, инициализация
    def __init__(self, max_screen_width=1920, ignore_screen_size=True, debug=False, stretch_to_screen=False):
        
        self.d = drawsvg.Drawing(0,0)    

        # data arrays
        self.rawdata = []                   # rawdata from file source
        self.id_array = []                  # array for ID column
        self.desc_array = []                # array for DESCRIPTION column
        self.data_area = []                 # array for data areas with tiles  
        self.comments = []                  # array for comments list

        # variables
        self.width = max_screen_width
        self.max_time = Rtime.fromint(0)    # max time in data
        self.render_time = Rtime.fromint(0) # max time in rendered data area
        self.max_rows = 0                   # max number of rows
        self.max_cols = 0                   # max number of data columns
        self.data_count = 1                 # number of data areas, default = 1
        self.render_width = 0
        self.max_comments = 0
 
        # settings
        self.ignore_screen_size = ignore_screen_size
        self.filename = ''
        self.debug_mode = debug  
        self.stretch_to_screen = stretch_to_screen
        self.max_screen_width = max_screen_width


    # print debug information 
    def debug(self, debug_element):
        if self.debug:
            print (debug_element)


    # 1 шаг (CSV)
    # Формат CSV:  [0] номер дорожки, [1] ID источника/системы, [2] Описание источника/системы, [3] время старта, [4] время завершения, [5] цвет, [6] описание действий
    # кодировка по умолчанию = CP1251
    def load_data_from_csv (self, filename, encoding='cp1251'):

        self.debug (f"\n{bcolors.CYELLOW}Loading raw data from CSV '{bcolors.CGREEN}{filename}{bcolors.CEND}'")
        self.filename = filename
        file_row_id = 0
        with open(self.filename, encoding=encoding) as csv_file:
            # читаем файл по строкам
            for row in csv.reader(csv_file, delimiter=';'):
                file_row_id += 1
                cell_start_time = Rtime.fromstr (row[3])
                cell_finish_time = Rtime.fromstr (row[4])
                if self.max_time < cell_finish_time:
                    self.max_time = cell_finish_time
                if self.max_rows < int(row[0]):
                    self.max_rows = int(row[0])
                # добавляем в rawdata
                self.rawdata.append({
                    'filerowid' : file_row_id,
                    'rowid': int(row[0]) - 1, 
                    'id_text': row[1].strip(),
                    'desc_text': row[2].strip(),
                    'start': cell_start_time,
                    'finish': cell_finish_time,
                    'duration': cell_finish_time - cell_start_time,
                    'color': row[5],
                    'caption': row[6],
                    'fontsize': default_font_size,
                    'rx': default_rx,
                    'opacity': default_opacity,
                    })
                self.debug(self.rawdata[len(self.rawdata) - 1])
        self.debug(f"{bcolors.CCYAN}Loaded raw data:{bcolors.CEND}\n\t- {bcolors.CGREEN}{len(self.rawdata)}{bcolors.CEND} rows" +
                   f"\n\t- {bcolors.CGREEN}{self.max_rows}{bcolors.CEND} data rows" +
                   f"\n\t- {bcolors.CGREEN}{self.max_time}{bcolors.CEND} max time")


    # 1 шаг (JSON)
    # JSON формат:  BUG: _no format_
    # кодировка по умолчанию = UTF-8
    def load_data_from_json (self, filename, encoding='utf-8'):

        self.debug (f"\n{bcolors.CYELLOW}Loading raw data from JSON '{bcolors.CGREEN}{filename}{bcolors.CEND}'")
        self.filename = filename
        file_row_id = 0
        with open(self.filename, encoding='utf-8') as csv_file:
            # читаем файл по строкам
            for row in csv.reader(csv_file, delimiter=';'):
                file_row_id += 1
                cell_start_time = Rtime.fromstr (row[3])
                cell_finish_time = Rtime.fromstr (row[4])
                if self.max_time < cell_finish_time:
                    self.max_time = cell_finish_time
                if self.max_rows < int(row[0]):
                    self.max_rows = int(row[0])
                # добавляем в rawdata
                self.rawdata.append({
                    'filerowid' : file_row_id,
                    'rowid': int(row[0]) - 1, 
                    'id_text': row[1].strip(),
                    'desc_text': row[2].strip(),
                    'start': cell_start_time,
                    'finish': cell_finish_time,
                    'duration': cell_finish_time - cell_start_time,
                    'color': row[5],
                    'caption': row[6],
                    'fontsize': default_font_size,
                    'rx': default_rx,
                    'opacity': default_opacity,
                    })
                self.debug(self.rawdata[len(self.rawdata) - 1])
        self.debug(f"{bcolors.CCYAN}Loaded raw data:{bcolors.CEND}\n\t- {bcolors.CGREEN}{len(self.rawdata)}{bcolors.CEND} rows" +
                   f"\n\t- {bcolors.CGREEN}{self.max_rows}{bcolors.CEND} data rows" +
                   f"\n\t- {bcolors.CGREEN}{self.max_time}{bcolors.CEND} max time")
        

    # 2 шаг - обработка загруженных данных в rawdata
    def process_rawdata(self, normalize_time=False):
    
        self.debug(f"\n{bcolors.CYELLOW}Processing raw data{bcolors.CEND} (time normalization flag = {bcolors.CYELLOW}{normalize_time}{bcolors.CEND})")

        min_time = Rtime(1000,0,0)
        
        # загрузить ID и описания, вычислить временные рамки
        for i in range (self.max_rows):
            self.id_array.append("")
            self.desc_array.append("")
        for rw in self.rawdata:
            self.id_array[rw['rowid']] = rw['id_text']
            self.desc_array[rw['rowid']] = rw['desc_text']
            # расчет минимального времени начала
            if rw['start'] < min_time:
                min_time = Rtime.fromint(rw['start'].time)
        
        # normalize_time: если значение TRUE, вычисляем min время начала и сдвигаем влево все ячейки к отметке T = 00:00:00 (TRIM времени по левой границе, нормализация)
        if normalize_time:
            self.debug (f"Normalizing time, delta = {bcolors.CYELLOW}{min_time}{bcolors.CEND}")
            for i in range(len(self.rawdata)):
                self.rawdata[i]['start'] -= min_time
                self.rawdata[i]['finish'] -= min_time
                print (self.rawdata[i])

        self.debug(f"{bcolors.CCYAN}Loaded ID{bcolors.CEND}")
        for i in range(self.max_rows):
            self.debug(f"\t{i+1}\t{self.id_array[i]}")

        self.debug(f"{bcolors.CCYAN}Loaded Description{bcolors.CEND}")
        for i in range(self.max_rows):
            self.debug(f"\t{i+1}\t{self.desc_array[i]}")
            
        # расчет размеров отрисовки и параметров рендера
        self.debug(f"{bcolors.CCYAN}Render parameters{bcolors.CEND}")
        data_tiles_max_width = calc_time_x_width(self.max_time, default_cell_width)
        render_screen_max_width = default_id_column_width + default_desc_column_width + data_tiles_max_width

        if render_screen_max_width < self.width:
            self.width = render_screen_max_width + 50

        if (self.ignore_screen_size): 
            data_tiles_width = data_tiles_max_width
        else:
            data_tiles_width = self.width - default_id_column_width - default_desc_column_width

        self.render_width = default_id_column_width + default_desc_column_width + data_tiles_width + 50 * self.ignore_screen_size + 50

        self.debug (f"\tIgnore screen size - {bcolors.CGREEN}{self.ignore_screen_size}{bcolors.CEND}" +
                    f"\n\tScreen width - {bcolors.CGREEN}{self.width}{bcolors.CEND} with cell width - {bcolors.CGREEN}{default_cell_width}{bcolors.CEND} " +
                    f"\n\tCalculated data tiles MAX width - {bcolors.CGREEN}{data_tiles_max_width}{bcolors.CEND} " +
                    f"\n\t" + 
                    f"ID width - {bcolors.CGREEN}{default_id_column_width}{bcolors.CEND} " +
                    f"Desc width - {bcolors.CGREEN}{default_desc_column_width}{bcolors.CEND} " +
                    f"Data tiles width - {bcolors.CGREEN}{data_tiles_width}{bcolors.CEND} " +
                    f"Render width - {bcolors.CGREEN}{self.render_width}{bcolors.CEND}")

        # расчет разсмера картинки и числа блоков с data_area
        if not self.ignore_screen_size:
            self.max_cols = 1
            while self.width > default_id_column_width + default_desc_column_width + self.max_cols * default_cell_width:
                self.max_cols += 1
            if self.width < default_id_column_width + default_desc_column_width + self.max_cols * default_cell_width:
                self.max_cols -= 1
            while self.data_count * self.max_cols * Rtime (1,0,0).time < self.max_time.time:
                self.data_count += 1

        if self.ignore_screen_size:
            self.max_cols = self.max_time.time // Rtime(1,0,0).time + 1

        self.debug (f"\tNumber of data areas - {bcolors.CGREEN}{self.data_count}{bcolors.CEND}")
        self.debug (f"\tNumber of hours in data area - {bcolors.CGREEN}{self.max_cols}{bcolors.CEND} with {bcolors.CGREEN}{self.max_cols}{bcolors.CEND} columns")
        
        # первоначальное наполнение массива элементов data_area с параметрами времени начала и завершения
        render_time = Rtime.fromint (Rtime(1,0,0).time * self.max_cols)     #  render time = 1 hour * number of cells
        self.debug (f"{bcolors.CCYAN}Calculated data areas{bcolors.CEND}")
        self.debug (f"\tmax cols = {bcolors.CYELLOW}{self.max_cols}{bcolors.CEND} render time = {bcolors.CYELLOW}{render_time}{bcolors.CEND}")

        for i in range (self.data_count):
            if i == 0:
                t_start = Rtime.fromint(0)
                t_finish = render_time
            else:
                t_start = Rtime.fromint (t_finish.time + 1)
                t_finish = Rtime.fromint (render_time.time * (i + 1))
            self.data_area.append(Data_area(i, t_start, t_finish))
            self.debug(f"\t{self.data_area[i]}")

        # наполнение всех data_area с соответствущими их времени начала и завершения ячейками (tile)
        self.debug (f"{bcolors.CCYAN}Filling data areas with tiles{bcolors.CEND}")
        for rw in self.rawdata:
            # расчет data_area
            area_start = self.get_data_area(rw['start'])
            area_finish = self.get_data_area(rw['finish'])
            if area_start != area_finish:
                print (f"\t{bcolors.CRED}Split{bcolors.CEND} Row {bcolors.CYELLOW}{rw['filerowid']}{bcolors.CEND} : " +
                       f"{bcolors.CYELLOW}{rw['start']} - {rw['finish']}{bcolors.CEND}" +
                       f" between data area {bcolors.CGREEN}{area_start}{bcolors.CEND} and {bcolors.CGREEN}{area_finish}{bcolors.CEND}" +
                       f" (cell finish - {bcolors.CYELLOW}{rw['finish']}{bcolors.CEND})," +
                       f" data area finish - {bcolors.CYELLOW}{self.data_area[area_start].time_finish}{bcolors.CEND})")
            # добавление ячеек
            self.debug (f"{bcolors.CRED}\tSplit row {bcolors.CYELLOW}{rw['filerowid']}{bcolors.CEND}" +
                        f" between total areas = {bcolors.CYELLOW}{self.data_count}{bcolors.CEND} " +
                        f"area_start={bcolors.CYELLOW}{area_start}{bcolors.CEND} area_finish={bcolors.CYELLOW}{area_finish}{bcolors.CEND}")
            for da in range (area_start, area_finish + 1):
                # расчет точного времени начала и завершения для rw" ячейки в [da] data_area
                if da == area_start:
                    r_st_time = Rtime.fromint(max(self.data_area[da].time_start.time, rw['start'].time) - render_time.time * da)
                else:
                    r_st_time = Rtime.fromint(0)
                if da == area_finish:
                    r_fi_time = Rtime.fromint(min(self.data_area[da].time_finish.time, rw['finish'].time) - render_time.time * da)
                else:
                    r_fi_time = render_time
                self.debug(f"\t  Time bounds for file row {bcolors.CYELLOW}{rw['filerowid']}{bcolors.CEND} " +
                           f"in data area {bcolors.CYELLOW}{da}{bcolors.CEND} is {bcolors.CGREEN}{repr(r_st_time)} - {repr(r_fi_time)}{bcolors.CEND}")
                # разделение ячейки ("перенос строки", если не помещается в текущий блок данных)
                cell_cap1 = rw['caption']
                cell_cap2 = f"{rw['duration']}"
                self.data_area[da].tiles.append(Tile(rw['rowid'], r_st_time, r_fi_time, rw['start'], rw['finish'], rw['duration'], rw['color'], 
                                                     [cell_cap1, cell_cap2], rw['fontsize'], rw['rx'], rw['opacity']))                    

        self.debug (f"\n{bcolors.CCYAN}Calculated tiles:")
        for da in self.data_area:
            self.debug (f"\t{bcolors.CYELLOW}Data area {da.id}{bcolors.CEND}")
            for ti in da.tiles:
                self.debug (f"\t\t{ti}" +
                            f" {bcolors.CRED}{calc_time_x_width(ti.duration, default_cell_width)} px{bcolors.CEND}")  

    # функция get_data_area рассчитывает номер блока данных (data_area) по заданному времени завершения действия, т.е. куда попадает ячейка
    def get_data_area (self, calc_time):
        for i in range(self.data_count):
            if calc_time.time <= self.data_area[i].time_finish.time:
                return i
        return self.data_count

    # 3 шаг, отрисовка
    def render(self):
        self.debug (f"{bcolors.CYELLOW}Rendering data{bcolors.CEND}")
        self.debug (f"\tCell width {bcolors.CGREEN}{default_cell_width}{bcolors.CEND} height {bcolors.CGREEN}{default_cell_height}{bcolors.CEND}")
        self.debug (f"\tData area with {bcolors.CGREEN}{self.max_rows}{bcolors.CEND} rows, header size " +
                    f"{bcolors.CGREEN}{default_header_height}{bcolors.CEND}, data area spacing " +
                    f"{bcolors.CGREEN}{default_data_areas_border}{bcolors.CEND}")
        
        da_data_height = default_cell_height * self.max_rows 
        da_height = default_header_height + da_data_height + default_data_areas_border

        # определение комментариев и дополнительного места 
        for da in self.data_area:
            data_y = da.id * da_height
            for ti in da.tiles:
                tix = default_id_column_width + default_desc_column_width + calc_time_x_width (ti.start, default_cell_width)
                tiy = data_y + default_header_height + ti.rowid * default_cell_height
                tiw = calc_time_x_width (ti.finish - ti.start, default_cell_width)
                text_size = default_font_size * len(ti.caption)
                if text_size > tiw:
                    self.max_comments += 1
                
        
        if self.stretch_to_screen:
            self.debug (f"{bcolors.CRED}Stretch to screen:{bcolors.CEND} render width {bcolors.CYELLOW}{self.render_width}{bcolors.CEND} " +
                        f"max screen width {bcolors.CYELLOW}{self.max_screen_width}{bcolors.CEND}")
            if self.render_width > self.max_screen_width:
                self.debug (f"Set Drawing width  {bcolors.CYELLOW}{self.render_width}{bcolors.CEND}")
                self.d = drawsvg.Drawing(self.render_width, da_height * self.data_count + self.max_comments * (default_font_size + 5)) 
            else:
                self.debug (f"Set Drawing width {bcolors.CYELLOW}{self.max_screen_width}{bcolors.CEND}")
                self.d = drawsvg.Drawing(self.max_screen_width, da_height * self.data_count + self.max_comments * (default_font_size + 5)) 
                self.d.append (drawsvg.Rectangle (0, 0, 
                                                  self.max_screen_width, da_height * self.data_count + self.max_comments * (default_font_size + 5), 
                                                  fill='white', stroke='white'))
        else:
            self.d = drawsvg.Drawing(self.render_width, da_height * self.data_count + self.max_comments * (default_font_size + 5)) 
        self.d.append (drawsvg.Rectangle (0, 0, self.render_width, da_height * self.data_count + self.max_comments * (default_font_size + 5), fill='white', stroke='white'))
        
        self.max_comments = 0
        for da in self.data_area:
            data_y = da.id * da_height

            # нарисовать полотно (canvas)
            self.debug (f"\tData area {bcolors.CYELLOW}{da.id}{bcolors.CEND} Y from {bcolors.CGREEN}{data_y}{bcolors.CEND} to {bcolors.CGREEN}{data_y + da_height}{bcolors.CEND}")

            # прямоугольники с данными
            self.d.append (drawsvg.Rectangle (default_id_column_width + default_desc_column_width, data_y + default_header_height, 
                                              self.max_cols * default_cell_width, da_data_height, fill='none', stroke=colors['grid']['border']))
            # разметка клеток по вертикали
            for i in range (self.max_cols):
                self.d.append (drawsvg.Rectangle (default_id_column_width + default_desc_column_width + i * default_cell_width, data_y + default_header_height, 
                                default_cell_width, da_data_height, fill='none', stroke=colors['grid']['border']))
            # разметка клеток по горизонтали
            for i in range (self.max_rows):
                self.d.append (drawsvg.Rectangle (0, data_y + default_header_height + i * default_cell_height, 
                                default_id_column_width + default_desc_column_width + self.max_cols * default_cell_width, default_cell_height, fill='none', stroke=colors['grid']['border']))
            # подписи временной шкалы
            for i in range (self.max_cols+1):
                self.d.append(drawsvg.Text(f"{i + self.max_cols * da.id}", default_font_size, 
                                default_id_column_width + default_desc_column_width + default_cell_width * i, 
                                data_y + default_header_height - 5, 
                                fill='black'))            
            # отрисовка прямоугольников с ID
            self.d.append (drawsvg.Rectangle (0, data_y + default_header_height, 
                                              default_id_column_width, da_data_height, fill='none', stroke=colors['grid']['border']))
            for i in range (self.max_rows):
                self.d.append(drawsvg.Text(self.id_array[i], default_font_size, 
                                10, 
                                data_y + default_header_height + i * default_cell_height + default_cell_height // 2, 
                                fill='black'))                  
            # отрисовка прямоугольников с описанием (description)
            self.d.append (drawsvg.Rectangle (default_id_column_width, data_y + default_header_height, 
                                              default_desc_column_width, da_data_height, fill='none', stroke=colors['grid']['border']))  
            for i in range (self.max_rows):
                self.d.append(drawsvg.Text(self.desc_array[i], default_font_size, 
                                default_id_column_width + 10, 
                                data_y + default_header_height + i * default_cell_height + default_cell_height // 2, 
                                fill='black'))                         
            # отрисовка ячеек
            for ti in da.tiles:
                tix = default_id_column_width + default_desc_column_width + calc_time_x_width (ti.start, default_cell_width)
                tiy = data_y + default_header_height + ti.rowid * default_cell_height
                tiw = calc_time_x_width (ti.finish - ti.start, default_cell_width)
                self.d.append (drawsvg.Rectangle (tix, tiy, tiw, default_cell_height, fill=ti.fill_color, stroke=ti.border_color, rx=ti.rx))
                
                # расчет ширины текста в пикселях (помещается или нет в ячейку...)
                text_size = max(default_font_size // 1.7 * len(ti.caption), default_font_size * len(ti.caption2))

                if text_size > tiw + default_font_size * 2:
                    self.max_comments += 1
                    ticaption1 = f"({self.max_comments})"
                    ticaption2 = ""
                    self.comments.append (f"({self.max_comments}) {ti.caption} : {ti.caption2}")
                    self.debug (f"\t{bcolors.CRED}Add comments: {bcolors.CEND} {bcolors.CYELLOW}{self.comments[self.max_comments - 1]} " +
                                f"{bcolors.CRED}{text_size} pixels{bcolors.CEND}")                
                    radius = default_font_size
                    center_x = tix + tiw // 2 
                    center_y = tiy + default_cell_height // 2 
                    self.d.append (drawsvg.Circle(center_x, center_y, radius * len(str(self.max_comments)), stroke=colors['comments']['border'], fill=colors['comments']['fill']))
                    self.d.append (drawsvg.Text(f"{self.max_comments}", default_font_size, center_x - len(str(self.max_comments)) * default_font_size // 2 + 3, 
                                                center_y + 3, stroke=colors['comments']['stroke']))
                else:
                    ticaption1 = f"{ti.caption}"
                    ticaption2 = f"{ti.caption2}"
                    # печать дополнительного текста в ячейке (вторая строка, преимущественно выводится время этапа)
                    self.d.append(drawsvg.Text(ticaption1, default_font_size, tix + 5, tiy + default_cell_height // 2 - 5, fill=ti.stroke_color)) 
                    self.d.append(drawsvg.Text(ticaption2, default_font_size, tix + 5, tiy + default_cell_height // 2 + default_font_size , fill=ti.stroke_color)) 
            
        # отрисовка комментариев
        for i in range (self.max_comments):
            self.d.append(drawsvg.Text(self.comments[i], default_font_size, 
                                       5, da_height * self.data_count + i * default_font_size, fill='black'))                 
    
    # 4 шаг, сохранение PNG
    def save_png (self):
        self.debug (f"\n{bcolors.CYELLOW}Saved PNG file: {bcolors.CGREEN} {self.filename + '.png'}{bcolors.CEND}")
        self.d.save_png(self.filename + '.png')        
    
    # 4 шаг, сохранение SVG
    def save_svg (self):
        self.debug (f"\n{bcolors.CYELLOW}Saved SVG file: {bcolors.CGREEN} {self.filename + '.svg'}{bcolors.CEND}")
        self.d.save_svg(self.filename + '.svg')    


