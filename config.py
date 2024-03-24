# Главные настройки

default_cell_width = 80         # ширина ячейки в пикселях
default_cell_height = 50        # высота ячейки в пикселях
default_rx = 5                  # радиус загругления прямоугольников с ячейками
default_opacity = 1             # прозрачность ячеек

default_id_column_width = 80    # ширина ячейки с ID системы
default_desc_column_width = 160 # ширина ячейки с описанием системы
default_header_height = 30      # высота заголовка с надписями шкалы
default_data_areas_border = 50  # отступ по вертикали между блоками DATA AREA (одно полотно на ширину размера отрисовываемой картинки)

default_font_size = 14          # размер шрифта по умолчанию


# Рассчитывает размер ячейки по оси X в пикселях, в зависимости от времени
def calc_time_x_width (time_to_calc, width_of_cell):
    return int(time_to_calc.hours * width_of_cell + time_to_calc.minutes * width_of_cell / 60)


# Класс для операций с временем
class Rtime():
    def __init__(self, init_hrs, init_min, init_sec):
        self.hours = init_hrs
        self.minutes = init_min
        self.seconds = init_sec
        self.time = init_hrs * 3600 + init_min * 60 + init_sec
    
    @staticmethod
    def fromstr(string_parameter):
        return Rtime( * (int(i.strip()) for i in string_parameter.split(':')))

    @staticmethod
    def fromint(integer_parameter):
        return Rtime(integer_parameter // 3600 % 60, 
                     integer_parameter // 60 % 60, 
                     integer_parameter % 60)
        
    # точное значение `var` в формате HH:MM:SS
    def __repr__(self):      
        return f'{"{:02d}".format(self.hours)}:{"{:02d}".format(self.minutes)}:{"{:02d}".format(self.seconds)}'
    
    # сокращенное значение в формате HH:MM
    def __str__(self):
        return f'{"{:02d}".format(self.hours)}:{"{:02d}".format(self.minutes)}'
    
    # операция +
    def __add__(self, value):
        return Rtime.fromint(self.time + value.time)

    # операция -
    def __sub__(self, value):
        return Rtime.fromint(self.time - value.time)
    
    # операция <
    def __lt__(self, other):
        return self.time < other.time
    
    # операция >
    def __gt__(self, other):
        return self.time > other.time


# цвета для вывода сообщений в консоль в режиме DEBUG
class bcolors:
    CEND      = '\33[0m'
    CBOLD     = '\33[1m'
    CITALIC   = '\33[3m'
    CURL      = '\33[4m'
    CBLINK    = '\33[5m'
    CBLINK2   = '\33[6m'
    CSELECTED = '\33[7m'
    CBLACK  = '\33[30m'
    CRED    = '\33[31m'
    CGREEN  = '\33[32m'
    CYELLOW = '\33[33m'
    CBLUE   = '\33[34m'
    CVIOLET = '\33[35m'
    CCYAN  = '\33[36m'
    CWHITE  = '\33[37m'


# палитра цветов по-умолчанию (если не загружена из файла)
colors = {
    'green' : {
        'border' : '#A5DD9B',
        'fill' :  '#CCFF99',
        'stroke' : 'black'
    },
    'blue' : {
        'border' : '#8EACCD',
        'fill' :  '#D2E0FB',
        'stroke' : 'black'
    },
    'darkblue' : {
        'border' : '#8EACCD',
        'fill' :  '#7EA6E0',
        'stroke' : 'black'
    },
    'white' : {
        'border' : 'black',
        'fill' :  'white',
        'stroke' : 'black'   
    },
    'red' : {
        'border' : '#B06161',
        'fill' :  '#FFC5C5',
        'stroke' : '#B06161' 
    },
    'yellow' : {
        'border' : '#666600',
        'fill' :  '#FFFF99',
        'stroke' : '#black'
    }, 
    'darkyellow' : {
        'border' : '#666600',
        'fill' :  '#FFFF99',
        'stroke' : '#black'
    },    
    'gray' : {
        'border' : '#525E75',
        'fill' :  '#EEEEEE',
        'stroke' : 'black'  
    },
    'none' : {
        'border' : 'none',
        'fill' : 'none',
        'stroke' : 'black' 
    },
    'black' : {
        'border' : '#525E75',        
        'fill' : '#000000',
        'stroke' : 'white'      
    }, 
    'purple' : {
        'border' : 'red',        
        'fill' : 'purple',
        'stroke' : 'yellow'      
    },     
    'cell' : {
        'border' : '#525E75',        
        'fill' : 'none',
        'stroke' : 'black'     
    }, 
    'grid' : {
        'border' : '#525E75',
        'fill' :  '#EEEEEE',
        'stroke' : 'black'  
    },
    'comments' : {
        'border' : '#525E75',
        'fill' :  '#E0E0E0',
        'stroke' : 'black'          
    },
}

# палитра цветов по-умолчанию (разработана для копирования на случай ошибок в colors, скопируйте отсюда)
default_colors = {
    'green' : {
        'border' : '#A5DD9B',
        'fill' :  '#E1F0DA',
        'stroke' : 'black'
    },
    'blue' : {
        'border' : '#8EACCD',
        'fill' :  '#D2E0FB',
        'stroke' : 'black'
    },
    'white' : {
        'border' : 'black',
        'fill' :  'white',
        'stroke' : 'black'   
    },
    'red' : {
        'border' : '#B06161',
        'fill' :  '#FFC5C5',
        'stroke' : '#B06161' 
    },
    'yellow' : {
        'border' : '#ECEE81',
        'fill' :  '#F6FDC3',
        'stroke' : '#525E75'
    },
    'gray' : {
        'border' : '#525E75',
        'fill' :  '#EEEEEE',
        'stroke' : 'black'  
    },
    'none' : {
        'border' : 'none',
        'fill' : 'none',
        'stroke' : 'black' 
    },
    'black' : {
        'border' : '#525E75',        
        'fill' : '#000000',
        'stroke' : 'white'      
    }, 
    'purple' : {
        'border' : 'red',        
        'fill' : 'purple',
        'stroke' : 'yellow'      
    },     
    'cell' : {
        'border' : '#525E75',        
        'fill' : 'none',
        'stroke' : 'black'     
    }, 
    'grid' : {
        'border' : '#525E75',
        'fill' :  '#EEEEEE',
        'stroke' : 'black'  
    },
    'comments' : {
        'border' : '#525E75',
        'fill' :  'cyan',
        'stroke' : 'black'          
    },
}
