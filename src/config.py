import psutil

from src.data.threshold import ThresholdConfiguration


class Config:
    splash_show_time = 5

    number_of_samples = 20
    cpu_temp_max_value = 100.0
    fan_samples = 10

    font_file_normal = 'UbuntuMono-R.ttf'
    font_file_bold = 'UbuntuMono-B.ttf'

    oled_font_size_normal = 13
    oled_font_size_small = 12
    oled_font_color = '#FFFFFF'

    fan_default_samples = 10

    lcd_color_bg = '#000000'

    lcd_title_color_fg = '#FFFFFF'
    lcd_title_color_bg = '#0000FF'
    lcd_title_font_size = 15

    lcd_histo_pane_width = 140
    lcd_histo_pane_height = 40

    lcd_histo_font_size_normal = 18
    lcd_histo_font_size_small = 14

    lcd_histo_color_fg = '#00FF00'

    lcd_histo_threshold_memory = ThresholdConfiguration(
        default_color='#00FF00',
        max=psutil.virtual_memory().total
    ).complete()

    lcd_histo_samples = 20

    lcd_histo_threshold_cpu = ThresholdConfiguration(
        default_color='#00FF00',
        max= 100.0
    ).add(40, '#00FF00').add(50, '#FFA500').add(100, '#FF0000').complete()

    lcd_histo_threshold_temperature = ThresholdConfiguration(
        default_color='#00FF00',
        max=100.0
    ).add(40, '#00FF00').add(55, '#FFFF00').add(70, '#FFA500').add(80, '#FF0000').complete()


