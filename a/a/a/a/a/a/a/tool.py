import os
import asyncio
import shutil
from telethon.sync import TelegramClient
from telethon import functions, types, errors

# cfgg
API_ID = 26152851
API_HASH = '160aceff0bc4565f0ca9f5d1e24e17a1'
SESSIONS_DIR = 'sessions'
DELAY = 2

if not os.path.exists(SESSIONS_DIR):
    os.makedirs(SESSIONS_DIR)


# def get_sessions():
#     return [s for s in os.listdir(SESSIONS_DIR) if ('.session')]
#

def get_sessions():
    return [s for s in os.listdir(SESSIONS_DIR) if s.endswith('.session')]


async def join_logic(client, target):
    try:
        if "t.me/joinchat/" in target or "t.me/+" in target:
            invite_hash = target.split('/')[-1].replace('+', '')
            await client(functions.messages.ImportChatInviteRequest(hash=invite_hash))
        else:
            target_clean = target.replace("https://t.me/", "").replace("@", "").split('/')[0]
            await client(functions.channels.JoinChannelRequest(channel=target_clean))
        return True
    except errors.FloodWaitError as e:
        print(f"⚠ flood-wait: {e.seconds} сек.")
    except Exception as e:
        print(f"❌ Error: {e}")
    return False


# async def mass_join():
#     target = input("Введите ссылку")
#     sessions = get_sessions()
#         async with TelegramClient(path, API_ID, API_HASH) as client:
#             print(f" {s}: попытка входа...")
#             await join_logic(client, target)
#             await asyncio.sleep(DELAY)

async def mass_join():
    target = input("Введите ссылку на чат: ")
    sessions = get_sessions()
    for s in sessions:
        path = os.path.join(SESSIONS_DIR, s)
        async with TelegramClient(path, API_ID, API_HASH) as client:
            print(f"User {s}: попытка входа...")
            await join_logic(client, target)
            await asyncio.sleep(DELAY)


async def mass_spam():
    target = input("Введите ссылку/юзернейм чата: ")
    message = input("Введите текст сообщения: ")
    try:
        count = int(input("Сколько раз отправить сообщение с каждого аккаунта? "))
    except ValueError:
        print("❌ Ошибка: введите число.")
        return

    sessions = get_sessions()

    for i in range(count):
        print(f"\n--- Отправка №{i + 1} ---")
        for s in sessions:
            path = os.path.join(SESSIONS_DIR, s)
            try:
                async with TelegramClient(path, API_ID, API_HASH) as client:
                    await join_logic(client, target)

                    await client.send_message(target, message)
                    print(f"✅ {s}: Сообщение отправлено")
            except Exception as e:
                print(f"❌ {s}: Ошибка отправки: {e}")

            await asyncio.sleep(DELAY)

        if i < count - 1:
            print(f"Ожидание перед следующим кругом...")


async def mass_report():
    msg_link = input("Введите ссылку на сообщение (https://t.me/chat/allahakbar2323): ")
    try:
        parts = msg_link.replace("https://t.me/", "").split('/')
        channel_name = parts[0]
        msg_id = int(parts[1])
    except:
        print("error not valid libnk")
        return

    sessions = get_sessions()
    for s in sessions:
        path = os.path.join(SESSIONS_DIR, s)
        async with TelegramClient(path, API_ID, API_HASH) as client:
            try:
                peer = await client.get_input_entity(channel_name)
                await client(functions.messages.ReportRequest(
                    peer=peer,
                    id=[msg_id],
                    reason=types.InputReportReasonSpam(),
                    message="Mass reporting"
                ))
                print(f"✅ {s}: Жалоба подана")
            except Exception as e:
                print(f"❌ {s}: {e}")
            await asyncio.sleep(DELAY)



def edit_session_menu():
    sessions = get_sessions()
    if not sessions: print("Нет сессий."); return

    for i, s in enumerate(sessions, 1): print(f"{i}. {s}")
    try:
        idx = int(input("Выберите сессию для редактирования: ")) - 1
        current_session = sessions[idx]
    except:
        return

    print(f"\nМеню для {current_session}:")
    print("1. Edit name session\n2. Check session\n3. Back")

    choice = input(">> ")
    if choice == "1":
        new_name = input("Новое имя: ")
        os.rename(os.path.join(SESSIONS_DIR, current_session),
                  os.path.join(SESSIONS_DIR, f"{new_name}.session"))
    elif choice == "2":
        async def check():
            async with TelegramClient(os.path.join(SESSIONS_DIR, current_session), API_ID, API_HASH) as c:
                me = await c.get_me()
                print(f"Valid: {me.username}")

        asyncio.run(check())


# фрозе симба самбок 2
# def action_panel():
#   while True:

def action_panel():
    while True:
        print("\n--- ACTION PANEL ---")
        print("1. Mass Join\n2. Mass Spam\n3. Mass Report\n4. Return to Main Menu")
        c = input(">> ")
        if c == "1":
            asyncio.run(mass_join())
        elif c == "2":
            asyncio.run(mass_spam())
        elif c == "3":
            asyncio.run(mass_report())
        elif c == "4":
            break


def session_manager_panel():
    while True:
        print("\n--- SESSION SETTINGS ---")
        print("1. Add Session\n2. Delete Session\n3. Edit Session\n4. ENTER MAIN MENU (Actions)\n5. Exit")
        c = input(">> ")
        if c == "1":
            name = input("Имя сессии: ")
            client = TelegramClient(os.path.join(SESSIONS_DIR, name), API_ID, API_HASH)
            client.start()
            client.disconnect()
        elif c == "2":
            sessions = get_sessions()
            for i, s in enumerate(sessions, 1): print(f"{i}. {s}")
            idx = int(input("Удалить №: ")) - 1
            os.remove(os.path.join(SESSIONS_DIR, sessions[idx]))
        elif c == "3":
            edit_session_menu()
        elif c == "4":
            action_panel()
        elif c == "5":
            exit()


if __name__ == "__main__":
    session_manager_panel()
