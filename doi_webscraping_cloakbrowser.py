#### Web Scraping "citations_count_str", "downloads_count_str" - Iterated - FINAL
# .xlsx data file not included in repo, contact to request

import pandas as pd
import time
import random
import cloakbrowser
from cloakbrowser import launch

# load df and launch synthetic browser

INPUT_FILE = r"data/manscirep_meta_data.xlsx"
SAVE_EVERY = 25

df = pd.read_excel(INPUT_FILE)

df["citations_count_str"] = None
df["downloads_count_str"] = None

browser = launch(headless=True, humanize=True)
page = browser.new_page()


# Extraction functions

def safe_text(page, selector, selector_type="css"):
    """
    Safely extract text from page.
    """
    try:
        if selector_type == "css":
            el = page.query_selector(selector)
        elif selector_type == "id":
            el = page.query_selector(f"#{selector}")
        elif selector_type == "class":
            el = page.query_selector(f".{selector}")
        else:
            return None
        
        if el:
            text = el.inner_text().strip()
            if text:
                return text
            
    except:
        pass
    return "NA"


def extract_metrics(page):
    """
    Try multiple selectors because publishers differ.
    """

    citation_selectors = [("ref_count", "id")]

    download_selectors = [("download-count-container", "class")]

    citations = "NA"
    downloads = "NA"


    for selector, stype in citation_selectors: #citations
        result = safe_text(page, selector, stype)
        if result !="NA":
            citations = result
            break


    for selector, stype in download_selectors: #downloads
        result = safe_text(page, selector, stype)
        if result !="NA":
            downloads = result
            break

    return citations, downloads



# loop across all obs

consecutive_cf = 0

cloudflare_tells = [
    "checking if the site connection is secure",
    "checking your browser",
    "enable javascript and cookies to continue",
    "cf-browser-verification",
    "cloudflare ray id",
    "cf_clearance",
    "just a moment",
    "ddos protection by cloudflare",
    "please wait while we check your browser",
        ]


for index, row in df.iterrows():
#for index, row in df.iloc[151:].iterrows(): # start from last saved obs (ie obs 151)


    doi = str(row["PaperDOI"]).strip()

    if not doi or doi == "nan":
        continue

    # page restart every 50 obs

    if index % 50 == 0 and index > 0: # adjust for starting obs line
        print(f" Restarting browser at obs {index}")
        page.close()
        page = browser.new_page()
        time.sleep(5)

    url = f"https://doi.org/{doi}"
    print(f"\n[{index + 1}/{len(df)}] {doi}")


    try:
        # page navigation

        page.goto(url, wait_until="domcontentloaded", timeout=60000)
        page.wait_for_timeout(4000)  ## wait for dynamic content to load (ie downloads count)

    # accept cookies
        try:
            accept_btn = page.query_selector("button#onetrust-accept-btn-handler") or \
                 page.query_selector("button:has-text('Accept')")
            if accept_btn:
                accept_btn.click()
                page.wait_for_timeout(1500)  # wait for page to re-render after accept
        except:
            pass

    # bot-wall detection

        page_content = page.content().lower()
        page_url = page.url.lower()

        if any(tell in page_content for tell in cloudflare_tells) or "challenges.cloudflare.com" in page_url:
            consecutive_cf += 1
            print(f"  ⚠ Cloudflare challenge at row {index} — backing off 90s and restarting")
            df.at[index, "citations_count_str"] = "cloudflare"
            df.at[index, "downloads_count_str"] = "cloudflare"
            page.screenshot(path=f"cloudflare_{index}.png")  # remove once confirmed working
            page.close()
            page = browser.new_page()
            time.sleep(90)
            continue
        else:
            consecutive_cf = 0

        final_url = page.url

        if "an error has occured" in page_content or "contact your system administrator" in page_content:
            print(f"  ⚠ INFORMS server error at row {index} — retrying after 30s")
            df.at[index, "citations_count_str"] = "server_error"
            df.at[index, "downloads_count_str"] = "server_error"
            time.sleep(30)
            continue 


        # extract metrics

        citations, downloads = extract_metrics(page)

        ### temp debug
        #if citations == "NA" and downloads == "NA":
        #    page.screenshot(path=f"debug_na_{index}.png")
        ### temp debug


        df.at[index, "citations_count_str"] = citations
        df.at[index, "downloads_count_str"] = downloads
        print(f"  Citations: {citations}")
        print(f"  Downloads: {downloads}")

        time.sleep(random.uniform(5, 10))

    except Exception as e:
        print(f"ERROR: {e}")
        df.at[index, "citations_count_str"] = "error"
        df.at[index, "downloads_count_str"] = "error"

    if (index + 1) % SAVE_EVERY == 0:
        df.to_excel(r"data/manscirep_meta_data_v3.xlsx")
        print(f"Saved at {index + 1}")


browser.close()
df.to_excel(r"data/manscirep_meta_data_v3.xlsx")
print("\nComplete.  File saved.")