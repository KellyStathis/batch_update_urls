import requests
import os
from dotenv import load_dotenv

def batch_update():
    if load_dotenv():
        account_id = os.getenv('ACCOUNT_ID').lower()
        account_pass = os.getenv('ACCOUNT_PASS')

        if account_id and account_pass:
            basic = requests.auth.HTTPBasicAuth(account_id, account_pass)

        # Set headers
        headers = {
            "accept": "application/vnd.api+json"
        }
        params = {
            "client-id": account_id.lower(),
            "page[size]": "1000"
        }

        # Select test or production system. Defaults to test unless PROD=true in env
        prod = False
        prod_config = os.getenv("PROD")
        if prod_config.lower() == "true":
            prod = True

        if prod:
            url = "https://api.datacite.org/dois"
        else:
            url = "https://api.test.datacite.org/dois"


        # Get find and replace strings from env
        find = os.getenv('FIND')
        replace = os.getenv('REPLACE')

        # Get DOIs for client
        response = requests.get(url, headers=headers, params=params, auth=basic)
        response_json = response.json()

        dois = response_json["data"]
        print("# DOIs retrieved: {}".format(str(len(dois))))

        # Construct list of DOIs to update
        urls_to_update = []

        for doi in dois:
            if doi["attributes"]["url"]:
                new_url = doi["attributes"]["url"].replace(find, replace)
                # If the URL would change, add it to urls_to_update
                if new_url != doi["attributes"]["url"]:
                    print("{}: {}  --> {}".format(doi["id"], doi["attributes"]["url"], new_url))
                    urls_to_update.append({"id": doi["id"], "old_url": doi["attributes"]["url"], "new_url": new_url})

        print("# URLs to be updated: {}".format(str(len(urls_to_update))))

        if len(urls_to_update) > 0:
            run_updates = input("Run batch update? (y to proceed)")
            print()
            if run_updates.lower() == "y":
                # Run updates
                update_count = 0
                for doi in urls_to_update:
                    # construct PUT request
                    payload_dict = {
                        "data": {
                            "type": "dois",
                            "attributes": {
                                "url": doi["new_url"]
                            },
                            "id": doi["id"]
                        }
                    }
                    response = requests.put("{}/{}".format(url, doi["id"]), auth=basic, headers=headers, json=payload_dict)
                    response_json = response.json()
                    if response.status_code == 200 and response_json["data"]["attributes"]["url"] == doi["new_url"]:
                        print("{}: {}  --> {}".format(doi["id"], doi["old_url"], doi["new_url"]))
                        update_count += 1
                    else:
                        print("Update failed: {}: {}".format(response.status_code, response_json))

                print("# URLs updated: {}".format(str(update_count)))
                print("Batch update completed.")
            else:
                print("Batch update aborted.")
        else:
            print("No URLs matching criteria to update.")
    else:
        print("No .env file provided.")

if __name__ == '__main__':
    batch_update()
