import logging
import os
from datetime import datetime

import cv2
import numpy as np

logging.basicConfig(level=logging.INFO)

FRAME_RATE = 30
MINIMUM_RECORDING_DURATION_SECONDS = 10
GRACE_PERIOD_SECONDS = 5

codec = cv2.VideoWriter_fourcc(*'XVID')


def main():
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


def detect_motion(cap):
    last_mean = 0
    frame_rec_count = 0
    total_frame_count = 0
    detected_motion = False
    outfile = None

    logging.info(f'Will begin recording motion when it is detected in {GRACE_PERIOD_SECONDS} seconds.')

    while True:
        ret, frame = cap.read()
        cv2.imshow('frame', frame)

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        result = np.abs(np.mean(gray) - last_mean)
        last_mean = np.mean(gray)

        if total_frame_count < FRAME_RATE * GRACE_PERIOD_SECONDS:
            total_frame_count += 1
            continue

        if result > 0.4:
            # Get the current time in YYYY-MM-DD HH-MM-SS format
            detected_motion_at = datetime.now().strftime('%Y-%m-%d %H-%M-%S')
            detected_motion = True

            logging.info('Motion detected!')

            if frame_rec_count == 0 and not outfile:
                logging.info(f'Started recording to file {detected_motion_at}.avi')
                outfile = cv2.VideoWriter(f'./recordings/{detected_motion_at}.avi', codec, 20.0, (640, 480))
            else:
                logging.info(f'Continuing recording to file {detected_motion_at}.avi')
                frame_rec_count = 0

        if detected_motion:
            outfile.write(frame)
            frame_rec_count += 1

        if frame_rec_count >= (FRAME_RATE * MINIMUM_RECORDING_DURATION_SECONDS):
            logging.info('Stopped recording.')
            detected_motion = False
            frame_rec_count = 0
            outfile.release()
            outfile = None

        if cv2.waitKey(1) & 0xFF == ord('q'):
            if outfile:
                outfile.release()

            logging.info('Exiting...')

            break


def setup_dirs():
    if not os.path.exists('./recordings'):
        os.makedirs('./recordings')


if __name__ == '__main__':
    main()