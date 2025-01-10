import os
import stat

from bottle import response
from db import get_db
from db.models import TrafficSettings

RSS_FEED_MAP = {

    "The New York Times": {
        "NYT Home Page": "https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml",
        "World": "https://rss.nytimes.com/services/xml/rss/nyt/World.xml",
        "Africa": "https://rss.nytimes.com/services/xml/rss/nyt/Africa.xml",
        "Americas": "https://rss.nytimes.com/services/xml/rss/nyt/Americas.xml",
        "Asia Pacific": "https://rss.nytimes.com/services/xml/rss/nyt/AsiaPacific.xml",
        "Europe": "https://rss.nytimes.com/services/xml/rss/nyt/Europe.xml",
        "Middle East": "https://rss.nytimes.com/services/xml/rss/nyt/MiddleEast.xml",
        "U.S.": "https://rss.nytimes.com/services/xml/rss/nyt/US.xml",
        "Education": "https://rss.nytimes.com/services/xml/rss/nyt/Education.xml",
        "Politics": "https://rss.nytimes.com/services/xml/rss/nyt/Politics.xml",
        "The Upshot": "https://rss.nytimes.com/services/xml/rss/nyt/Upshot.xml",
        "N.Y./Region": "https://rss.nytimes.com/services/xml/rss/nyt/NYRegion.xml",
        "Business": "https://rss.nytimes.com/services/xml/rss/nyt/Business.xml",
        "Energy & Environment": "https://rss.nytimes.com/services/xml/rss/nyt/EnergyEnvironment.xml",
        "Small Business": "https://rss.nytimes.com/services/xml/rss/nyt/SmallBusiness.xml",
        "Economy": "https://rss.nytimes.com/services/xml/rss/nyt/Economy.xml",
        "DealBook": "https://rss.nytimes.com/services/xml/rss/nyt/Dealbook.xml",
        "Media & Advertising": "https://rss.nytimes.com/services/xml/rss/nyt/MediaandAdvertising.xml",
        "Your Money": "https://rss.nytimes.com/services/xml/rss/nyt/YourMoney.xml",
        "Technology": "https://rss.nytimes.com/services/xml/rss/nyt/Technology.xml",
        "Personal Tech": "https://rss.nytimes.com/services/xml/rss/nyt/PersonalTech.xml",
        "Sports": "https://rss.nytimes.com/services/xml/rss/nyt/Sports.xml",
        "Baseball": "https://rss.nytimes.com/services/xml/rss/nyt/Baseball.xml",
        "College Basketball": "https://rss.nytimes.com/services/xml/rss/nyt/CollegeBasketball.xml",
        "College Football": "https://rss.nytimes.com/services/xml/rss/nyt/CollegeFootball.xml",
        "Golf": "https://rss.nytimes.com/services/xml/rss/nyt/Golf.xml",
        "Hockey": "https://rss.nytimes.com/services/xml/rss/nyt/Hockey.xml",
        "Pro-Basketball": "https://rss.nytimes.com/services/xml/rss/nyt/ProBasketball.xml",
        "Pro-Football": "https://rss.nytimes.com/services/xml/rss/nyt/ProFootball.xml",
        "Soccer": "https://rss.nytimes.com/services/xml/rss/nyt/Soccer.xml",
        "Tennis": "https://rss.nytimes.com/services/xml/rss/nyt/Tennis.xml",
        "Science": "https://rss.nytimes.com/services/xml/rss/nyt/Science.xml",
        "Environment": "https://rss.nytimes.com/services/xml/rss/nyt/Climate.xml",
        "Space & Cosmos": "https://rss.nytimes.com/services/xml/rss/nyt/Space.xml",
        "Health": "https://rss.nytimes.com/services/xml/rss/nyt/Health.xml",
        "Well Blog": "https://rss.nytimes.com/services/xml/rss/nyt/Well.xml",
        "Arts": "https://rss.nytimes.com/services/xml/rss/nyt/Arts.xml",
        "Art & Design": "https://rss.nytimes.com/services/xml/rss/nyt/ArtandDesign.xml",
        "Book Review": "https://rss.nytimes.com/services/xml/rss/nyt/Books/Review.xml",
        "Dance": "https://rss.nytimes.com/services/xml/rss/nyt/Dance.xml",
        "Movies": "https://rss.nytimes.com/services/xml/rss/nyt/Movies.xml",
        "Music": "https://rss.nytimes.com/services/xml/rss/nyt/Music.xml",
        "Television": "https://rss.nytimes.com/services/xml/rss/nyt/Television.xml",
        "Theater": "https://rss.nytimes.com/services/xml/rss/nyt/Theater.xml",
        "Fashion & Style": "https://rss.nytimes.com/services/xml/rss/nyt/FashionandStyle.xml",
        "Dining & Wine": "https://rss.nytimes.com/services/xml/rss/nyt/DiningandWine.xml",
        "Love": "https://rss.nytimes.com/services/xml/rss/nyt/Weddings.xml",
        "T Magazine": "https://rss.nytimes.com/services/xml/rss/nyt/tmagazine.xml",
        "Travel": "https://www.nytimes.com/services/xml/rss/nyt/Travel.xml",
        "Jobs": "https://rss.nytimes.com/services/xml/rss/nyt/Jobs.xml",
        "Real Estate": "https://rss.nytimes.com/services/xml/rss/nyt/RealEstate.xml",
        "Autos": "https://rss.nytimes.com/services/xml/rss/nyt/Automobiles.xml",
        "Lens Blog": "https://rss.nytimes.com/services/xml/rss/nyt/Lens.xml",
        "Obituaries": "https://rss.nytimes.com/services/xml/rss/nyt/Obituaries.xml",
        "Times Wire": "https://rss.nytimes.com/services/xml/rss/nyt/recent.xml",
        "Most E-Mailed": "https://rss.nytimes.com/services/xml/rss/nyt/MostEmailed.xml",
        "Most Shared": "https://rss.nytimes.com/services/xml/rss/nyt/MostShared.xml",
        "Most Viewed": "https://rss.nytimes.com/services/xml/rss/nyt/MostViewed.xml",
        "Charles M. Blow": "https://www.nytimes.com/svc/collections/v1/publish/www.nytimes.com/column/charles-m-blow/rss.xml",
        "Jamelle Bouie": "https://www.nytimes.com/svc/collections/v1/publish/www.nytimes.com/column/jamelle-bouie/rss.xml",
        "David Brooks": "https://www.nytimes.com/svc/collections/v1/publish/www.nytimes.com/column/david-brooks/rss.xml",
        "Frank Bruni": "https://www.nytimes.com/svc/collections/v1/publish/www.nytimes.com/column/frank-bruni/rss.xml",
        "Gail Collins": "https://www.nytimes.com/svc/collections/v1/publish/www.nytimes.com/column/gail-collins/rss.xml",
        "Ross Douthat": "https://www.nytimes.com/svc/collections/v1/publish/www.nytimes.com/column/ross-douthat/rss.xml",
        "Maureen Dowd": "https://www.nytimes.com/svc/collections/v1/publish/www.nytimes.com/column/maureen-dowd/rss.xml",
        "Thomas L. Friedman": "https://www.nytimes.com/svc/collections/v1/publish/www.nytimes.com/column/thomas-l-friedman/rss.xml",
        "Michelle Goldberg": "https://www.nytimes.com/svc/collections/v1/publish/www.nytimes.com/column/michelle-goldberg/rss.xml",
        "Ezra Klein": "https://www.nytimes.com/svc/collections/v1/publish/www.nytimes.com/column/ezra-klein/rss.xml",
        "Nicholas D. Kristof": "https://www.nytimes.com/svc/collections/v1/publish/www.nytimes.com/column/nicholas-kristof/rss.xml",
        "Paul Krugman": "https://www.nytimes.com/svc/collections/v1/publish/www.nytimes.com/column/paul-krugman/rss.xml",
        "Farhad Manjoo": "https://www.nytimes.com/svc/collections/v1/publish/www.nytimes.com/column/farhad-manjoo/rss.xml",
        "Bret Stephens": "https://www.nytimes.com/svc/collections/v1/publish/www.nytimes.com/column/bret-stephens/rss.xml",
        "Sunday Opinion": "https://rss.nytimes.com/services/xml/rss/nyt/sunday-review.xml"
    },
    "Reuters": {
        "All Sectors": "https://www.reutersagency.com/feed/?taxonomy=best-sectors&post_type=best",
        "Equities": "https://www.reutersagency.com/feed/?best-sectors=equities&post_type=best",
        "Foreign Exchange & Fixed Income": "https://www.reutersagency.com/feed/?best-sectors=foreign-exchange-fixed-income&post_type=best",
        "Economy": "https://www.reutersagency.com/feed/?best-sectors=economy&post_type=best",
        "Commodities & Energy": "https://www.reutersagency.com/feed/?best-sectors=commodities-energy&post_type=best",
        "All Topics": "https://www.reutersagency.com/feed/?taxonomy=best-topics&post_type=best",
        "Business & Finance": "https://www.reutersagency.com/feed/?best-topics=business-finance&post_type=best",
        "Deals": "https://www.reutersagency.com/feed/?best-topics=deals&post_type=best",
        "Politics": "https://www.reutersagency.com/feed/?best-topics=political-general&post_type=best",
        "Environment": "https://www.reutersagency.com/feed/?best-topics=environment&post_type=best",
        "Tech": "https://www.reutersagency.com/feed/?best-topics=tech&post_type=best",
        "Health": "https://www.reutersagency.com/feed/?best-topics=health&post_type=best",
        "Sports": "https://www.reutersagency.com/feed/?best-topics=sports&post_type=best",
        "Entertainment & Lifestyle": "https://www.reutersagency.com/feed/?best-topics=lifestyle-entertainment&post_type=best",
        "Human Interest": "https://www.reutersagency.com/feed/?best-topics=human-interest&post_type=best",
        "Journalist Spotlight": "https://www.reutersagency.com/feed/?best-topics=journalist-spotlight&post_type=best",
        "All Regions": "https://www.reutersagency.com/feed/?taxonomy=best-regions&post_type=best",
        "Middle East": "https://www.reutersagency.com/feed/?best-regions=middle-east&post_type=best",
        "Africa": "https://www.reutersagency.com/feed/?best-regions=africa&post_type=best",
        "Europe": "https://www.reutersagency.com/feed/?best-regions=europe&post_type=best",
        "North America": "https://www.reutersagency.com/feed/?best-regions=north-america&post_type=best",
        "South America": "https://www.reutersagency.com/feed/?best-regions=south-america&post_type=best",
        "Asia": "https://www.reutersagency.com/feed/?best-regions=asia&post_type=best",
        "All Impacts": "https://www.reutersagency.com/feed/?taxonomy=best-customer-impacts&post_type=best",
        "Market Impact": "https://www.reutersagency.com/feed/?best-customer-impacts=market-impact&post_type=best",
        "Media Customer Impact": "https://www.reutersagency.com/feed/?best-customer-impacts=media-customer-impact&post_type=best",
        "All Updates": "https://www.reutersagency.com/feed/?post_type=reuters-best",
        "The Big Picture": "https://www.reutersagency.com/feed/?best-types=the-big-picture&post_type=best",
        "Reuters News First": "https://www.reutersagency.com/feed/?best-types=reuters-news-first&post_type=best"
    }


}


