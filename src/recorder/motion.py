import logging
from datetime import datetime

import cv2
import numpy as np

from utils.threading import StoppableThread

FRAME_RATE = 30
MINIMUM_RECORDING_DURATION_SECONDS = 10
GRACE_PERIOD_SECONDS = 5

codec = cv2.VideoWriter_fourcc(*'XVID')


class MotionDetector(StoppableThread):
    def __init__(self, cap, bot):
        super(MotionDetector, self).__init__()
        self.cap = cap
        self.bot = bot

    def run(self):
        self.detect_motion(self.cap, self.bot)

    def detect_motion(self, cap, bot):
        last_mean = 0
        frame_rec_count = 0
        detected_motion = False
        outfile = None
        total_frame_count = 0

        logging.info(f'Will begin recording motion when it is detected in {GRACE_PERIOD_SECONDS} seconds.')

        while True:
            ret, frame = cap.read()

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            result = np.abs(np.mean(gray) - last_mean)
            last_mean = np.mean(gray)

            if total_frame_count < FRAME_RATE * GRACE_PERIOD_SECONDS:
                total_frame_count += 1
                continue

            if result > 1.5:
                # Get the current time in YYYY-MM-DD HH-MM-SS format
                detected_motion_at = datetime.now().strftime('%Y-%m-%d %H-%M-%S')
                detected_motion = True

                logging.info('Motion detected!')

                if frame_rec_count == 0 and not outfile:
                    logging.info(f'Started recording to file {detected_motion_at}.avi')
                    outfile = cv2.VideoWriter(f'./recordings/{detected_motion_at}.avi', codec, 20.0, (640, 480))
                    frame_file = cv2.imencode('.jpg', frame)[1].tobytes()

                    bot.motion_sensed(detected_motion_at, frame_file)
                else:
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

            if cv2.waitKey(1) & 0xFF == ord('q') or self.stopped():
                if outfile:
                    outfile.release()

                logging.info('Exiting...')

                break

