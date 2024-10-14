import openai
from typing import List
import os

from seaborn.external.appdirs import system

openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_book_recommendations(user_preferences: dict) -> List[str]:
    prompt = f"""
    Based on the following user preferences, recommend 30 book titles that the user might enjoy. Only provide the titles, separated by commas.

    User Preferences:
    Favorite Book: {user_preferences.get('favorite_book', 'N/A')}
    Favorite Authors: {', '.join(user_preferences.get('favorite_authors', []))}
    Preferred Genres: {', '.join(user_preferences.get('preferred_genres', []))}
    Themes of Interest: {', '.join(user_preferences.get('themes_of_interest', []))}
    Reading Level: {user_preferences.get('reading_level', 'N/A')}

    Recommended Book Titles:
    """
    print(prompt)
    # response = openai.Completion.create(
    #     engine="text-davinci-002",
    #     prompt=prompt,
    #     max_tokens=200,
    #     n=1,
    #     stop=None,
    #     temperature=0.7,
    # )

    titles = "The Hobbit, The Silmarillion, The Wheel of Time, The Name of the Wind, The Way of Kings, A Song of Ice and Fire, Mistborn: The Final Empire, The Once and Future King, The Dark Tower, The First Law Trilogy, The Earthsea Cycle, The Broken Empire Trilogy, The Lies of Locke Lamora, The Dragonbone Chair, The Sword of Shannara, The Belgariad, The Riftwar Saga, The Malazan Book of the Fallen, The Black Company, The Stormlight Archive, The Priory of the Orange Tree, The Farseer Trilogy, The Chronicles of Prydain, The Chronicles of Narnia, The Elric Saga, Gardens of the Moon, The Magicians, The Deed of Paksenarrion, The Inheritance Cycle, The Riddle-Master Trilogy"
    titles = titles.strip().split(',')
    return [title.strip() for title in titles]

    # titles = response.choices[0].text.strip().split(',')
    # return [title.strip() for title in titles]