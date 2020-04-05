Colors = {
                             
    'BLUE':'#0000ff',
    'LIGHT BLUE 1':'#6fa8dc',
    'LIGHT BLUE 2':'#9fc5e8',
    'LIGHT BLUE 3':'#cfe2f3',
    'CORNFLOWER BLUE':'#4a86e8',
    'LIGHT CORNFLOWER 1':'#6d9eeb',
    'LIGHT CORNFLOWER 2':'#a4c2f4',
    'LIGHT CORNFLOWER 3':'#c9daf8',
    'RED':'#ff0000',
    'LIGHT RED 1':'#e06666',
    'LIGHT RED 2':'#ea9999',
    'LIGHT RED 3':'#f4cccc',
    'RED BERRY':'#980000',
    'LIGHT RED BERRY 1':'#cc4125',
    'LIGHT RED BERRY 2':'#dd7e6b',
    'LIGHT RED BERRY 3':'#e6b8af',
    'YELLOW':'#ffff00',
    'LIGHT YELLOW 1':'#ffd966',
    'LIGHT YELLOW 2':'#ffe599',
    'LIGHT YELLOW 3':'#fff2cc',
    'ORANGE':'#ff9900',
    'LIGHT ORANGE 1':'#f6b26b',
    'LIGHT ORANGE 2':'#f9cb9c',
    'LIGHT ORANGE 3':'#fce5cd',
    'PURPLE':'#9900ff',
    'LIGHT PURPLE 1':'#8e7cc3',
    'LIGHT PURPLE 2':'#b4a7d6',
    'LIGHT PURPLE 3':'#d9d2e9',
       
}

def rgb(ref):
    hex_color = Colors[ref]
    to_rgb = hex_color.lstrip('#')
    rgb_format = list(tuple(int( to_rgb[i:i+2], 16) for i in (0, 2, 4)))

    return [i/255 for i in rgb_format]
