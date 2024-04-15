import logging

import cv2
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler

from recorder.motion import MotionDetector

ME_CHAT_ID = 156222616
ALLOWED_USER_IDS = [ME_CHAT_ID]


class TelegramBot:
    def __init__(self, token: str, cap: cv2.VideoCapture):
        self.token = token
        self.application = ApplicationBuilder().token(token).read_timeout(30).connect_timeout(30).build()
        self.cap = cap
        self.motion_detector = None

        start_handler = CommandHandler('start', self.start_cmd)
        security_cam_start_handler = CommandHandler('security_cam_start', self.security_cam_start_cmd)
        security_cam_stop_handler = CommandHandler('security_cam_stop', self.security_cam_stop_cmd)
        callback_query_handler = CallbackQueryHandler(self.callback_query_handler)

        self.application.add_handler(security_cam_start_handler)
        self.application.add_handler(security_cam_stop_handler)
        self.application.add_handler(start_handler)
        self.application.add_handler(callback_query_handler)

    def start(self):
        logging.info('Starting Telegram bot...')

        self.application.run_polling()

    def _check_allowed_user(self, user_id: int):
        return user_id in ALLOWED_USER_IDS

    async def start_cmd(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        keyboard = [
            [
                InlineKeyboardButton('Security Cam Start', callback_data='security_cam_start'),
                InlineKeyboardButton('Security Cam Stop', callback_data='security_cam_stop')
            ]
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text('Choose an option:', reply_markup=reply_markup)

    async def callback_query_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query

        await query.answer()

        if query.data == 'security_cam_start':
            await self.security_cam_start_cmd(update, context)
        elif query.data == 'security_cam_stop':
            await self.security_cam_stop_cmd(update, context)

    async def security_cam_start_cmd(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if self._check_allowed_user(update.effective_user.id):
            await context.bot.send_message(chat_id=ME_CHAT_ID, text='Starting security cam...')

            self.motion_detector = MotionDetector(self.cap, self)
            self.motion_detector.start()

    async def security_cam_stop_cmd(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if self._check_allowed_user(update.effective_user.id):
            await context.bot.send_message(chat_id=ME_CHAT_ID, text='Stopping security cam...')

            self.motion_detector.stop()
            self.motion_detector.join()

            self.motion_detector = None

    def motion_sensed(self, timestamp: str, frame):
        logging.info('Sending motion detected message...')

        message = f'Motion detected at {timestamp}!'
        url = f"https://api.telegram.org/bot{self.token}/sendMessage?chat_id={ME_CHAT_ID}&text={message}"

        requests.get(url)

        photo_send_url = f'https://api.telegram.org/bot{self.token}/sendPhoto'
        params = {'chat_id': ME_CHAT_ID}
        files = {'photo': frame}

        requests.post(photo_send_url, params=params, files=files)

    async def shut_down(self):
        logging.info('Shutting down...')

        await self.application.shutdown()
