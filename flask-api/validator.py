import os, shutil, re

def str2time(text):
    h, m, s = text.split(':')
    return int(h) * 3600 + int(m) * 60 + float(s)

def get_error_log(lines):
    error_log = []
    prev_end_time = 0
    prev_line = ''
    for idx, line in enumerate(lines):
        try:
            # Validate Style
            if line.startswith('Style') and \
                ('panton' not in line.lower() or 'arial' in line.lower()):
                error_log.append(f"Line {idx+1}: incorrect style")
            
            if line.startswith('Dialogue'):
                start_time = str2time(line.split(',')[1])

                # Validate Position
                position = int(line.split(',')[7])
                if 'start' in line.lower() and 'tiempo' in line.lower() and position != 550:
                    error_log.append(f"Line {idx+1}: position of 'Tiempo' != 550")
                if position >= 600:
                    error_log.append(f"Line {idx+1}: position >= 600")

                # Validate Time
                if start_time - prev_end_time >= 10:
                    error_log.append(f"Line {idx+1}: there is a time gap >= 10s with the previous line")

                # Validate Frames timing
                if prev_end_time >= start_time and \
                    (('INSTRUMENTAL' in prev_line and 'tropicalzone' not in line) or
                        ('tropicalzone' in prev_line)):
                    error_log.append(f"Line {idx+1}: 'INSTRUMENTAL' frame is finishing too late or the next line is starting too early")
                
                if prev_end_time >= start_time and '.....' in prev_line and '.....' not in line:
                    error_log.append(f"Line {idx+1}: '.....' frame is finishing too late or the next line is starting too early")

                # Validate {\kf0}
                prev_end_time = str2time(line.split(',')[2])
                prev_line = line

        except:
            error_log.append(f"Unknown error in Line {idx+1}: {line}")
    
    if len(error_log) == 0:
        error_log = ['OK']
    return error_log


        