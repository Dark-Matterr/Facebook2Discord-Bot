# Facebook to Discord Bot
Using private servers or embedded computer such as Raspberry Pi, you can automate to send latest desired Facebook profiles 
or pages to your Discord channel using this script.

# Setup
- Clone this repository: `https://github.com/Dark-Matterr/Facebook2Discord-Bot.git`
- Create a conda enviroment and install the required packages: `pip install -r requirements.txt`
- Edit the following variables in the facebook.py
    * `PAGE_NAME`
    * `COOKIE_FILE`
    * `LOG_JSON`
    * `BOT_TOKEN`
    * `BOT_NAME`
    * `BOT_CHANNEL_ID`
    * `BOT_CHECK_DELAY_SEC`

- Create a file `cookiefile.txt` that contains your facebook cookie in the same directory. Use [Get Cookies.txt (Chrome)](https://chrome.google.com/webstore/detail/get-cookiestxt/bgaddhkoddajcdgocldbbfleckgcbcid) to generate a cookie txt file.
