from lib.furina import Furina, isPrivate
import requests

async def Wikipedia(msg, match, client):
    try:
        if not msg.get_args():
            await msg.reply("Provide search term.\nExample: !wiki who is iron man")
            return
        query = " ".join(msg.get_args())
        search_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{query.replace(' ', '_')}"
        res = requests.get(search_url)
        if res.status_code == 200:
            data = res.json()
            title = data.get('title', 'No title')
            extract = data.get('extract', 'No summary available')
            page_url = data.get('content_urls', {}).get('desktop', {}).get('page', '')
            wiki_info = f"**{title}**\n\n{extract[:500]}..."
            if page_url:
                wiki_info += f"\n\nRead more: {page_url}"
            await msg.reply(wiki_info)
        else:
            await msg.reply("Article not found.")
    except Exception as e:
        await msg.reply(f"Error: {e}")

async def Weather(msg, match, client):
    try:
        if not msg.get_args():
            await msg.reply("Provide a city name. Example: `!weather kerala`")
            return

        city = " ".join(msg.get_args())
        res = requests.get(f"https://ironman.koyeb.app/api/weather?place={city}")

        if res.status_code != 200:
            await msg.reply(f"Could not get weather for `{city}`.")
            return

        data = res.json()
        main = data.get("weather", [{}])[0].get("main", "N/A")
        description = data.get("weather", [{}])[0].get("description", "N/A")
        temp = data.get("main", {}).get("temp", "N/A")
        feels_like = data.get("main", {}).get("feels_like", "N/A")
        humidity = data.get("main", {}).get("humidity", "N/A")
        wind_speed = data.get("wind", {}).get("speed", "N/A")

        weather_info = (
            f"**Weather in {data.get('name', city.title())}**\n"
            f"Condition: {main} ({description})\n"
            f"Temperature: {temp}°C (Feels like {feels_like}°C)\n"
            f"Humidity: {humidity}%\n"
            f"Wind Speed: {wind_speed} m/s"
        )

        await msg.reply(weather_info)

    except Exception as e:
        await msg.reply(f"Error: {e}")

Furina({
    "pattern": r"wiki\s+(.+)",
    "fromMe": isPrivate,
    "desc": "Search Wikipedia",
    "type": "search"
}, Wikipedia)

Furina({
    "pattern": r"weather\s+(.+)",
    "fromMe": isPrivate,
    "desc": "Get weather information",
    "type": "search"
}, Weather)
