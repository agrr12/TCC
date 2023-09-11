import analysis_API as AN
import threading
from multiprocessing import Process, Manager

import os

if __name__ == '__main__':
    times = ['hours', 'minutes', 'seconds']
    type = ['hexbin', 'scatter']
    for time in times:
        for type in type:
            out = f'C:\\Users\\agrri\\PycharmProjects\\TCC\\project\\CSVs\\comparison_metrics'
            source = f'C:\\Users\\agrri\\PycharmProjects\\TCC\\sources\\img\\days_hours\\{type}'
            unit_type = f'{time}_{type}'
            manager = Manager()
            shared_list = manager.list()
            AN.compare_image_pairs(source, out, unit_type, shared_list)
