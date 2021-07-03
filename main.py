"""
Telegram-MeerkatBot V1.0 (Jul 1 20201)
More Info & Setup Tutorial: git.io/Jnx9P
"""

import os
from telegram.ext import Updater, CommandHandler , MessageHandler , Filters , CallbackContext
import telegram
import feedparser
import datetime
import pytz

print('bot running at ' + str(datetime.datetime.today()))

#At This Section We Define 'updater' using our Telegram Bot API-KEY
updater = Updater('Enter Your API-KEY Here!')
dispatcher = updater.dispatcher

#At This Section We Define Some Basic Command Handlers, Including /start & /about and We Also Create Our Database
def start(update , context):
    file = open('%i.txt' %update.effective_chat.id, 'a')
    file.close()
    file = open('%i_url.txt' %update.effective_chat.id, 'a')
    file.close()
    file = open('users_list.txt' , 'r')
    users_list_list = []
    for line in file:
        users_list_list.append(line[:-1])
    file.close()
    
    

    file = open('users_list.txt' , 'a')
    if str(update.effective_chat.id) in users_list_list:
      pass
    elif str(update.effective_chat.id) not in users_list_list:
        file.write(str(update.effective_chat.id) + '\n')

    file.close()

    keyboard = [
        [telegram.KeyboardButton('/add ➕ Follow a New Website'),
        telegram.KeyboardButton('/mylist ⚙️ View Your Websites List')],
        ]
    kb_markup = telegram.ReplyKeyboardMarkup(keyboard)
    context.bot.send_message(chat_id=update.effective_chat.id, text="""

🙌 Welcome to Meerkat RSS Reader!

🤖 Meerkat's a Feed-reader Robot;
Consider Meerkat as Your News Assistant... When One of Your Previously Subscribed Websites Gets Updated, We Immediately Send You the Link to Those Updates.

#️⃣ Use Bot's Configuration Buttons to Manage Your Own List of Subscribed News Centers.

🌐 Once You Add a Site, We Handle the Rest; Looking for the Latest Updates on Your Subscribed Websites.

🕊 And of Course Meerkat's an Open-source Robot. So if You'd Like to Know More About the Functionality of the Robot... Or Just Contact Bot Developers, Use /about Command!

""" , reply_markup=kb_markup)

def about(update , context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="""

📡 Early Version - Under Development
⚙️ Beta V1.0

🤖 Developed By:
@JoiFoi & @mac_mr

📧 <a href='mailto:JoiFoi@Outlook.Com'>JoiFoi@Outlook.Com</a>

🏭 Detailed Guide and Source Code on:
<a href='http://git.io/JcZoZ'>🕊 Meerkat Github Page</a>

""" , parse_mode = 'HTML' , disable_web_page_preview = True)

def siteslist(update , context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="""
    
🌎 Worldwide Political News Centers

🇺🇸 The New York Times /Sub01
🇺🇸 FOX News /Sub02
🇺🇸 Los Angles Times /Sub03
🇺🇸 The Washington Times /Sub04
🇬🇧 BBC World News /Sub05
🇮🇷 Isna News /Sub06
🇮🇷 Mehrnews /Sub07
🇮🇷 Tasnim News /Sub08

📡 Technology News

🇺🇸 IGN Tech Articles /Sub09
🇺🇸 CNET News /Sub10
🇺🇸 The Verge Software News /Sub11
🇺🇸 The New York Times Tech Center /Sub12
🇮🇷 Zoomit /Sub13
🇮🇷 Digiato /Sub14

🎞 Movies And TV Shows News

🇺🇸 Cinema Blend /Sub15
🇺🇸 MovieWeb /Sub16

🎸 Music & Entertainment News

🇺🇸 All Access /Sub17
🇺🇸 Pitchfork /Sub18
🇺🇸 All But Forgotten Oldies /Sub19  

""")

sites = {
'/Sub01' :'https://rss.nytimes.com/services/xml/rss/nyt/World.xml', #The New York Times
'/Sub02' :'http://feeds.foxnews.com/foxnews/world', #FOX News
'/Sub03' :'https://www.latimes.com/world-nation/rss2.0.xml#nt=1col-7030col1', #Los Angles Times
'/Sub04' :'https://www.washingtontimes.com/rss/headlines/news/world/', #4. The Washington Times
'/Sub05' :'http://feeds.bbci.co.uk/news/world/rss.xml', #BBC World News
'/Sub06' :'https://www.isna.ir/rss/tp/161', #Isna News
'/Sub07' :'https://www.mehrnews.com/rss/tp/7', #Mehrnews
'/Sub08' :'https://www.tasnimnews.com/fa/rss/feed/0/7/1/%D8%B3%DB%8C%D8%A7%D8%B3%DB%8C', #Tasnim News
'/Sub09' :'http://feeds.feedburner.com/ign/tech-articles', #IGN Tech Articles
'/Sub10' :'https://www.cnet.com/rss/news/', #CNET News
'/Sub11' :'https://www.theverge.com/apps/rss/index.xml', #The Verge Software News
'/Sub12' :'https://rss.nytimes.com/services/xml/rss/nyt/Technology.xml', #The New York Times Tech Center
'/Sub13' :'http://feeds.zoomit.ir/zoomit-it', #Zoomit
'/Sub14' :'https://digiato.com/feed', #Digiato
'/Sub15' :'https://www.cinemablend.com/rss_news_movies.xml', #Cinema Blend
'/Sub16' :'https://movieweb.com/rss/all-news/', #MovieWeb
'/Sub17' :'https://www.allaccess.com/feed/net-news/format/top40-mainstream.rss', #All Access
'/Sub18' :'https://pitchfork.com/feed/feed-news/rss', #Pitchfork
'/Sub19':'https://www.allbutforgottenoldies.net/rss-feeds/allbutforgottenoldies.xml' #All But Forgotten Oldies
}

