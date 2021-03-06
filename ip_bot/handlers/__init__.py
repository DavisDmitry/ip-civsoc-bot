from aiogram import Dispatcher
from aiogram.dispatcher.filters.builtin import IDFilter

from ip_bot.filters import ReplyHashTag
from ip_bot.handlers import join
from ip_bot.handlers.about_civsoc import about_civsoc
from ip_bot.handlers.about_fraction import about_fraction
from ip_bot.handlers.directors_contact_directors_side import directors_reply
from ip_bot.handlers.directors_contact_user_side import (directors_state,
                                                         set_directors_state)
from ip_bot.handlers.get_chat_id import get_chat_id_cmd
from ip_bot.handlers.redaction_contact_redaction_side import redaction_reply
from ip_bot.handlers.redaction_contact_user_side import (redaction_state,
                                                         set_redaction_state)
from ip_bot.handlers.start import start_cmd, start_cq, start_new_cq
from ip_bot.states import Contact


def register_handlers(dp: Dispatcher):
    """
    Registration of all handlers.

    State handlers should be superior to others in their category.

    Order of categories:
    Callback queries handlers
    Commands handlers
    Messages handlers
    """
    # Start handlers by callback queries
    dp.register_callback_query_handler(start_cq, text='start', state='*')
    dp.register_callback_query_handler(start_new_cq,
                                       text='start_new',
                                       state='*')

    join.user_side.register_cq_with_state(dp)

    join.user_side.register_cq(dp)

    # When user click on button 'О фракции'
    dp.register_callback_query_handler(about_fraction, text='about_fraction')

    # When user click on button 'О движении'
    dp.register_callback_query_handler(about_civsoc, text='about_civsoc')

    # When user click on button 'Связаться с директоратом'
    dp.register_callback_query_handler(set_directors_state, text='directors')

    # When user click on button 'Связаться с редакцией'
    dp.register_callback_query_handler(set_redaction_state, text='redaction')

    # Start handler by command
    dp.register_message_handler(start_cmd,
                                chat_type='private',
                                commands='start',
                                state='*')

    # Get chat id by command
    dp.register_message_handler(get_chat_id_cmd,
                                commands='get_chat_id',
                                state='*')

    join.user_side.register_message_with_state(dp)

    # When user send message for directors
    dp.register_message_handler(directors_state, state=Contact.directors)
    dp.register_message_handler(directors_state,
                                ReplyHashTag(hashtags='Директорат'),
                                chat_type='private', is_reply=True, state='*')

    # When user send message for redaction
    dp.register_message_handler(redaction_state, state=Contact.redaction)
    dp.register_message_handler(redaction_state,
                                ReplyHashTag(hashtags='Редакция'),
                                chat_type='private', is_reply=True, state='*')

    # When director replied to message from user
    dp.register_message_handler(directors_reply,
                                IDFilter(chat_id=dp.bot.config.DIRECTORS_CHAT),
                                text_unequal='.',
                                is_reply=True)

    # When redactor replied to message from user
    dp.register_message_handler(redaction_reply,
                                IDFilter(chat_id=dp.bot.config.REDACTION_CHAT),
                                text_unequal='.',
                                is_reply=True)
