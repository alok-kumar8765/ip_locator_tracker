# GeoStellar - Advanced IP Location Tracker 🌍

> **A modern, high-performance, dark-themed desktop IP and domain geolocation utility built with Python, Tkinter, `requests`, and `tkintermapview`.**

---

## 📊 Badges

---

## 📑 Table of Contents

1. [Description](https://www.google.com/search?q=%23-description)
2. [Features](https://www.google.com/search?q=%23-features)
3. [Folder Structure Diagram](https://www.google.com/search?q=%23-folder-structure-diagram)
4. [Data Flow Diagram (DFD)](https://www.google.com/search?q=%23-data-flow-diagram-dfd)
5. [Entity-Relationship / Object Model Diagram](https://www.google.com/search?q=%23-entity-relationship--object-model-diagram)
6. [Installation](https://www.google.com/search?q=%23-installation)
7. [Setup Guide](https://www.google.com/search?q=%23-setup-guide)
8. [Usage Guide](https://www.google.com/search?q=%23-usage-guide)
9. [Use Cases](https://www.google.com/search?q=%23-use-cases)
10. [Pros and Cons](https://www.google.com/search?q=%23-pros-and-cons)
11. [Limitations](https://www.google.com/search?q=%23-limitations)
12. [Bugs and Vulnerabilities](https://www.google.com/search?q=%23-bugs-and-vulnerabilities)
13. [Future Updates](https://www.google.com/search?q=%23-future-updates)
14. [Contributing](https://www.google.com/search?q=%23-contributing)
15. [Like, Share, Star](https://www.google.com/search?q=%23-like-share-star)
16. [Thanks & Acknowledgements](https://www.google.com/search?q=%23-thanks--acknowledgements)

---

## 📝 Description

**GeoStellar** is a desktop application designed to lookup and visualize geolocation telemetry for any public IP address or domain name. Powered by Python, custom `ttk` styling, secure HTTPS REST calls via `ipapi.co`, and embedded mapping through `tkintermapview` (utilizing Google map tiles), it instantly provides deep insights including country, region, city, ZIP code, precise latitude/longitude coordinates, timezone, and registered ISP data with an interactive pin marker.

---

## ✨ Features

* **IP & Domain Resolution:** Look up any public IPv4/IPv6 address or domain name (e.g., `google.com` or `8.8.8.8`).
* **Automated Local IP Discovery:** One-click **"Lookup My IP"** button to automatically audit your active public network connection.
* **Comprehensive Telemetry Display:** Instantly extracts and exhibits nine distinct geographic and networking data points.
* **Interactive Map Visualization:** Embeds a fully responsive map tile window pointing a dynamic text-labeled marker directly at the target coordinates.
* **Modern Dark-Themed UI:** Clean slate layout (`#0f172a` and `#1e293b`) configured with polished card frames and clean typography.

---

## 📂 Folder Structure Diagram

```text
GeoStellar/
│
├── ip_tracker.py           # Main application script
├── README.md               # Project documentation
└── assets/                 # Optional media and screenshots
    └── preview.png         # UI screenshot preview

```

---

## 🔄 Data Flow Diagram (DFD)

The execution flow from user input to interactive map rendering:

```text
 [ User Input ] 
   │ (Enters IP/Domain or clicks "Lookup My IP")
   ▼
 [ Control Panel (GUI) ] ──(Triggers Request)──► [ Secure HTTPS REST Call ]
                                                        │
                                              (Queries ipapi.co /json/)
                                                        │
                                            [ Remote Geolocation API Server ]
                                                        │
                                              (Returns JSON telemetry)
                                                        │
                                                        ▼
 [ Main UI Thread ] ◄──(Parses JSON response)── [ Data Handler ]
   │                                                 │
   ├─► Updates Telemetry Card Labels                 └─► Extracts Lat/Lon Coordinates
   ▼
 [ Interactive Map Update ]
   │ (Sets map position & zoom)
   ▼
 [ Renders Custom Map Marker Pin ]

```

---

## 📐 Entity-Relationship / Object Model Diagram

The structural relationship between the desktop GUI controller and map rendering components:

```text
┌─────────────────────────────────┐                 1:1                 ┌─────────────────────────────────┐
│           IPTrackerApp          │ ────────────────────────────────> │      TkinterMapView Object      │
├─────────────────────────────────┤                                   ├─────────────────────────────────┤
│ - root: tk.Tk                   │                                   │ - tile_server: Google Tiles     │
│ - current_marker: MapMarker     │                                   │ - position: (Lat, Lon)          │
│ - info_labels: Dict[str, Label] │                                   │ - zoom_level: Int               │
├─────────────────────────────────┤                                   ├─────────────────────────────────┤
│ + setup_styles()                │                                   │ + set_position(lat, lon)        │
│ + create_layout()               │                                   │ + set_zoom(zoom)                │
│ + track_ip(my_ip)               │                                   │ + set_marker(lat, lon, text)    │
└─────────────────────────────────┘                                   └─────────────────────────────────┘

```

---

## 📦 Installation

Ensure you have **Python 3.8+** installed on your system.

Install the required external dependencies (`requests` for network querying and `tkintermapview` for map embedding) via pip:

```bash
pip install requests tkintermapview

```

---

## ⚙️ Setup Guide

1. Save the application script as `ip_tracker.py`.
2. Verify that dependencies are properly installed by running a quick check in your terminal:
```bash
python -c "import requests, tkintermapview; print('Dependencies ready!')"

```



---

## 💻 Usage

1. Open your terminal or command prompt in the directory containing `ip_tracker.py`.
2. Launch the application:
```bash
python ip_tracker.py

```


3. **Interactive Control:**
* Type any valid IP address or domain name into the input bar and click **Track Location** (or press `Enter`).
* Alternatively, click **Lookup My IP** to instantly load your current public connection details.
* View the telemetry data on the left panel and explore the targeted location pin on the interactive map on the right.



---

## ⚖️ Pros and Cons

### Pros

* **Zero Cost API:** Operates using reliable free-tier public HTTPS endpoints.
* **No API Key Required:** Works straight out of the box without registration or secret keys.
* **Visual Context:** Instant map integration provides immediate geographical clarity.
* **Cross-Platform:** Runs seamlessly on Windows, macOS, and Linux.

### Cons

* **Internet Dependency:** Requires an active internet connection to query geolocation servers and fetch map tiles.
* **Rate Limiting:** Public IP APIs enforce standard request rate limits per IP address.

---

## ⚠️ Limitations

* Geolocation database accuracy for granular locations (like specific city districts) depends on ISP registry updates and IP block allocations, which can occasionally pinpoint the nearest regional data center rather than a physical street address.

---

## 🐛 Bugs and Vulnerabilities

* **Exception Handlers:** Built-in try-except blocks handle network timeouts, invalid domains, and private/reserved IP addresses (`127.0.0.1`, local subnets) gracefully via error message boxes without crashing the application.

---

## 🚀 Future Updates

* [ ] **History Log:** Save recent IP lookups to a local SQLite database for quick review.
* [ ] **Export Report:** Export telemetry details to CSV or PDF summary reports.
* [ ] **Map Layer Switcher:** Toggle between normal road view, satellite imagery, and dark map themes.
* [ ] **WHOIS Integration:** Add a secondary tab for domain registrant and ASN data lookup.

---

## 👥 Contributing

Contributions, bug reports, and feature requests are welcome!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AdvancedTelemetry`)
3. Commit your Changes (`git commit -m 'Add WHOIS lookup feature'`)
4. Push to the Branch (`git push origin feature/AdvancedTelemetry`)
5. Open a Pull Request

---

## ⭐ Like, Share, Star!

If this project helped you track down network routes or build desktop tools, please **give it a ⭐ star** and share it with other developers!

---

## 🙏 Thanks & Acknowledgements

* Built using Python's standard `tkinter` framework and `requests` library.
* Map tile visualizations powered by **tkintermapview** and Google Map tile servers.
* IP lookup data services provided by **ipapi.co**.