def generate_traffic_api_file():
    try:
        file_path = "/tmp/e-ink.txt"
        with open(file_path, "w") as temp_file:
            temp_file.write("")

        # Set file permissions to 600
        os.chmod(file_path, stat.S_IRUSR | stat.S_IWUSR)
        print(f"File created with secure permissions: {file_path}")
        return file_path
    except Exception as e:
        raise RuntimeError(f"Failed to generate the file: {str(e)}")


def consume_file_traffic_api_file():
    try:
        file_path = "/tmp/e-ink.txt"
        print(f"Checking if file exists at: {file_path}")
        if not os.path.exists(file_path):
            print("File does not exist.")
            return {"error": "File doesn't exist"}

        print("Reading file contents...")
        with open(file_path, 'r') as f:
            lines = f.readlines()

        print(f"File contents: {lines}")

        if len(lines) != 1:
            print("File validation failed: More than one line or empty file.")
            return {"error": "File must contain exactly one line with the API key."}

        api_key = lines[0].strip()
        print(f"Extracted API key: '{api_key}'")

        if not api_key or len(api_key) < 5:  # Adjust the minimum length as needed
            print("Invalid API key: It is empty or too short.")
            return {"error": "Invalid API key. It must be a non-empty string with sufficient length."}

        print("Getting database session...")
        try:
            db = next(get_db())
        except Exception as e:
            raise RuntimeError(f"Failed to get database session: {str(e)}")

        print("Fetching TrafficSettings from database...")
        try:
            traffic_settings = db.get(TrafficSettings, 1)
        except Exception as e:
            raise RuntimeError(
                f"Failed to fetch TrafficSettings from database: {str(e)}")

        if not traffic_settings:
            print("TrafficSettings not found in database.")
            return {"error": "Unable to find traffic settings in the database."}

        zipcode = traffic_settings.zipcode
        print(f"Zipcode retrieved: {zipcode}")

        print("Updating API key in database...")
        try:
            traffic_settings.api_key = api_key
            db.commit()
            print("API key updated successfully.")
        except Exception as e:
            raise RuntimeError(
                f"Failed to update API key in the database: {str(e)}")

        print("Deleting temporary file...")
        try:
            os.remove(file_path)
            print(f"File {file_path} deleted successfully.")
        except Exception as e:
            raise RuntimeError(
                f"Failed to delete the temporary file: {str(e)}")

        print("Process completed successfully.")
        return {"success": True, "message": f"API key updated for zipcode {zipcode}"}

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return {"error": str(e)}
