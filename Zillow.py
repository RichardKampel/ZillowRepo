import requests
import sys
from bs4 import BeautifulSoup
from SinglePropertyScraper import single_scrape

REQ_HEADERS = {"authority": "www.zillow.com",
               "method": "GET",
               "path": "/search/GetSearchPageState.htm?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22usersSearchTerm%22%3A%22Manhattan%2C%20New%20York%2C%20NY%22%2C%22mapBounds%22%3A%7B%22west%22%3A-74.1036203210449%2C%22east%22%3A-73.85402467895506%2C%22south%22%3A40.67111225244346%2C%22north%22%3A40.8902659739345%7D%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A12530%2C%22regionType%22%3A17%7D%5D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22sortSelection%22%3A%7B%22value%22%3A%22days%22%7D%2C%22isAllHomes%22%3A%7B%22value%22%3Atrue%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A12%7D&wants={%22cat1%22:[%22listResults%22,%22mapResults%22],%22cat2%22:[%22total%22]}&requestId=7",
               "scheme": "https",
               "accept": "*/*",
               "accept_encoding": "gzip, deflate, br",
               "accept-language": "en-US,en;q=0.9",
               "cookie": "zguid=23|%2429a113b6-9232-46b8-88b6-d3a9f4a68076; zgsession=1|c4d6bedc-390a-40f5-b4ec-9bb9567149fc; _ga=GA1.2.1480107205.1645543547; zg_anonymous_id=%222fc34413-db26-4f53-b849-94bbee67b91c%22; zjs_anonymous_id=%2229a113b6-9232-46b8-88b6-d3a9f4a68076%22; _gcl_au=1.1.471946074.1645543547; KruxPixel=true; DoubleClickSession=true; _pxvid=b587989b-93f3-11ec-bddb-764e617a6b6a; __pdst=9d7cef9ec14f48718e2dee4f3dbea87e; _cs_c=0; _fbp=fb.1.1645543548161.913985218; _pin_unauth=dWlkPU1UZGtPVGsxTVdJdE9EQTNPQzAwWkdGbExUbGxaRGt0TVdJNE1HVTVPVEJqTWpoaA; KruxAddition=true; g_state={\"i_l\":0}; loginmemento=1|d85dd0d3e5887e7073263757f75f6e6a574a0df7f6a0b99b6fdf14610bfe3a2a; userid=X|3|5b5b0d776c600104%7C9%7Cvw8Sg1nKzu-1HktUc8NnoboRAstPxZ2AEe_HyNBec6c%3D; zjs_user_id=%22X1-ZUsqfew3jvbguh_8xo7u%22; __gads=ID=c0a982dc789b8c9a:T=1645543585:S=ALNI_MbpXG1GK0c0BPaMzg0Fe_v1z-Ft_w; optimizelyEndUserId=oeu1645694932438r0.8066675891253827; _gid=GA1.2.637799767.1645694936; ZILLOW_SSID=1|; FSsampler=1910383593; contently_insights_user=ya278k86bfi5543i7acf; x_contently_id_80832bb06c689bedf1420c42e04931e9={\"s_id\":\"80832bb06c689bedf1420c42e04931e9\",\"user_id\":\"ya278k86bfi5543i7acf\",\"set_ts\":1645694937886}; _clck=1iow4df|1|ez9|0; _cs_id=1f811a45-5f04-a5e8-ea66-3d3c73e25c85.1645543548.5.1645694939.1645694939.1.1679707548783; _uetsid=310f3c40955411ec9e19fbf830c8692d; _uetvid=b59032f093f311ecb82b6b51bd7b2dfb; JSESSIONID=956123D2484C7FEE21F5C105180BFFE8; ZILLOW_SID=1|AAAAAVVbFRIBVVsVEi1Y%2BSM1arIovydcer2Ese5yjYPrIez2%2BKAwHrr5Ap4MmR4xLnth8L%2Bft13GSII6k4ccEeBGD%2Ffj; utag_main=v_id:017f2209e1d00043ee57e50910800507900170710083e$_sn:3$_se:1$_ss:1$_st:1645747702763$dc_visit:2$ses_id:1645745902763%3Bexp-session$_pn:1%3Bexp-session; _clsk=n9e68c|1645745908377|6|0|l.clarity.ms/collect; AWSALB=mI8vKSI38tuVwtN8uxh020W8hzxyruXsSBK22TQ+7FOqe8YUoHy66A/Y14dOguwo9hfLrI1WmJdId6i3hWZTPinqWqvD+ISxtST7g0jIoeMIXLrKKUH4fJOSnS40; AWSALBCORS=mI8vKSI38tuVwtN8uxh020W8hzxyruXsSBK22TQ+7FOqe8YUoHy66A/Y14dOguwo9hfLrI1WmJdId6i3hWZTPinqWqvD+ISxtST7g0jIoeMIXLrKKUH4fJOSnS40; search=6|1648337908444%7Crect%3D40.8902659739345%252C-73.8538530175781%252C40.67111225244346%252C-74.10379198242185%26rid%3D12530%26disp%3Dmap%26mdm%3Dauto%26p%3D1%26sort%3Ddays%26z%3D1%26fs%3D1%26fr%3D0%26mmm%3D0%26rs%3D0%26ah%3D0%26singlestory%3D0%26housing-connector%3D0%26abo%3D0%26garage%3D0%26pool%3D0%26ac%3D0%26waterfront%3D0%26finished%3D0%26unfinished%3D0%26cityview%3D0%26mountainview%3D0%26parkview%3D0%26waterview%3D0%26hoadata%3D1%26zillow-owned%3D0%263dhome%3D0%26featuredMultiFamilyBuilding%3D0%09%0912530%09%09%09%09%09%09; _px3=2bbbf451e7dcd219835bc175c207262fda67af649f01ad68828125ccf1d79200:iw9Twr/8RQUzQQPKKiXC8NUf+u64+HpkfJW7mtYlj14YUfwdEApxgse8FYB4HpkVksXUHRV7Rppoh3/xdWM23Q==:1000:zWIijcHwde9uv4/KAxl0OFgQ0SH9sKWT334AgwYak59xpVwAoWRxzmCsistyb9C9EJFpaSa8Kbv3XJj8LwX18U6IZoO5fx6kS3u7DEmsVdhQ54t/yKIcza2Ki/c0xeNv4OTr+RzUbbx6es9rX0nwEMRpNYDpYObcxDFLHy1F2NsDI7JzwBS5uu8UhF0D8owpbIskFY/gZlrO0PfYefP+xg==",
               "sec-ch-ua": "\" Not A;Brand\";v=\"99\", \"Chromium\";v=\"98\", \"Google Chrome\";v=\"98\"",
               "sec-ch-ua-mobile": "?0",
               "sec-ch-ua-platform": "\"macOS\"",
               "sec-fetch-dest": "empty",
               "sec-fetch-mode": "cors",
               "sec-fetch-site": "same-origin",
               "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, "
                             "like Gecko) Chrome/98.0.4758.102 Safari/537.36",
               }


