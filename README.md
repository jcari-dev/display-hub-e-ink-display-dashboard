
# Display Hub: E-Ink Display Dashboard

Display Hub is an innovative e-ink display manager designed to simplify interactions with e-ink screens. With a focus on modularity and usability, it allows users to effortlessly configure and display essential information through an intuitive drag-and-drop web interface.

![All Modules Sample](all_modules_sample.jpg)

## Key Features

- **Modular Design**: Customize your e-ink display with modules such as:
  - **Traffic Incidents**: Stay informed with live traffic updates using the [TomTom Traffic API](https://developer.tomtom.com).
  - **News Headlines**: Get updates from outlets like [The New York Times](https://www.nytimes.com) and [El País](https://elpais.com), supporting news in both English and Spanish.
  - **Stock Prices**: Track the latest stock prices using [yfinance](https://pypi.org/project/yfinance/) (powered by Yahoo! Finance).
  - **Weather Forecast**: Receive real-time weather updates via the [Open-Meteo API](https://open-meteo.com).
  - **Email Alerts** (in progress): Soon to support notifications from [Gmail](https://mail.google.com) and [Outlook](https://outlook.live.com).

- **Web-Based GUI**: The drag-and-drop web interface makes configuring and managing modules effortless, even for those without technical expertise.

- **Real-Time Updates**: Modules pull live data from external APIs, ensuring the information displayed is always fresh and accurate.

- **One-Click Installation**: With a simple one-command setup, even first-time users can get started in minutes.

- **Cross-Language Support**: The News module currently supports English and Spanish, with plans to expand to other languages in the future.

- **Runs on Raspberry Pi**: Designed to work seamlessly on Raspberry Pi devices, Display Hub is lightweight and energy-efficient, making it perfect for home projects.

## Getting Started

Follow these steps to set up Display Hub on your e-ink display:

### 1. Hardware Requirements

Ensure you have the following hardware:

- **Raspberry Pi**: Refer to the list of supported models [here](https://jcari-dev.github.io/display-hub-e-ink-display-dashboard-docs/docs/resources/supported-pi-models).

- **E-Ink Display**: Refer to the list of supported display models [here](https://jcari-dev.github.io/display-hub-e-ink-display-dashboard-docs/docs/resources/supported-displays).

- **Secondary Device (Optional)**: A device with a desktop environment is required to access the web GUI. While this should work on Raspberry Pi's with a desktop environment, it has not been tested.

### 2. Software Requirements

Ensure you meet the [software requirements.](https://jcari-dev.github.io/display-hub-e-ink-display-dashboard-docs/docs/quickstart/software-requirements)


### 3. Connecting the Screen

To connect the e-Paper display (assuming it is a [Waveshare2in13 V4](https://www.waveshare.com/2.13inch-e-paper-hat.htm) model) to a Raspberry Pi, connect each pin on the display to the corresponding GPIO pin on the Raspberry Pi as shown in the table below:

| e-Paper Connector | Raspberry Pi Pin (Board) |
|-------------------|--------------------------|
| VCC               | 3.3V (Pin 1)             |
| GND               | GND (Pins 6, 9, 14, 20, 25, 30, 34, or 39) |
| DIN               | GPIO 10 (MOSI, Pin 19)   |
| CLK               | GPIO 11 (SCLK, Pin 23)   |
| CS                | GPIO 8 (CE0, Pin 24)     |
| DC                | GPIO 25 (Pin 22)         |
| RST               | GPIO 17 (Pin 11)         |
| BUSY              | GPIO 24 (Pin 18)         |

For reference, you can find a detailed pin layout of the Raspberry Pi GPIO pins on the [Pinout.xyz website](https://pinout.xyz).

Depending on the model of the e-Paper screen, you may also be able to connect the display directly as a HAT. Refer to the supported displays guide for more details.

### 4. Installation

After ensuring that you meet both the hardware and software requirements and that your display is connected, run the following command in your Pi's terminal:

```bash
curl -S https://raw.githubusercontent.com/jcari-dev/display-hub-e-ink-display-dashboard/refs/heads/main/setup.sh | bash
```

When the installation is successful, you should see a message indicating the local IP address to access the web GUI. Upon accessing the provided URL, you will be redirected to the homepage.

For troubleshooting, please refer to the troubleshooting installation page [here](https://jcari-dev.github.io/display-hub-e-ink-display-dashboard-docs/).

## Documentation

For detailed information, please refer to the [Display Hub Documentation](https://jcari-dev.github.io/display-hub-e-ink-display-dashboard-docs/docs/intro/).

## Contributing

We welcome contributions! To get started:

1. Fork the repository.
2. Create a new branch for your feature.
3. Submit a pull request.

## License

This project is licensed under the MIT License.