import urllib
import time
import shutil
from requests import get
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np


# from the accent.gmu website, pass in list of languages to scrape mp3 files and save them to disk
def mp3getter(lst):
    links = []
    for j in range(len(lst)):
        for i in range(1,lst[j][1]+1):
                try:
                    print(" fetching record ", i, " for language ", j)
                    # urllib.request.urlretrieve("http://accent.gmu.edu/soundtracks/{0}{1}.mp3".format(lst[j][0], i), '../sounds/{0}{1}.mp3'.format(lst[j][0], i))
                    # print("http://accent.gmu.edu/soundtracks/{0}{1}.mp3".format(lst[j][0], i))
                    with open('links.txt', 'a') as f:
                        f.writelines("http://accent.gmu.edu/soundtracks/{0}{1}.mp3".format(lst[j][0], i))
                        f.writelines('\n')
                except:
                    time.sleep(2)
        

# from list of languages, return urls of each language landing page
def lang_pages(lst):
    urls=[]
    for lang in lst:
        urls.append('http://accent.gmu.edu/browse_language.php?function=find&language={}'.format(lang))
    return urls

#output:
#
# ['http://accent.gmu.edu/browse_language.php?function=find&language=amharic',
#  'http://accent.gmu.edu/browse_language.php?function=find&language=arabic',
#  'http://accent.gmu.edu/browse_language.php?function=find&language=bengali',
#  'http://accent.gmu.edu/browse_language.php?function=find&language=bulgarian',
#  'http://accent.gmu.edu/browse_language.php?function=find&language=cantonese',
#  'http://accent.gmu.edu/browse_language.php?function=find&language=dutch',
#  'http://accent.gmu.edu/browse_language.php?function=find&language=english',
#  'http://accent.gmu.edu/browse_language.php?function=find&language=farsi',
#  'http://accent.gmu.edu/browse_language.php?function=find&language=french',
#  'http://accent.gmu.edu/browse_language.php?function=find&language=german',
#  'http://accent.gmu.edu/browse_language.php?function=find&language=greek',
#  'http://accent.gmu.edu/browse_language.php?function=find&language=hindi',
#  'http://accent.gmu.edu/browse_language.php?function=find&language=italian',
#  'http://accent.gmu.edu/browse_language.php?function=find&language=japanese',
#  'http://accent.gmu.edu/browse_language.php?function=find&language=korean',
#  'http://accent.gmu.edu/browse_language.php?function=find&language=kurdish',
#  'http://accent.gmu.edu/browse_language.php?function=find&language=macedonian',
#  'http://accent.gmu.edu/browse_language.php?function=find&language=mandarin',
#  'http://accent.gmu.edu/browse_language.php?function=find&language=miskito',
#  'http://accent.gmu.edu/browse_language.php?function=find&language=nepali',
#  'http://accent.gmu.edu/browse_language.php?function=find&language=pashto',
#  'http://accent.gmu.edu/browse_language.php?function=find&language=polish',
#  'http://accent.gmu.edu/browse_language.php?function=find&language=portuguese',
#  'http://accent.gmu.edu/browse_language.php?function=find&language=punjabi',
#  'http://accent.gmu.edu/browse_language.php?function=find&language=romanian',
#  'http://accent.gmu.edu/browse_language.php?function=find&language=russian',
#  'http://accent.gmu.edu/browse_language.php?function=find&language=serbian',
#  'http://accent.gmu.edu/browse_language.php?function=find&language=spanish',
#  'http://accent.gmu.edu/browse_language.php?function=find&language=swedish',
#  'http://accent.gmu.edu/browse_language.php?function=find&language=tagalog',
#  'http://accent.gmu.edu/browse_language.php?function=find&language=thai',
#  'http://accent.gmu.edu/browse_language.php?function=find&language=turkish',
#  'http://accent.gmu.edu/browse_language.php?function=find&language=ukrainian',
#  'http://accent.gmu.edu/browse_language.php?function=find&language=urdu',
#  'http://accent.gmu.edu/browse_language.php?function=find&language=vietnamese']

# from http://accent.gmu.edu/browse_language.php, return list of languages
def get_languages():
    url = "http://accent.gmu.edu/browse_language.php"
    html = get(url)
    soup = BeautifulSoup(html.content, 'html.parser')
    languages = []
    language_lists = soup.findAll('ul', attrs={'class': 'languagelist'})
    for ul in language_lists:
        for li in ul.findAll('li'):
            languages.append(li.text)
    return languages
    
# from list of languages, return list of urls
def get_language_urls(lst):
    urls = []
    for language in lst:
        urls.append('http://accent.gmu.edu/browse_language.php?function=find&language=' + language)
    return urls

# from language, get the number of speakers of that language
def get_num(language):
    url = 'http://accent.gmu.edu/browse_language.php?function=find&language=' + language
    try:
        html = get(url)
        soup = BeautifulSoup(html.content, 'html.parser')
        test = soup.find_all('div', attrs={'class': 'content'})
        num = int(test[0].find('h5').text.split()[2])
    except:
        num = 0
    return num
    
