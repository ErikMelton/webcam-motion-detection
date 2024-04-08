import logging
import os

import cv2

from recorder.motion import detect_motion


def run():
    logging.info('Setting up directories...')

    setup_dirs()

    logging.info('Starting camera...')

    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        logging.error('Error: Could not open camera.')

        return

    logging.info('Camera started.')

    detect_motion(cap)

    cap.release()
    cv2.destroyAllWindows()


def setup_dirs():
    if not os.path.exists('./recordings'):
        os.makedirs('./recordings')



