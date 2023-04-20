from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, ChatJoinRequest
from pyrogram import Client, enums, filters
from pyrogram.errors import UserNotParticipant
from info import AUTH_CHANNEL, ADMINS
from database.fsub_db import Fsub_DB

LINK = None

@Client.on_chat_join_request(filters.chat(AUTH_CHANNEL))
async def filter_join_reqs(bot, message: ChatJoinRequest):
    user_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name
    date = message.date
    await Fsub_DB().add_user(user_id=str(user_id), username=username, first_name=first_name, date=date)

@Client.on_message(filters.command("total_requests") & filters.private & filters.user(ADMINS))
async def get_all_reqs(bot, message):
    total = await Fsub_DB().total_users()
    return await message.reply_text(f"<b>Total Requests: {total}</b>")

@Client.on_message(filters.command("delete_requests") & filters.private & filters.user(ADMINS))
async def delete_all_reqs(bot, message):
    total = await Fsub_DB().total_users()
    await Fsub_DB().purge_users()
    return await message.reply_text(f"<b>Successfully deleted all {total} requests...</b>")

async def Force_Sub(bot: Client, message: Message, file_id = False, mode = "checksub"):
    global LINK
    if not AUTH_CHANNEL:
        return True
    try:
        if LINK == None:
            link = await bot.create_chat_invite_link(
                chat_id=AUTH_CHANNEL,
                creates_join_request=True
            )
            LINK = link
            print("Created Invite Link !")
        else:
            link = LINK
    except Exception as e:
        print(f"Unable to create Invite link !\n\nError: {e}")
        return False
    try:
        user = await Fsub_DB().get_user(str(message.from_user.id))
        if user and str(user["id"]) == str(message.from_user.id):
            return True
    except Exception as e:
        print(f"Error: {e}")
        await message.reply(
            text=f"Error: {e}",
            parse_mode=enums.ParseMode.MARKDOWN,
            disable_web_page_preview=True
        )
        return False
    try:
        await bot.get_chat_member(
            chat_id=AUTH_CHANNEL,
            user_id=message.from_user.id
        )
        return True
    except UserNotParticipant:
        btn = [
                [
                InlineKeyboardButton("🍿ᴊᴏɪɴ ᴏᴜʀ ʙᴀᴄᴋ-ᴜᴘ ᴄʜᴀɴɴᴇʟ🍿", url=link.invite_link)
            ]
        ]
        if file_id != False:
            btn.append([InlineKeyboardButton("🔄 𝗧𝗥𝗬 𝗔𝗚𝗔𝗜𝗡 🔄", callback_data=f"{mode}#{file_id}")])
        else:
            pass

        await message.reply(
            text="♦️ **READ THIS INSTRUCTION** ♦️\n\n🗣 __ഗ്രൂപ്പിൽ ചോദിക്കുന്ന സിനിമകൾ നിങ്ങൾക്ക് ലഭിക്കണം എന്നുണ്ടെങ്കിൽ നിങ്ങൾ താഴെ കൊടുത്തിട്ടുള്ള ചാനലിൽ ജോയിൻ ചെയ്യണം. ജോയിൻ ചെയ്ത ശേഷം വീണ്ടും ഗ്രൂപ്പിൽ പോയി ആ ബട്ടനിൽ അമർത്തിയാൽ നിങ്ങൾക്ക് ഞാൻ ആ സിനിമ പ്രൈവറ്റ് ആയി അയച്ചു തരുന്നതാണ്..__😍\n\n🗣 __In Order To Get The Movies Requested By You in Our Groups, You Will Have To Click On '🍿ᴊᴏɪɴ ᴏᴜʀ ʙᴀᴄᴋ-ᴜᴘ ᴄʜᴀɴɴᴇʟ🍿' First. After That, Try Accessing That Movie Again From Our Group Or Click 🔄 𝗧𝗥𝗬 𝗔𝗚𝗔𝗜𝗡 🔄 Button. I'll Send You That Movie Privately__ 🙈 \n\n👇 **JOIN THIS CHANNEL & TRY** 👇",
            reply_markup=InlineKeyboardMarkup(btn),
            parse_mode=enums.ParseMode.MARKDOWN
        )
        return False