# from list of languages, return list of tuples (LANGUAGE, LANGUAGE_NUM_SPEAKERS) for mp3getter, ignoring languages
# with 0 speakers
def get_formatted_languages(languages):
    formatted_languages = []
    for language in languages:
        print("processing language: ", language)
        num = get_num(language)
        if num != 0:
            formatted_languages.append((language,num))
    return formatted_languages
    
# from each language whose url is contained in the above list, save the number of speakers of that language to a list
def get_nums(lst):
    nums = []
    for url in lst:
        html = get(url)
        soup = BeautifulSoup(html.content, 'html.parser')
        test = soup.find_all('div', attrs={'class': 'content'})
        nums.append(int(test[0].find('h5').text.split()[2]))
    return nums

def get_speaker_info(start, stop):
    '''
    Inputs: two integers, corresponding to min and max speaker id number per language
    Outputs: Pandas Dataframe containing speaker filename, birthplace, native_language, age, sex, age_onset of English
    '''

    user_data = []
    for num in range(start,stop):
        info = {'speakerid': num, 'filename': 0, 'birthplace':1, 'native_language': 2, 'age':3, 'sex':4, 'age_onset':5}
        url = "http://accent.gmu.edu/browse_language.php?function=detail&speakerid={}".format(num)
        html = get(url)
        soup = BeautifulSoup(html.content, 'html.parser')
        body = soup.find_all('div', attrs={'class': 'content'})
        try:
            info['filename']=str(body[0].find('h5').text.split()[0])
            bio_bar = soup.find_all('ul', attrs={'class':'bio'})
            info['birthplace'] = str(bio_bar[0].find_all('li')[0].text)[13:-6]
            info['native_language'] = str(bio_bar[0].find_all('li')[1].text.split()[2])
            info['age'] = float(bio_bar[0].find_all('li')[3].text.split()[2].strip(','))
            info['sex'] = str(bio_bar[0].find_all('li')[3].text.split()[3].strip())
            info['age_onset'] = float(bio_bar[0].find_all('li')[4].text.split()[4].strip())
            user_data.append(info)
        except:
            info['filename'] = ''
            info['birthplace'] = ''
            info['native_language'] = ''
            info['age'] = ''
            info['sex'] = ''
            info['age_onset'] = ''
            user_data.append(info)
        df = pd.DataFrame(user_data)
        df.to_csv('speaker_info_{}.csv'.format(stop))
    return df

# copy files from one list of wav files to a specified location
def copy_files(lst, path):
    for filename in lst:
        shutil.copy2('{}.wav'.format(filename), '{}/{}.wav'.format(path, filename))


