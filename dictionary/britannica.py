# britannica.py
'''
Module for Britannica Dictionary

'''

from dictionary.tools import get_soup

DOMAIN = 'https://www.britannica.com'


def get_entries(word):
    '''
    Get related entries for a word in Britannica Dictionary

    Args:
        word (str): Word to search for

    Returns:
        list: List of dictionaries containing the text and link of each entry, or an empty list if no entries are found
    '''
    url = f"{DOMAIN}/dictionary/{word}"
    soup = get_soup(url)
    if not soup:
        return []
    entries = soup.find('ul', class_='o_list')

    if entries:
        return [{'text': entry.find('a').get_text(strip=True), 'link': DOMAIN + entry.find('a')['href']} for entry in entries.find_all('li')]
    else:
        return []

def get_total_entries(word):
    '''
    Get total number of entries for a word in Britannica Dictionary

    Args:
        word (str): Word to search for

    Returns:
        int: Total number of entries for the word
    '''
    return len(get_entries(word))


def get_word_of_the_day():
    '''
    Get the word of the day from Britannica Dictionary

    Returns:
        dict: Dictionary containing the word, part of speech, image, and meaning information, or None if not found
    '''
    url = f"{DOMAIN}/dictionary/eb/word-of-the-day"
    soup = get_soup(url)
    
    if not soup:
        return None

    word_container = soup.find('div', class_='hw_d box_sizing ld_xs_hidden')
    image_container = soup.find('div', class_='wod_img_act')
    meaning_container = soup.find('div', class_='midbs')  # Container for meaning information

    word_info = {}

    if word_container:
        word_text = word_container.find('span', class_='hw_txt').get_text(strip=True)
        part_of_speech = word_container.find('span', class_='fl').get_text(strip=True)
        word_info['word'] = f"{word_text} ({part_of_speech})"
    else:
        return None

    if image_container:
        image = image_container.find('img')
        if image:
            word_info['image'] = {'src': image.get('src', ''), 'alt': image.get('alt', '')}

    if meaning_container:
        meanings = []
        meaning_blocks = meaning_container.find_all('div', class_='midb')
        for block in meaning_blocks:
            definition = block.find('div', class_='midbt').find('p').get_text(strip=False)
            examples = [example.get_text(strip=False) for example in block.find_all('li', class_='vi')]
            meaning = { 'definition': definition, 'examples': examples}
            meanings.append(meaning)
    word_info['meanings'] = meanings


    return word_info


def get_parts(word):
    '''
    Get the parts of speech for a given word from the Britannica Dictionary.

    Args:
        word (str): The word to fetch parts of speech for.

    Returns:
        list: List of strings, with each string containing the headword and its part of speech.
    '''
    url = f"{DOMAIN}/dictionary/{word}"
    soup = get_soup(url)
    if not soup:
        return None

    entries = soup.find_all('div', class_='hw_d')
    if not entries:
        return None

    parts_of_speech = []

    for entry in entries:
        headword = entry.find('span', class_='hw_txt').get_text(strip=True)
        part_of_speech = entry.find('span', class_='fl').get_text(strip=True)

        parts_of_speech.append(f"{headword} ({part_of_speech})")

    return parts_of_speech


def get_definitions(word):
    '''
    Extracts the definitions and examples from the Britannica Dictionary for a given word.

    Args:
        word (str): The word to fetch definitions for.

    Returns:
        list: List of dictionaries, where each dictionary contains a meaning and its examples.
              Returns None if no definitions are found or if sense/examples are not found.
    '''
    url = f"{DOMAIN}/dictionary/{word}"
    soup = get_soup(url)
    if not soup:
        return None

    sblocks = soup.find_all('div', class_='sblocks')
    definitions_with_examples = []

    for sblock in sblocks:
        definition_blocks = sblock.find_all('div', class_='sblock_c')
        for block in definition_blocks:
            sense = block.find_all('div', class_='sense')
            for s in sense: 
                definitions = s.find_all('span', class_='def_text')
                examples = s.find_all('li', class_='vi')
                
                if definitions and examples:
                    for definition, example in zip(definitions, examples):
                        meaning = definition.get_text(strip=True)
                        example_list = [example.get_text(strip=True) for example in examples]
                        definitions_with_examples.append({'meaning': meaning, 'examples': example_list})
                elif definitions:
                    for definition in definitions:
                        meaning = definition.get_text(strip=True)
                        definitions_with_examples.append({'meaning': meaning, 'examples':[]})

    return definitions_with_examples