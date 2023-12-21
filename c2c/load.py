import requests
import json
import pandas as pd
import time


class Load:
    def __init__(self):
        self.base_url = 'https://api.camptocamp.org/routes'

    def load_routes(self, offset=0, limit=1) -> pd.DataFrame:
        url = f"{self.base_url}?offset={offset}&limit={limit}"

        response = requests.get(url)
        response.raise_for_status()  # Check for HTTP errors

        data = json.loads(response.content)
        #print(data)
        documents = []
        for item in data['documents']:
            # Do something with each element (item)
            document_id = item['document_id']
            print(json.dumps(item))
            localized = [x for x in item["locales"] if x["lang"] == "fr"]
            if len(localized) > 0:
                print(document_id)
                documents.append(self.download_route(document_id))

        df = pd.DataFrame(documents)
        #df = df.drop_duplicates()
        #df = df.dropna()

        return df

    def download_route(self, route_id):
        try:
            time.sleep(0.5)
            
            # Construct the full URL by appending the endpoint to the base URL
            full_url = f"{self.base_url}/{route_id}"

            # Send an HTTP GET request to the full URL
            response = requests.get(full_url)
            response.raise_for_status()  # Check for HTTP errors

            data = json.loads(response.content)
            #print(response.content)
            
            # find french locale
            fr = [x for x in data["locales"] if x["lang"] == "fr"][0]
            return {
                "route_id": route_id,
                'url': full_url,
                "activities":  data.get("activities"),
                "elevation_min": data.get("elevation_min"),
                "elevation_max": data.get("elevation_max"),
                "height_diff_up": data.get("height_diff_up"),
                "height_diff_down": data.get("height_diff_down"),
                "route_length": data.get("route_length"),
                "durations": data.get("durations"),
                "height_diff_access": data.get("height_diff_access"),
                "height_diff_difficulties": data.get("height_diff_difficulties"),
                "route_types": data.get("route_types"),
                "orientations": data.get("orientations"),
                "lift_access": data.get("lift_access"),
                "hiking_mtb_exposition": data.get("hiking_mtb_exposition"),
                "mtb_up_rating": data.get("mtb_up_rating"),
                "mtb_down_rating": data.get("mtb_down_rating"),
                "mtb_length_asphalt": data.get("mtb_length_asphalt"),
                "mtb_length_trail": data.get("mtb_length_trail"),
                "mtb_height_diff_portages": data.get("difficulties_height"),
                "difficulties_height": data.get("mtb_height_diff_portages"),
                "route_types": data.get("route_types"),
                "glacier_gear": data.get("glacier_gear"),
                "configuration": data.get("configuration"),
                "global_rating": data.get("global_rating"),
                "engagement_rating": data.get("engagement_rating"),
                "risk_rating": data.get("risk_rating"),
                "equipment_rating": data.get("equipment_rating"),
                "exposition_rock_rating": data.get("exposition_rock_rating"),
                "rock_free_rating": data.get("rock_free_rating"),
                "rock_required_rating": data.get("rock_required_rating"),
                "aid_rating": data.get("aid_rating"),
                "labande_global_rating": data.get("labande_global_rating"),
                "labande_ski_rating": data.get("labande_ski_rating"),
                "rock_types": data.get("rock_types"),
                "ice_rating": data.get("ice_rating"),
                "mixed_rating": data.get("mixed_rating"),
                "ski_rating": data.get("mixed_rating"),
                "ski_exposition": data.get("mixed_rating"),

                "title": f"{fr.get('title_prefix')}, {fr['title']}",
                "description": fr.get("description"),
                "summary": fr.get("summary"),
                "remarks": fr.get("remarks"),
                "gear": fr.get("gear")
            }

        except requests.exceptions.RequestException as e:
            print(f"Error: {str(e)}")
            return {}


