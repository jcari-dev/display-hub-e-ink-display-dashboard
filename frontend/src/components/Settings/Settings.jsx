import NewsSettings from "./SubModules/News/NewsSettings";
import WeatherSettings from "./SubModules/Weather/WeatherSettings";
import TrafficSettings from "./SubModules/Traffic/TrafficSettings";
import StocksSettings from "./SubModules/Stocks/StocksSettings";
import EmailSettings from "./SubModules/Email/EmailSettings";



const Settings = ({ module }) => {

  const moduleMaps = {
    "News": <NewsSettings />,
    "Weather": <WeatherSettings/>,
    "Traffic": <TrafficSettings/>,
    "Stocks": <StocksSettings/>,
    "Email": <EmailSettings/>
  }


  
  if (module === "") {
    return (
      <div>
        <h1></h1>
      </div>
    )
  } else {
    return (
      <div>
        <h1>{module} Settings</h1>
        {moduleMaps[module]}
      </div>
    )
  }


  };
  
export default Settings;
  