key_list = list(sites.keys())
val_list = list(sites.values())


def check_message(update: telegram.Update, context: CallbackContext):
    
    try:
        if update.message.text not in sites:
            context.bot.send_message(chat_id=update.effective_chat.id, text=
            "✖️ That's Not a Valid Command!\n\n"
            "📖 Some of Our Valid Commands:\n"
            "+ Use /add to Follow a New Website!\n"
            "+ Use /mylist to Manage Your Following Websites!\n")
        
        elif update.message.text in sites:
            file = open('%i.txt' %update.effective_chat.id, 'r')
            templist = []
            templist_count = 0
            for line in file:
                templist.append(key_list[val_list.index(line[:-1])])
                templist_count += 1
            file.close()
            
            if update.message.text in templist:
                context.bot.send_message(chat_id=update.effective_chat.id, text=
                "✖️ Invalid Request!\n"
                "😀 You Already Follow That Website!"
                )

            elif update.message.text not in templist:
              if templist_count < 3:
                file = open('%i.txt' %update.effective_chat.id, 'a')
                file.write(str(sites.get(update.message.text)) + '\n')
                file.close()
                context.bot.send_message(chat_id=update.effective_chat.id, text=
                "✅ Done!\n\n"
                "🔎 Once This Website Updates, We Send You The New Post Immediately!"
                " Use /mylist If You'd Like To Edit Your List."
                )
              elif templist_count <= 3:
                context.bot.send_message(chat_id=update.effective_chat.id, text=
                "✖️ Invalid Request!\n"
                "📂 Your List Is Already Full (Max = 3)"
                )

    except:
        pass


def userlist(update , context):
    file = open('%i.txt' %update.effective_chat.id, 'r')
    userlinkslist = ''
    count = 0
    
    for line in file:
        count += 1
        userlinkslist = userlinkslist + str(count) + '. ' + str(line)

    if count != 0:
        context.bot.send_message(chat_id=update.effective_chat.id, text=
        "📡 You Are Currently Subscribed To The Following List:\n\n"
        "Subscription Count: " + str(count) + "\n" +
        userlinkslist +
        "\n❌ Use /wipe To Completely Clear Your List;"
        " Like It Never Existed..."
        )
    elif count == 0:
        context.bot.send_message(chat_id=update.effective_chat.id, text=
        "🙄 Your List is Empty!\n\n"
        "➕ Use /add to Follow a New Website."
        )

def wipe(update , context):
    os.remove('%i.txt' %update.effective_chat.id)
    file = open('%i.txt' %update.effective_chat.id, 'a')
    file.close()
    context.bot.send_message(chat_id=update.effective_chat.id, text=
    "✔️ Done! Everything Cleared...\n"
    "➕ Use /add To Follow New Websites"
    )

def main(context: CallbackContext):
    users = open('users_list.txt' , 'r')
    userlist = []
    for user in users:
        userlist.append(int(user[:-1]))
    users.close()

    for user in userlist:
        user_follows = open('%i.txt' %user, 'r')
        user_sent = open('%i_url.txt' %user, 'r')
        user_follows_list = []
        user_sent_list = []
        updates = []
        
        for line in user_follows:
            user_follows_list.append(line[:-1])
        user_follows.close()
        

        for line in user_sent:
            user_sent_list.append(line[:-1])
        
        
        user_sent.close()
        
        for line in user_follows_list:
            d = feedparser.parse(line)
            for i in d['entries']:
                updates.append(i['link'])
                
        
        


        for update in updates:
            if update not in user_sent_list:
                user_sent = open('%i_url.txt' %user, 'a')
                context.bot.send_message(chat_id=user, text=str(update))
                user_sent.write(str(update) + '\n')
            elif update in user_sent_list:
                pass
        
        user_sent.close()

#And This Section Configures All Your Message & Command Handlers
dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('about', about))
dispatcher.add_handler(CommandHandler('add', siteslist))
dispatcher.add_handler(CommandHandler('mylist', userlist))
dispatcher.add_handler(CommandHandler('wipe', wipe))
dispatcher.add_handler(MessageHandler(Filters.text , check_message))

#Well On This Section We Setup main() To Get Runned Every Two Minutes
hourlist = []
minlist = []

for hour in range(0 , 24):
    hourlist.append(hour)
for min in range(0 , 60):
    if min%2 == 0:
        minlist.append(min)

j = updater.job_queue

for hours in hourlist:
    for mins in minlist:
        job_daily = j.run_daily(main, days=(0, 1, 2, 3, 4, 5, 6), time=datetime.time(hour=hours, minute=mins, tzinfo=pytz.timezone('Asia/Tehran')))

updater.start_polling()
