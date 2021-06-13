#!/usr/bin/env python3
import PySimpleGUI as sg
import numpy as np
import fripp.controls as controls
import fripp.config as config
import time
import soundfile as sf
import pathlib

def slider(key, text, default_value, maximum=100):
    '''Generates a standard slider with associated text'''
    return [sg.Text(text, size=(14,2), pad=(5,(15,0))),
            sg.Slider(key=key,
                      default_value=default_value,
                      disable_number_display=True,
                      tick_interval=None,
                      range=(0,maximum), 
                      orientation='h',
                      size=(28,20), pad=(5,0))]
                    
def broken_line(graph, values):
    spacing = 100/len(values)
    for n,i in enumerate(values):
        graph.DrawLine((n*spacing,50-50*i),
                       (n*spacing,50+50*i),
                       color=config.display_color)
                       
def show_loop(graph, bins=75, norm=False):
    loopsize = np.size(controls.loop,0)
    bw = int(loopsize/bins)
    vu_meter = np.zeros(bins)
    
    # Split the loop in bins and calculate volume
    for i in range(bins):
        vu_meter[i] = (np.linalg.norm(controls.loop[i*bw:(i+1)*bw,:]))
    
    # Normalize
    if norm:
        vu_meter = vu_meter/np.max(vu_meter)
    else:
        vu_meter = vu_meter/32

    # Display the broken line
    graph.Erase()
    broken_line(graph, vu_meter)
        
def gui():
    '''Construct the control panel'''
    sg.theme('Default 1') # LightGray2 is good too

    # All the stuff inside your window.
    layout = [  [sg.Graph(canvas_size=(config.display_width, config.display_height),
                          graph_bottom_left=(0,0), graph_top_right=(100,100),
                          key='canvas')],
                slider('input_gain', 'Input gain', controls.input_gain),
                slider('back_volume', 'Back volume', controls.back_volume),
                slider('loop_volume', 'Loop volume', controls.loop_volume),
                slider('feedback', 'Feedback', controls.feedback),
                [sg.Text('Subdivide', size=(14,2), pad=(5,(15,0))), 
                 sg.Combo(config.subdiv_list, default_value=1,
                 key='subdiv', font=('Sans',10), size=(8,5)),
                 sg.Text('Beats', key='beats', size=(20,1))],
                [sg.Button('Undo'), sg.Button('Clear'), sg.Button('Save'), sg.Button('Stop')]                
             ]

    # Make the main window
    window = sg.Window('Fripp', layout, 
                        return_keyboard_events=True, use_default_focus=False)
    window.Finalize()
    
    # Graph the loop volume
    graph = window['canvas']

    while controls.running:
        show_loop(graph)

        event, values = window.read(timeout=100)
        controls.input_gain = values['input_gain']/50
        controls.back_volume = values['back_volume']/50
        controls.loop_volume = values['loop_volume']/50
        controls.feedback = values['feedback']/100

        # Parse subdiv value
        if str(values['subdiv']).isdigit() and values['subdiv']!='0':
            controls.subdiv = int(values['subdiv'])
        subdiv_interval = np.round(config.bars*config.signature/controls.subdiv,2)
        window['beats'].update('({0} beats)'.format(subdiv_interval))

        if event=='space:65': # On space bar press
            if controls.input_gain != 0:
                controls.last_input_gain = controls.input_gain
                window['input_gain'].update(value=0)
            else:
                window['input_gain'].update(value=controls.last_input_gain*100)

        if event=='Undo':
            # Restore previous loop state
            controls.loop = np.array(controls.last_save)
            print('Restoring the last saved loop')

        if event=='Clear':
            # Empty the buffer
            controls.loop = np.zeros(np.shape(controls.loop))
            
        if event=='Save':
            folder = pathlib.Path(config.save_directory)
            loop_filename = (config.output_filename if config.output_filename else str(time.time())) + '_' + str(controls.saved_loops) + '.flac'
            sf.write(folder/loop_filename, controls.loop, int(controls.samplerate))
            controls.last_save = np.array(controls.loop) # Save for the next undo
            controls.saved_loops += 1
            print('Wrote the current loop to', loop_filename)

        if event=='Stop':
            controls.running = False
            window.close()
            break