def print_property_urls_dict_nicely(dict):
    """
    Prints dictionary of property URLs nice
    :param dict:
    :return:
    """
    for key in dict:
        print(f"SEARCH URL: \n{key.url}\n")
        for value in dict[key]:
            print(f"Property URL - {' '.join(value.split('/')[-3].split('-'))}: {value}")
        print('\n')


class ZillowSearch:
    """
    Class whose objects represent individual searches for properties on Zillow
    Attributes:
         - search_url: url of the search (for a specific location)
         - name: name of location searched
    """
    def __init__(self, search_url):
        """
        Initializes ZillowSearch object with both its parameters
        :param search_url: url of the search
        Creates two attributes:
            - url: url of the search
            - properties_info_dict: dictionary of properties (keys) and each property's information (values)
        """
        self.url = search_url
        self.properties_info_dict = {}

    def create_properties_info_dict(self, property_urls_dict):
        """
        Creates properties_info_dict, a dictionary of properties (keys) and each property's information (values)
        :param property_urls_dict: dictionary of properties (keys) and each property's information (values)
        """
        # all_props_dict = {prop_url1: {prop_url: url, Address: "54 4th Ave NY", Price: $, ...}, prop_url2: {prop_url: ...}, ...}
        all_props_dict = {}
        for search_url in property_urls_dict:
            for property_url in property_urls_dict[search_url]:
                all_props_dict[property_url] = single_scrape(property_url)
        self.properties_info_dict = all_props_dict


class ZillowScraper:
    """
    Class whose object represents the project's singular scraper (only one ZillowScraper object created)
    Attributes:
         - property_urls_dict: dictionary of searches/locations searched (keys) and the property urls for each of the
           properties in the given search (e.g. {"https://...manhattan": [prop_url1, prop_url2], ...} )
    """
    property_url_class_in_search = 'list-card-link list-card-link-top-margin'

    def __init__(self):
        """
        Initializes single and only ZillowScraper object
        """
        self.property_urls_dict = {}  # {search1: [prop_url1.1, ...], search2: [prop_url2.1, ...], }

    def scrape_search_for_property_urls(self, search_obj):
        """
        Scrapes url of a ZillowSearch object (e.g. ZillowSearch.url) for the urls of each property in the search result
        :param search_obj: ZillowSearch object
        """
        with requests.Session() as session:
            r = session.get(search_obj.url, headers=REQ_HEADERS)
        soup = BeautifulSoup(r.content, 'html.parser')
        self.property_urls_dict[search_obj] = []
        for link_html_string in soup.find_all(class_=self.property_url_class_in_search, href=True):
            self.property_urls_dict[search_obj] += [link_html_string.get('href')]


def main():
    """
    Main scraper function for extracting data from properties that appear in different searches on Zillow.com
    """
    # Initialise ZillowScraper object
    scraper = ZillowScraper()
    # Create list of Z-Search objects, one for each url provided.
    searches_list = list(sys.argv[1:])
    zsearch_obj_list = [ZillowSearch(url) for url in searches_list]
    for i in range(len(zsearch_obj_list)):
        # Creates dictionary of property URLs for searched location
        scraper.scrape_search_for_property_urls(zsearch_obj_list[i])
        # Creates 2nd dictionary of property-specific information, for each of the properties in a given search result
        zsearch_obj_list[i].create_properties_info_dict(scraper.property_urls_dict)
        # Prints all property-specific data for each property in a given search result
    print("\n\nPROPERTY URLs FOR ALL PROPERTIES (FOR EACH LOCATION SEARCHED):\n\n")
    print_property_urls_dict_nicely(scraper.property_urls_dict)
    print("")
    # Print property data for all properties searched
    print("\n\nPROPERTY INFO FOR ALL PROPERTIES:\n\n")
    for zsearch_obj in zsearch_obj_list:
        for property in zsearch_obj.properties_info_dict:
            print(zsearch_obj.properties_info_dict[property])


if __name__ == "__main__":
    main()
