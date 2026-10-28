import tkinter as tk
from tkinter import ttk, messagebox
import requests
import tkintermapview

# Modern Dark Theme Palette
BG_COLOR = "#0f172a"        # Deep slate background
CARD_BG = "#1e293b"         # Lighter slate cards
TEXT_PRIMARY = "#f8fafc"    # Bright text
TEXT_SECONDARY = "#94a3b8"  # Muted grey text
ACCENT_COLOR = "#3b82f6"    # Vibrant blue accent
ACCENT_HOVER = "#2563eb"    # Darker blue for hover

class IPTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("GeoStellar - Advanced IP Location Tracker")
        self.root.geometry("1200x750")
        self.root.minsize(1000, 650)
        self.root.configure(bg=BG_COLOR)

        self.current_marker = None
        
        self.setup_styles()
        self.create_layout()

    def setup_styles(self):
        """Configures custom TTK styles for a modern desktop look."""
        style = ttk.Style()
        style.theme_use("clam")

        style.configure(".", background=BG_COLOR, foreground=TEXT_PRIMARY, font=("Segoe UI", 10))
        style.configure("Card.TFrame", background=CARD_BG, relief="flat")
        
        style.configure("TLabel", background=BG_COLOR, foreground=TEXT_PRIMARY)
        style.configure("Card.TLabel", background=CARD_BG, foreground=TEXT_PRIMARY)
        style.configure("Header.TLabel", background=CARD_BG, foreground=TEXT_PRIMARY, font=("Segoe UI", 13, "bold"))
        style.configure("Value.TLabel", background=CARD_BG, foreground="#38bdf8", font=("Segoe UI", 10, "bold"))

        style.configure("Accent.TButton", background=ACCENT_COLOR, foreground="white", font=("Segoe UI", 10, "bold"), borderwidth=0)
        style.map("Accent.TButton", background=[("active", ACCENT_HOVER)])
        
        style.configure("Secondary.TButton", background="#334155", foreground="white", font=("Segoe UI", 10), borderwidth=0)
        style.map("Secondary.TButton", background=[("active", "#475569")])

    def create_layout(self):
        """Builds the 2-column dashboard layout."""
        self.root.rowconfigure(1, weight=1)
        self.root.columnconfigure(0, weight=1)

        # ==========================================
        # TOP CONTROL PANEL
        # ==========================================
        header_frame = ttk.Frame(self.root, style="Card.TFrame")
        header_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 10))
        header_frame.columnconfigure(1, weight=1)

        title_lbl = ttk.Label(header_frame, text="🌍 IP Location Tracker Dashboard", style="Header.TLabel", font=("Segoe UI", 14, "bold"))
        title_lbl.grid(row=0, column=0, columnspan=4, sticky="w", padx=15, pady=(12, 10))

        ttk.Label(header_frame, text="Enter IP / Domain:", style="Card.TLabel").grid(row=1, column=0, sticky="w", padx=15, pady=(0, 15))

        self.ip_entry_var = tk.StringVar()
        self.ip_entry = ttk.Entry(header_frame, textvariable=self.ip_entry_var, font=("Segoe UI", 11))
        self.ip_entry.grid(row=1, column=1, sticky="ew", padx=5, pady=(0, 15))
        self.ip_entry.bind("<Return>", lambda event: self.track_ip())

        btn_track = ttk.Button(header_frame, text="Track Location", style="Accent.TButton", command=self.track_ip)
        btn_track.grid(row=1, column=2, padx=5, pady=(0, 15))

        btn_my_ip = ttk.Button(header_frame, text="Lookup My IP", style="Secondary.TButton", command=lambda: self.track_ip(my_ip=True))
        btn_my_ip.grid(row=1, column=3, padx=(5, 15), pady=(0, 15))

        # ==========================================
        # BODY CONTAINER (Left: Info Panel, Right: Map)
        # ==========================================
        body_container = ttk.Frame(self.root)
        body_container.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 20))
        body_container.rowconfigure(0, weight=1)
        body_container.columnconfigure(0, weight=4)  # Info Panel
        body_container.columnconfigure(1, weight=7)  # Map Widget

        # ------------------------------------------
        # LEFT PANEL: Geolocation Details Cards
        # ------------------------------------------
        info_frame = ttk.Frame(body_container, style="Card.TFrame")
        info_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        info_frame.columnconfigure(1, weight=1)

        ttk.Label(info_frame, text="Geolocation Details", style="Header.TLabel").grid(row=0, column=0, columnspan=2, sticky="w", padx=15, pady=(15, 10))

        fields = [
            ("IP Address", "ip_val"),
            ("Country", "country_val"),
            ("Region / State", "region_val"),
            ("City", "city_val"),
            ("ZIP Code", "zip_val"),
            ("Latitude", "lat_val"),
            ("Longitude", "lon_val"),
            ("Timezone", "tz_val"),
            ("ISP / Organization", "isp_val")
        ]

        self.info_labels = {}
        for idx, (label_text, key) in enumerate(fields, start=1):
            lbl_title = ttk.Label(info_frame, text=f"{label_text}:", style="Card.TLabel")
            lbl_title.grid(row=idx, column=0, sticky="w", padx=15, pady=8)

            lbl_val = ttk.Label(info_frame, text="---", style="Value.TLabel")
            lbl_val.grid(row=idx, column=1, sticky="w", padx=15, pady=8)
            self.info_labels[key] = lbl_val

        # Status footer message
        self.status_var = tk.StringVar(value="Ready. Enter an IP or click 'Lookup My IP'.")
        status_lbl = ttk.Label(info_frame, textvariable=self.status_var, background=CARD_BG, foreground=TEXT_SECONDARY, font=("Segoe UI", 9, "italic"))
        status_lbl.grid(row=len(fields) + 1, column=0, columnspan=2, sticky="w", padx=15, pady=(25, 15))

        # ------------------------------------------
        # RIGHT PANEL: Interactive Map View
        # ------------------------------------------
        map_outer_frame = ttk.Frame(body_container, style="Card.TFrame")
        map_outer_frame.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
        map_outer_frame.rowconfigure(1, weight=1)
        map_outer_frame.columnconfigure(0, weight=1)

        ttk.Label(map_outer_frame, text="Interactive Map Visualization", style="Header.TLabel").grid(row=0, column=0, sticky="w", padx=15, pady=(15, 10))

        # Embedded Map View
        self.map_widget = tkintermapview.TkinterMapView(map_outer_frame, corner_radius=8)
        self.map_widget.grid(row=1, column=0, sticky="nsew", padx=15, pady=(0, 15))
        
        # FIXED: Use Google normal map tiles to bypass OpenStreetMap "Access denied" blocks
        self.map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)
        
        # Default global view initialization
        self.map_widget.set_position(20.0, 0.0)
        self.map_widget.set_zoom(2)

    def track_ip(self, my_ip=False):
        """Fetches details via HTTPS ipapi.co and updates the map marker."""
        query = self.ip_entry_var.get().strip()
        
        self.status_var.set("Fetching geolocation data...")
        self.root.update_idletasks()

        try:
            # FIXED: Secure HTTPS endpoint using ipapi.co
            if my_ip or not query:
                url = "https://ipapi.co/json/"
            else:
                url = f"https://ipapi.co/{query}/json/"

            # Added a standard User-Agent header to satisfy API security rules
            headers = {'User-Agent': 'Mozilla/5.0'}
            response = requests.get(url, headers=headers, timeout=6)
            data = response.json()

            if "error" in data or data.get("reserved") or "reason" in data:
                error_msg = data.get("reason", data.get("message", "Invalid IP address or lookup failed."))
                messagebox.showerror("Lookup Failed", f"Error: {error_msg}")
                self.status_var.set("Lookup failed. Please check your input.")
                return

            # Extract fields accurately matching ipapi.co schema
            ip = data.get("ip", "N/A")
            country = data.get("country_name", "N/A")
            country_code = data.get("country", "")
            region = data.get("region", "N/A")
            city = data.get("city", "N/A")
            zip_code = data.get("postal", "N/A")
            lat = data.get("latitude", 0.0)
            lon = data.get("longitude", 0.0)
            timezone = data.get("timezone", "N/A")
            isp = data.get("org", "N/A")

            if lat is None or lon is None:
                messagebox.showerror("Location Error", "Could not retrieve geographic coordinates for this IP.")
                return

            # Update info card labels
            self.info_labels["ip_val"].config(text=str(ip))
            self.info_labels["country_val"].config(text=f"{country} ({country_code})")
            self.info_labels["region_val"].config(text=str(region))
            self.info_labels["city_val"].config(text=str(city))
            self.info_labels["zip_val"].config(text=str(zip_code))
            self.info_labels["lat_val"].config(text=str(lat))
            self.info_labels["lon_val"].config(text=str(lon))
            self.info_labels["tz_val"].config(text=str(timezone))
            self.info_labels["isp_val"].config(text=str(isp))

            if my_ip or not query:
                self.ip_entry_var.set(str(ip))

            # Move and zoom map to coordinates
            self.map_widget.set_position(float(lat), float(lon))
            self.map_widget.set_zoom(11)

            # Clear existing marker if present
            if self.current_marker:
                self.current_marker.delete()

            # Place a text marker on the map
            marker_text = f"{city}, {country}\nIP: {ip}"
            self.current_marker = self.map_widget.set_marker(float(lat), float(lon), text=marker_text)

            self.status_var.set(f"Successfully located: {city}, {country}")

        except requests.exceptions.RequestException as e:
            messagebox.showerror("Network Error", f"Could not connect to the API server.\nDetails: {e}")
            self.status_var.set("Connection error.")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")
            self.status_var.set("Error occurred.")

if __name__ == "__main__":
    root = tk.Tk()
    app = IPTrackerApp(root)
    root.mainloop()