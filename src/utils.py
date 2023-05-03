import os
import json
import requests

from bs4 import BeautifulSoup
from requests import RequestException


def get_project_path():
    current_path_list = os.getcwd().split("\\")
    #  Where is src
    src_pos = current_path_list.index('src')
    current_path_list = current_path_list[:src_pos]
    current_path = current_path_list[0]+"\\"
    for x in range(1, len(current_path_list)):
        p_var = current_path_list[x]
        current_path = os.path.join(current_path, p_var)
    return current_path


def setup_environment():
    set_env_vars(env_file=os.path.join(base_path, '.env'))

    dir_path = os.path.join(base_path, 'configs', 'env')
    if os.getenv('APP_ENV') == 'dev':
        env_file = os.path.join(dir_path, 'dev.env')
    elif os.getenv('APP_ENV') == 'staging':
        env_file = os.path.join(dir_path, 'staging.env')
    elif os.getenv('APP_ENV') == 'live':
        env_file = os.path.join(dir_path, 'live.env')
        print("***Warning, we are running against live data***")
    else:
        print(f"Invalid APP_ENV of {os.getenv('APP_ENV')}")
        exit(-1)

    set_env_vars(env_file=env_file)


def set_env_vars(env_file=''):
    try:
        with open(env_file) as env_file:
            print(f"{env_file} file read.")
            for line in env_file:
                line = line.strip()
                if line == '':
                    continue
                if line[0] == '#':
                    continue
                if '=' not in line:
                    continue
                env_var_list = line.split("=")
                env_var_name = env_var_list[0]
                env_var_val = env_var_list[1]
                os.environ[env_var_name] = env_var_val
    except:
        print(f"{env_file} does not exist.")


def search(realtor_url):
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        response = requests.get(url=realtor_url, headers=headers)
        # ofile_name = os.path.join(project_path, 'data', 'resp.html')
        # with open(ofile_name, "w", encoding="utf-8") as f:
        #     f.write(response.content.decode("utf-8"))
        #     print(f"{ofile_name} written.")
        return response.content
    except RequestException as e:
        print(f"Unable to get search results {e}")
        return None


def get_soup(text):
    soup = BeautifulSoup(text, "html.parser")
    return soup


def get_listings(text) -> list:
    soup = get_soup(text)
    listings = soup.find_all("div", class_="CardContent__StyledCardContent-rui__sc-7ptz1z-0")
    return listings


def get_listing_type(text) -> str:
    soup = get_soup(text)
    listing_type = soup.find_all("div", class_="Text__StyledText-rui__sc-19ei9fn-0")
    if listing_type:
        if len(listing_type) > 1:
            print(f"{len(listing_type)} types found.")
        listing_type = listing_type[0].text
    else:
        listing_type = ""
    return listing_type


def get_listing_price(text) -> str:
    soup = get_soup(text)
    listing_price = soup.find_all("div", class_="Price__Component-rui__x3geed-0")
    if listing_price:
        if len(listing_price) > 1:
            # Multiple shows how much it went up or down
            # print(f"{len(listing_price)} prices found {listing_price}.")
            pass
        listing_price = listing_price[0].text
    else:
        listing_price = ""
    return listing_price


def get_bed_count(text) -> str:
    soup = get_soup(text)
    bed_list = soup.find_all("li", class_="PropertyBedMetastyles__StyledPropertyBedMeta-rui__a4nnof-0")
    if bed_list:
        bed_list = bed_list[0].text
    else:
        bed_list = ""

    return bed_list


def get_bath_count(text) -> str:
    soup = get_soup(text)
    bath_list = soup.find_all("li", class_="PropertyBathMetastyles__StyledPropertyBathMeta-rui__sc-67m6bo-0")
    if bath_list:
        bath_list = bath_list[0].text
    else:
        bath_list = ""

    return bath_list


def get_square_footage(text) -> str:
    soup = get_soup(text)
    sq_list = soup.find_all("li", class_="PropertySqftMetastyles__StyledPropertySqftMeta-rui__sc-1gdau7i-0")
    if sq_list:
        soup = get_soup(str(sq_list[0]))
        sq_list = soup.find_all("span", class_="VisuallyHiddenstyles__StyledVisuallyHidden-rui__aoql8k-0")
        if sq_list:
            sq_list = sq_list[0].text
        else:
            sq_list = ""
    else:
        sq_list = ""

    return sq_list


base_path = get_project_path()
setup_environment()
project_path = get_project_path()