if __name__ == '__main__':
    # lst = get_languages()
    # print(len(lst))
    # lert = get_formatted_languages(lst)
    # print(lert)
    lert = [('afrikaans', 6), ('agni', 1), ('akan', 13), ('albanian', 11), ('amazigh', 2), ('american sign language', 2), ('amharic', 23), ('anyin', 1), ('arabic', 153), ('armenian', 8), ('azerbaijani', 5), ('azerbaijani, south', 2), ('azeri turk', 2), ('bafang', 2), ('baga', 1), ('bahasa indonesia', 12), ('bai', 1), ('balant', 1), ('balanta ganja', 1), ('bamanankan', 5), ('bambara', 5), ('bamun', 1), ('bangla', 1), ('bari', 2), ('basque', 2), ('bavarian', 2), ('belarusan', 3), ('bengali', 19), ('bosnian', 12), ('bulgarian', 19), ('burmese', 2), ('cameroon creole english', 1), ('cantonese', 31), ('carolinian', 1), ('catalan', 5), ('cebuano', 1), ('chaldean', 2), ('chaldean neo aramaic', 1), ('chamorro', 1), ('chichewa', 1), ('chin, mizo', 1), ('chinese', 167), ('chittagonian', 1), ('croatian', 8), ('danish', 9), ('dari', 8), ('dholuo', 2), ('dinka', 1), ('djola', 1), ('dutch', 50), ('eastern farsi', 2), ('ebira', 1), ('edo', 1), ('english', 618), ('estonian', 17), ('ewe', 3), ('fang', 1), ('fanti', 3), ('faroese', 1), ('farsi', 30), ('fataluku', 1), ('fefe', 1), ('fijian', 3), ('filipino', 2), ('finnish', 15), ('flemish', 5), ('french', 69), ('frisian', 1), ('fulani', 1), ('fulfulde adamawa', 1), ('ga', 6), ('gan', 1), ('ganda', 3), ('garifuna', 2), ('gedeo', 1), ('georgian', 5), ('german', 38), ('greek', 15), ('gujarati', 16), ('gusii', 2), ('hadiyya', 2), ('hainanese', 1), ('haitian creole french', 7), ('hakka', 3), ('hausa', 10), ("hawai'i creole english", 2), ("hawai'ian pidgin", 2), ('hebrew', 9), ('hijazi', 17), ('hiligaynon', 2), ('hindi', 31), ('hindi-urdu', 31), ('hindko', 1), ('hmong', 2), ('hmong daw', 2), ('home sign', 1), ('hungarian', 11), ('ibibio', 3), ('icelandic', 3), ('ife', 1), ('igbo', 3), ('ikalanga', 1), ('ilonggo', 2), ('indonesian', 12), ('irish', 1), ('irish gaelic', 1), ('italian', 37), ('jamaican creole english', 4), ('japanese', 34), ('javanese', 1), ('jola', 1), ('kabyle', 1), ('kalanga', 1), ('kamba', 1), ('kambaata', 3), ('kamtok', 1), ('kannada', 9), ('kanuri', 1), ('kazakh', 4), ('kembata', 3), ('khalkha mongol', 8), ('khasonke', 1), ('khmer', 7), ('kikongo', 2), ('kikuyu', 5), ('kinyarwanda', 1), ('kirghiz', 3), ('kirundi', 1), ('kisii', 2), ('kiswahili', 11), ('klao', 1), ('kongo', 2), ('konkani', 3), ('korean', 90), ('krio', 6), ('kru', 1), ('kurdi', 4), ('kurdish', 10), ('kurmanji', 1), ('kyrgyz', 3), ('lamaholot', 1), ('lamotrekese', 1), ('lao', 3), ('latvian', 3), ('liberian english', 2), ('liberian pidgin english', 2), ('lingala', 1), ('lithuanian', 7), ('luba-kasai', 1), ('luganda', 3), ('luo', 3), ('luxembourgeois', 1), ('macedonian', 26), ('malagasy', 1), ('malay', 5), ('malayalam', 7), ('maltese', 2), ('mancagne', 1), ('mandarin', 115), ('mandingo', 1), ('mandingue', 1), ('mandinka', 1), ('maninkakan', 1), ('mankanya', 1), ('manual communication', 1), ('marathi', 9), ('mauritian', 3), ('mende', 3), ('miskito', 11), ('mizo', 1), ('moba', 1), ('mongolian', 9), ('montenegrin', 1), ('moore', 1), ('morisyen', 2), ('mortlockese', 1), ('najdi', 26), ('nama', 1), ('nandi', 1), ('naxi', 1), ('ndebele', 1), ('nepali', 14), ('newar', 1), ('newari', 1), ('ngemba', 2), ('nicaragua creole english', 4), ('northern sotho', 1), ('norwegian', 7), ('nuer', 1), ('nyanja', 1), ('omani arabic', 1), ('oriya', 2), ('oromo', 3), ('ossetic', 1), ('pahari', 2), ('panjabi', 12), ('papiamentu', 2), ('pashto', 10), ('patois', 4), ('persian', 27), ('pidgin english', 1), ('pohnpeian', 1), ('polish', 39), ('poonchi', 1), ('portuguese', 60), ('pulaar', 3), ('punjabi', 12), ('quechua', 2), ('romanian', 23), ('rotuman', 2), ('rundi', 1), ('russian', 76), ('rwanda', 1), ("sa'a", 1), ('sardinian', 1), ('sarua', 1), ('satawalese', 2), ('sepedi', 1), ('serbian', 19), ('serer', 1), ('serer sine', 1), ('sesotho', 1), ('setswana', 2), ('shan', 1), ('shilluk', 1), ('shona', 2), ('sicilian', 1), ('sindhi', 1), ('sinhala', 7), ('sinhalese', 7), ('slovak', 6), ('slovenian', 2), ('somali', 7), ('sotho', 1), ('spanish', 206), ('sunda', 1), ('sundanese', 1), ('susu', 1), ('swahili', 11), ('swedish', 22), ('swiss german', 7), ('sylheti', 1), ('synthesized', 4), ('tagalog', 24), ('taishan', 1), ('taiwanese', 9), ('tajiki', 14), ('tamajeq', 2), ('tamazight', 1), ('tamil', 13), ('tatar', 1), ('telugu', 13), ('temne', 1), ('teochew', 1), ('tetum', 1), ('tetun-dili', 1), ('thai', 20), ('tibetan', 4), ('tigre', 1), ('tigrigna', 9), ('tok pisin', 1), ('tshiluba', 1), ('tswana', 2), ('turkish', 38), ('turkmen', 2), ('twi', 9), ('ukrainian', 11), ('urdu', 25), ('uyghur', 5), ('uzbek', 5), ('vietnamese', 27), ('vlaams', 4), ('voro', 3), ('wali', 1), ('woleaian', 1), ('wolof', 6), ('wu', 3), ('xasonga', 1), ('xiang', 4), ('yakut', 1), ('yapese', 1), ('yiddish', 5), ('yoruba', 5), ('yue', 1), ('zulu', 1)]

    mp3getter(lert)