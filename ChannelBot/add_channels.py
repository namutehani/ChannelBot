import asyncio.exceptions
from pyrogram import Client, filters
from pyrogram.errors import ChatAdminRequired, UserNotParticipant, ChannelPrivate
from ChannelBot.database.users_sql import add_channel as uac, remove_channel
from ChannelBot.database.channel_sql import add_channel as cac, remove_channel, get_channel_info
from ChannelBot.settings import channel_settings
from pyrogram.types import InlineKeyboardMarkup


@Client.on_message((filters.regex(r'^\+ Add Channels \+$') | filters.command('add')) & filters.private)
async def _add_channels(bot: Client, msg):
    user_id = msg.from_user.id
    bot_id = (await bot.get_me()).id
    try:
        channel = await bot.ask(user_id,
                                "Lütfen beni kanala admin olarak ekleyin"
                                "\n\nSonra kanaldan mesaj iletin "
                                "\n\nUygulanan işlemi iptal etmek için /cancel komutunu kullanın.Eğer 5 dakika içinde yanıtlanmazsa otomatij iptal edilecektir...", timeout=300)
        while True:
            if channel.forward_from_chat:
                if channel.forward_from_chat.type == 'channel':
                    channel_id = channel.forward_from_chat.id
                    try:
                        chat_member = await bot.get_chat_member(channel_id, bot_id)
                        chat_member_user = await bot.get_chat_member(channel_id, user_id)
                        if chat_member.can_post_messages and chat_member.can_edit_messages:
                            if chat_member_user.status in ['creator', 'administrator']:  # Don't allow non-admins.
                                success, info = await get_channel_info(channel_id)
                                if success:
                                    try:
                                        admin_chat_member = await bot.get_chat_member(channel_id, info['admin_id'])
                                    except (ChatAdminRequired, UserNotParticipant, ChannelPrivate):
                                        await remove_channel(info['admin_id'], channel_id)
                                        admin_chat_member = None
                                else:
                                    admin_chat_member = None
                                if success and admin_chat_member and admin_chat_member.status in ['creator', 'administrator']:  # Already added channel and admin still admin.
                                    admin = await bot.get_users(info['admin_id'])
                                    text = f"This channel is already added by {admin.mention}"
                                    await channel.reply(text, quote=True)
                                else:
                                    await uac(user_id, channel_id)
                                    await cac(channel_id, user_id)
                                    text, markup, _ = await channel_settings(channel_id, bot)
                                    if text:
                                        await msg.reply(text, reply_markup=InlineKeyboardMarkup(markup))
                                    else:
                                        await channel.reply('Kanal bulunamadı lütfen tekrar deneyin !')
                                        await remove_channel(channel_id)
                            else:
                                text = "Adminlik ayarlarımı kontrol et"
                                await channel.reply(text, quote=True)
                            break
                        else:
                            text = "Adminlik ayarlarımda sıkıntı olduğu için işlem yapamıyorum. \n\nLütfen tekrar mesaj iletin veya /cancel ile işlemi iptal edin"
                            channel = await bot.ask(user_id, text, timeout=300, reply_to_message_id=channel.message_id)
                    except (ChatAdminRequired, UserNotParticipant, ChannelPrivate):
                        text = "Tekrar mesaj iletmeyi dene ya da /cancel ile işlemi iptal et"
                        channel = await bot.ask(user_id, text, timeout=300, reply_to_message_id=channel.message_id)
                else:
                    text = 'This is not a channel message. Please try forwarding again  or /cancel the process.'
                    channel = await bot.ask(user_id, text, timeout=300, reply_to_message_id=channel.message_id)
            else:
                if channel.text.startswith('/'):
                    await channel.reply('Kanal eklme işlemi iptal edildi !', quote=True)
                    break
                else:
                    text = 'Lütfen mesaj iletin ya da /cancel komutunu kullanın'
                    channel = await bot.ask(user_id, text, timeout=300, reply_to_message_id=channel.message_id, filters=~filters.me)
    except asyncio.exceptions.TimeoutError:
        await msg.reply('İşlem otomatikmen iptal edildi...', quote=True)
