from utils import search, get_listings, get_listing_type, get_listing_price, get_bed_count, \
    get_bath_count, get_square_footage

if __name__ == '__main__':
    url = "https://www.realtor.com/apartments/Raleigh_NC/type-townhome/beds-4/baths-3/affordable"
    resp = search(url)
    if resp:
        print("Search successful.")
        listing_list = get_listings(resp)
        print(f"{len(listing_list)} listings found.")
        if listing_list:
            for listing in listing_list:
                listing_text = str(listing)
                listing_type = get_listing_type(listing_text)
                listing_price = get_listing_price(listing_text)
                bed_count = get_bed_count(listing_text)
                bath_count = get_bath_count(listing_text)
                square_footage = get_square_footage(listing_text)
                output = f"{listing_type}, {listing_price}, {bed_count}, {bath_count}, {square_footage}"
                output_set = set(output.split(","))
                if '' in output_set:
                    output_set.remove('')
                if ' ' in output_set:
                    output_set.remove(' ')
                if output_set:
                    print(output)

