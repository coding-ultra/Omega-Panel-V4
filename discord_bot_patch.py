# SQLite Discord Admin Patch

from dotenv import load_dotenv
load_dotenv()

DISCORD_BOT_TOKEN=os.getenv('DISCORD_BOT_TOKEN','').strip()
MAIN_ADMIN_ID=str(os.getenv('MAIN_ADMIN_ID','')).strip()

def get_setting(key, default=''):
    conn=get_db()
    try:
        row=conn.execute('SELECT value FROM settings WHERE key=?',(key,)).fetchone()
        return row['value'] if row else default
    finally:
        conn.close()

def set_setting(key,value):
    conn=get_db()
    try:
        conn.execute('INSERT INTO settings(key,value) VALUES(?,?) ON CONFLICT(key) DO UPDATE SET value=excluded.value',(key,str(value)))
        conn.commit()
    finally:
        conn.close()

def is_bot_admin():
    async def predicate(interaction):
        uid=str(interaction.user.id)
        if uid==MAIN_ADMIN_ID:
            return True
        admins=[x.strip() for x in get_setting('bot_extra_admins','').split(',') if x.strip()]
        if uid in admins:
            return True
        await interaction.response.send_message('❌ Access Denied. You are not a bot admin.',ephemeral=True)
        return False
    return app_commands.check(predicate)
