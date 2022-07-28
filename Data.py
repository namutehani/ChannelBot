from pyrogram.types import InlineKeyboardButton


class Data:
    # Start Message
    START = """
Merhaba {}
    """

    # Home Button
    home_buttons = [
        [InlineKeyboardButton(text="🏠 Ana Menüye Dön 🏠", callback_data="home")],
    ]

    # Rest Buttons
    buttons = [
        [
            InlineKeyboardButton("Nasıl kullanılır ❔", callback_data="help"),
            InlineKeyboardButton("🎪 Hakkında 🎪", callback_data="about")
        ],
    ]

    # Help Message
    HELP = """
Kanal ekle düğmesini kullan veya /add komutunu kullanın!

✨ **Komutlar** ✨

/about - Bot hakkında
/help - Yardım metni
/start - Botu başlatır.

Alternatif komutlar:
/channels - Eklenimilen kanalları listeler
/add - Kanal ekler
/report - Problem bildir
    """

    # About Message
    ABOUT = """
**Bot hakkında** 
    ._.
    """
