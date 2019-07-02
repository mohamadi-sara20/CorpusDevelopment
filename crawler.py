import requests
import json, time
import corpus_utils
import re

tags = {
    #'culture': 'سینما نقاشی کتاب تلویزیون فیلم فرهنگ فرهنگی هنر هنرمند شعر شاعر فرهنگی هنری',
    'culture': 'فیلم فرهنگ فرهنگی هنر هنرمند شعر شاعر فرهنگی هنری',
    'sport': 'ورزش ورزشی فیتنس فوتبال والیبال بسکتبال تنیس بدمینتون شنا کاراته تکواندو تیمـملی',
    'politics': 'سیاسی سیاست انتخابات روحانی تظاهرات اعتصاب امریکا رهبر رهبری ارتش سپاه برجام تحریم سرکوب شاه',
    'economy': 'گرانی تورم دلار ارز اجاره فقر گرسنگی اقتصادی بازار مسکن اقتصاد پول قیمت',
    'social': 'اجتماعی تاریخی روزنامه معلمان دانشجو جوان جوانان اعتیاد کارگر جامعه',
    }

seen_ids = set({})
post_count = 0

def is_new(id):
    '''
    Checks if a message is new or has already been seen
    :param id: message id
    :param id type: str
    :rtype: bool
    '''
    if id not in seen_ids:
        return True
    else:
        return False


def make_links(tag, cursor):
    '''
    creates the link to be streamed using each tag in the tag set.
    :param tag: a specific hashtag
    :param tag type: str
    :return: a link
    :rtype: str
    '''
    if not tag:
        raise ValueError('empty input!')
    if not isinstance(tag, type('')):
        raise TypeError('strings accepted only!')
    link = f'https://www.instagram.com/explore/tags/{tag}/?__a=1'
    if cursor:
        link += f'&max_id={cursor}'
    return link


def make_post(new_post, id, just_get_images=False):
    '''
    creates a post in a dictionary format using its text and its id and sending it to the database.
    :param new_post: dictionary
    :param id: str
    :rtype: NoneType
    '''

    try:
        post = new_post['node']['edge_media_to_caption']['edges'][0]['node']['text']
    except:
        return ''

    if post:
        #np = re.sub('[A-Za-z]', '', post)
        #np = re.sub('([\\s,-_.#]*[#_]\\w*)*([\\s,-_.#])*$', ' ', np)
        #np = re.sub('([/،."\'«»؟✒?!,؛;\\\])', ' \g<1> ', np)
        #np = np.replace('_', '')
        #np = np.replace('-', '')
        #np = re.sub('\s{2,}', ' ', np)
        return post




def get_posts(tag, cursor):
    '''
    get the posts containing a specific tag
    :param tag: a specific hashtag
    :return: posts containing a hashtag
    :rtype: list of dictionaries
    '''
    try:
        r_insta = requests.get(make_links(tag, cursor))
        data_arrivals = json.loads(r_insta.text)
        cursor = data_arrivals['graphql']['hashtag']['edge_hashtag_to_media']['page_info']['end_cursor']
        data = data_arrivals['graphql']['hashtag']['edge_hashtag_to_media']['edges']
        time.sleep(1)
        return data, cursor
    except:
        return [], None

def get_insta_posts(tag, subject):
    post_count = 0
    print('CRAWL STARTED: {} - {}'.format(subject, tag))
    path = 'raw-files/{}/'.format(subject)
    corpus_utils.make_directory(path)
    with open(path+tag+'.txt', 'w+') as output:
        cursor = None
        while True:
                #time.sleep(1)
            new_posts, cursor = get_posts(tag, cursor)
            try:
                for new_post in new_posts:
                    try:
                        id = new_post['node']['id']
                        if is_new(id):
                            n = make_post(new_post, id)
                            if len(n) > 500:
                                output.write(n)
                                output.write('\n<instagram_post>\n')
                                post_count+=1
                                if post_count % 100 == 0:
                                    print(post_count)
                            seen_ids.add(id)
                    except:
                        print('skipped a post due to an exception')
            except:
                print('Aborted crawling due to an exception')
                break

            if not cursor or post_count >= 2000:
                break
    print('CRAWL FILISHED: {} - {} - COUNT: {}'.format(subject, tag, post_count))


if __name__ == '__main__':
    for subject in tags.keys():
        seen_ids = set({})
        s_tags = tags[subject].split(' ')
        print ('SUBECT: '+subject)
        for i in range (0, len(s_tags)):
            print('TAG:'+s_tags[i])
            get_insta_posts(s_tags[i], subject)


