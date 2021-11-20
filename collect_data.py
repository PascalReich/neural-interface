import argparse
import time
import numpy as np
import pandas as pd
import random

import brainflow
from brainflow.board_shim import BoardShim, BrainFlowInputParams
from brainflow.data_filter import DataFilter, FilterTypes, AggOperations

import pygame
from pygame.locals import *

bgcolor = (251, 240, 217)

pygame.init()
screen = pygame.display.set_mode(flags=pygame.FULLSCREEN)
pygame.display.set_caption('Collect Data')
screen.fill(bgcolor)

font = pygame.font.Font(None, 100)


def display(str):
    screen.fill(bgcolor)

    text = font.render(str, True, (0, 0, 0), bgcolor)
    textRect = text.get_rect()
    textRect.centerx = screen.get_rect().centerx
    textRect.centery = screen.get_rect().centery

    screen.blit(text, textRect)
    pygame.display.update()
    

def main():
    # BoardShim.enable_dev_board_logger()

    board_id = 1
    serial_port = "COM3"

    num_steps = 15
    cur_step = 0
    cur_word = ""
    termBank = ["LEFT", "RIGHT", "UP", "DOWN"]

    next_display = time.time() + 15

    eeg_channels = BoardShim.get_eeg_channels(board_id)

    final_data = None

    params = BrainFlowInputParams()
    # params.ip_port = args.ip_port
    params.serial_port = serial_port
    #params.mac_address = args.mac_address
    #params.other_info = args.other_info
    #params.serial_number = args.serial_number
    #params.ip_address = args.ip_address
    #params.ip_protocol = args.ip_protocol
    #params.timeout = args.timeout
    #params.file = args.file

    board = BoardShim(board_id, params)
    board.prepare_session()
    print("connected")
    display("connected")

    board.start_stream(45000)

    print("Starting in 5 seconds")
    display("Starting in 5 seconds")
    time.sleep(5)
    while True:
        board.get_board_data() # clear buffer
        print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n"* 5) # clear terminal
        next_word = random.choice(termBank)
        while cur_word == next_word:
            next_word = random.choice(termBank)# choose word
        cur_word = next_word
        print(cur_word)  # display word
        display(cur_word)
        time.sleep(2)  # wait to gather data
        data = board.get_board_data()  # collect data
        display("")

        # now we are off the clock

        collected_data = []

        for channel in eeg_channels:
            collected_data.append(data[channel])

        """for i in range(len(collected_data)):
            collected_data[i].insert(0, cur_step)
            collected_data[i].insert(1, termBank.index(cur_word))"""

        collected_data = np.array(collected_data)

        collected_data = np.insert(collected_data, 0, cur_step, axis=0)
        collected_data = np.insert(collected_data, 1, termBank.index(cur_word), axis=0)

        # print(collected_data)


        """if final_data is not None:
            print(final_data)
            for i in range(len(final_data)):
                final_data[i].append(collected_data[i])
        else:
            final_data = collected_data
            """
        if final_data is not None:
            # print(final_data)
            final_data = np.hstack((final_data, collected_data))
        else:
            final_data = collected_data
        
        #final_data.append(collected_data)

        # clean up

        cur_step += 1
        
        pygame.event.pump()
        keys = pygame.key.get_pressed()
        if keys[K_ESCAPE]:
            display("Saving Session")
            break
            

        end  = time.time() + 5
        wait = False
        
        while time.time() < end:
            pygame.event.pump()
            keys = pygame.key.get_pressed()
            if keys[K_SPACE]:
                wait = True
                display("Pausing")
                time.sleep(1)
                break
                
        while wait:
            display("Paused. Press SPACE to unpause")
            pygame.event.pump()
            keys = pygame.key.get_pressed()
            if keys[K_SPACE]:
                display("Unpausing in 3 seconds")
                time.sleep(2)
                display("")
                time.sleep(1)
                break
            
            
        pygame.event.pump()
        keys = pygame.key.get_pressed()
        if keys[K_ESCAPE]:
            display("Saving Session")
            break
                
                

    board.stop_stream()
    board.release_session()

    # train_data = []

    # demo for transforms
    
    # df = pd.DataFrame(np.transpose(train_data))

    print(final_data)

    train_data = np.array(final_data)
    
    file = f'out/test-{time.time()}.csv'

    DataFilter.write_file(train_data, file, 'w')

    print(data)
    
    print(f"saved to {file}")


if __name__ == "__main__":
    main()