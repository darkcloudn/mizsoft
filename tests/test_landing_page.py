"""
Comprehensive Automated Test Suite for Mizsoft Landing Page
Target Workspace: /Volumes/Workplace/Mizsoft/LandingPage-Mizsoft

This test suite covers all 5 Tiers specified in Chairman's directives & Acceptance Criteria:
- Tier 1: HTML Structure (Bento Grid 4 cards 2:1:1:2, Ticker, Work Grid 9 cards, Stats, Footer, Slide Panel, Modal container)
- Tier 2: 4 Core Tech Pillars Content (Camera AI RK3588, KiCad PCB 4-8 layers, SmartFarm/SmartLight IoT, Enterprise ERP & AI Agents)
- Tier 3: Zero Legacy Keywords ("LINE apps", "mini templates", "piggy farm")
- Tier 4: Multilingual T object (VI, EN, JA, KO) on index.html and mobile.html, data-i18n bindings, Modal i18n
- Tier 5: Local HTTP Server (http://localhost:8000), Local Resources & JavaScript Syntax Integrity
"""

import os
import re
import json
import subprocess
import urllib.request
import urllib.error
import unittest
from pathlib import Path
from bs4 import BeautifulSoup

# Base directory for the landing page project
WORKSPACE_DIR = Path("/Volumes/Workplace/Mizsoft/LandingPage-Mizsoft").resolve()
INDEX_HTML_PATH = WORKSPACE_DIR / "index.html"
MOBILE_HTML_PATH = WORKSPACE_DIR / "mobile.html"
OPENSOURCE_HTML_PATH = WORKSPACE_DIR / "opensource.html"
HTTP_BASE_URL = "http://localhost:8000"


def read_file(path: Path) -> str:
    """Helper to read UTF-8 file content."""
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def extract_js_object_with_node(html_path: Path, pattern: str) -> dict:
    """
    Extract a JS object matching a regex pattern from an HTML file using Node.js.
    Returns parsed dictionary.
    """
    code = f"""
    const fs = require('fs');
    const html = fs.readFileSync('{html_path}', 'utf8');
    const match = html.match({pattern});
    if (!match) {{
        console.error('Pattern not found');
        process.exit(1);
    }}
    try {{
        const fn = new Function('return ' + match[1]);
        console.log(JSON.stringify(fn()));
    }} catch (e) {{
        console.error('Eval error: ' + e.message);
        process.exit(2);
    }}
    """
    res = subprocess.run(
        ["node", "-e", code],
        capture_output=True,
        text=True
    )
    if res.returncode != 0:
        raise ValueError(f"Failed to extract JS object from {html_path.name}: {res.stderr}")
    return json.loads(res.stdout)


class TestTier1HtmlStructure(unittest.TestCase):
    """
    Tier 1: HTML Structure & Component Verification
    - Bento Grid 4 cards in 2:1:1:2 geometry
    - Ticker banner with seamless loop & core items
    - Work Grid with exactly 9 cards
    - Stats section
    - Footer structure
    - Slide Panel / Mobile Bottom Sheet
    - Modal container DOM
    """

    def setUp(self):
        self.index_html = read_file(INDEX_HTML_PATH)
        self.mobile_html = read_file(MOBILE_HTML_PATH)
        self.index_soup = BeautifulSoup(self.index_html, "html.parser")
        self.mobile_soup = BeautifulSoup(self.mobile_html, "html.parser")

    def test_bento_grid_4_cards_and_ratio_2_1_1_2(self):
        """Verify Bento Grid on index.html has exactly 4 cards with 2:1:1:2 ratio."""
        bento_grid = self.index_soup.find(class_="bento-grid")
        self.assertIsNotNone(bento_grid, "bento-grid container not found in index.html")

        # Find direct bento-card children
        cards = bento_grid.find_all(class_="bento-card", recursive=False)
        self.assertEqual(len(cards), 4, f"Expected exactly 4 bento-cards in bento-grid, but found {len(cards)}")

        # Verify geometric ratio: Card 1 (large: 2), Card 2 (normal: 1), Card 3 (normal: 1), Card 4 (large: 2)
        c1, c2, c3, c4 = cards[0], cards[1], cards[2], cards[3]

        self.assertIn("bento-large", c1.get("class", []), "Card 1 must have 'bento-large' class (ratio 2)")
        self.assertNotIn("bento-large", c2.get("class", []), "Card 2 must be standard width (ratio 1)")
        self.assertNotIn("bento-large", c3.get("class", []), "Card 3 must be standard width (ratio 1)")
        self.assertIn("bento-large", c4.get("class", []), "Card 4 must have 'bento-large' class (ratio 2)")

        # Verify data-service attributes
        self.assertEqual(c1.get("data-service"), "camera-ai", "Card 1 must target 'camera-ai'")
        self.assertEqual(c2.get("data-service"), "pcb", "Card 2 must target 'pcb'")
        self.assertEqual(c3.get("data-service"), "iot", "Card 3 must target 'iot'")
        self.assertEqual(c4.get("data-service"), "erp", "Card 4 must target 'erp'")

    def test_ticker_structure_and_items(self):
        """Verify Ticker on desktop and mobile contains separator dots and core technology items."""
        # Desktop
        desktop_ticker_wrap = self.index_soup.find(class_="ticker-wrap")
        self.assertIsNotNone(desktop_ticker_wrap, "ticker-wrap not found in index.html")
        desktop_ticker = desktop_ticker_wrap.find(class_="ticker")
        self.assertIsNotNone(desktop_ticker, "ticker not found in index.html")

        desktop_items = desktop_ticker.find_all(class_="ticker-item")
        self.assertGreaterEqual(len(desktop_items), 2, "Expected at least 2 ticker-items for seamless marquee")
        desktop_text = desktop_items[0].get_text()

        required_ticker_items = [
            "Camera AI",
            "PCB KiCad",
            "SmartFarm IoT",
            "Enterprise ERP",
            "Firmware Nhúng",
            "Computer Vision"
        ]
        for item in required_ticker_items:
            self.assertIn(item, desktop_text, f"Missing '{item}' in desktop ticker")
        self.assertIn("✦", desktop_text, "Missing '✦' separator in desktop ticker")

        # Mobile
        mobile_ticker_wrap = self.mobile_soup.find(class_="ticker-wrap")
        self.assertIsNotNone(mobile_ticker_wrap, "ticker-wrap not found in mobile.html")
        mobile_text = mobile_ticker_wrap.get_text()
        for item in required_ticker_items:
            self.assertIn(item, mobile_text, f"Missing '{item}' in mobile ticker")

    def test_work_grid_9_cards_desktop(self):
        """Verify Work Grid in index.html has exactly 9 project cards."""
        work_grid = self.index_soup.find(class_="work-grid")
        self.assertIsNotNone(work_grid, "work-grid not found in index.html")

        # Cards can be div.work-card or a.work-card
        cards = work_grid.find_all(lambda el: el.name in ["div", "a"] and "work-card" in el.get("class", []))
        self.assertEqual(len(cards), 9, f"Expected 9 work-cards in index.html, but found {len(cards)}")

        # Verify key project identifiers
        data_projects = [c.get("data-project") for c in cards if c.get("data-project")]
        expected_projects = ["camera-ai", "pcb", "smartfarm", "smartlight", "erp", "ai-agent", "data", "iot"]
        for p in expected_projects:
            self.assertIn(p, data_projects, f"Project '{p}' missing from work-grid")

        # Verify the 9th item is the live demo link
        demo_card = [c for c in cards if c.name == "a" and "demo/farm-organic-iot" in c.get("href", "")]
        self.assertEqual(len(demo_card), 1, "9th work-card must be live demo link to 'demo/farm-organic-iot/'")

    def test_work_swipe_cards_mobile(self):
        """Verify Work section in mobile.html has exactly 9 swipe cards and 9 indicator dots."""
        track = self.mobile_soup.find(id="swipe-track")
        if not track:
            track = self.mobile_soup.find(class_="swipe-track")
        self.assertIsNotNone(track, "swipe-track not found in mobile.html")

        cards = track.find_all(lambda el: el.name in ["div", "a"] and "swipe-card" in el.get("class", []))
        self.assertEqual(len(cards), 9, f"Expected 9 swipe-cards in mobile.html, but found {len(cards)}")

        dots_container = self.mobile_soup.find(id="swipe-dots")
        self.assertIsNotNone(dots_container, "swipe-dots container not found in mobile.html")
        dots = dots_container.find_all(class_="swipe-dot")
        self.assertEqual(len(dots), 9, f"Expected 9 swipe-dots in mobile.html, but found {len(dots)}")

    def test_stats_section_structure(self):
        """Verify Stats section on both desktop and mobile has 4 metrics."""
        # Desktop
        desktop_stats = self.index_soup.find(class_="stats-grid")
        self.assertIsNotNone(desktop_stats, "stats-grid not found in index.html")
        desktop_items = desktop_stats.find_all(class_="stat-item")
        self.assertEqual(len(desktop_items), 4, f"Expected 4 stat-items in index.html, got {len(desktop_items)}")

        # Mobile
        mobile_stats = self.mobile_soup.find(class_="stats-grid")
        self.assertIsNotNone(mobile_stats, "stats-grid not found in mobile.html")
        mobile_items = mobile_stats.find_all(class_="stat-item")
        self.assertEqual(len(mobile_items), 4, f"Expected 4 stat-items in mobile.html, got {len(mobile_items)}")

    def test_footer_structure(self):
        """Verify Footer contains Mizsoft branding, copyright 2026, Tokyo & Vietnam."""
        footer = self.index_soup.find("footer")
        self.assertIsNotNone(footer, "footer tag not found in index.html")
        footer_text = footer.get_text()
        self.assertIn("Mizsoft", footer_text, "Brand 'Mizsoft' not found in footer")
        self.assertIn("2026", footer_text, "Year '2026' not found in footer")
        self.assertIn("Tokyo", footer_text, "'Tokyo' not found in footer")
        self.assertIn("Vietnam", footer_text, "'Vietnam' not found in footer")

    def test_slide_panel_desktop(self):
        """Verify Slide Panel contact drawer and open triggers in index.html."""
        panel = self.index_soup.find(id="panel")
        self.assertIsNotNone(panel, "panel container (#panel) not found in index.html")
        overlay = self.index_soup.find(id="panel-overlay")
        self.assertIsNotNone(overlay, "panel-overlay not found in index.html")
        close_btn = self.index_soup.find(id="close-panel")
        self.assertIsNotNone(close_btn, "close-panel button not found in index.html")

        # Verify open panel buttons exist
        self.assertIsNotNone(self.index_soup.find(id="open-panel"), "#open-panel button missing")
        self.assertIsNotNone(self.index_soup.find(id="open-panel-hero"), "#open-panel-hero button missing")
        self.assertIsNotNone(self.index_soup.find(id="open-panel-cta"), "#open-panel-cta button missing")

    def test_bottom_sheet_mobile(self):
        """Verify Bottom Sheet contact drawer in mobile.html."""
        sheet = self.mobile_soup.find(id="sheet")
        self.assertIsNotNone(sheet, "sheet container (#sheet) not found in mobile.html")
        sheet_bg = self.mobile_soup.find(id="sheet-bg")
        self.assertIsNotNone(sheet_bg, "sheet-bg backdrop not found in mobile.html")
        form = self.mobile_soup.find(id="mobile-form")
        self.assertIsNotNone(form, "mobile-form not found in mobile.html")

        # Verify open triggers
        self.assertIsNotNone(self.mobile_soup.find(id="open-sheet"), "#open-sheet missing")
        self.assertIsNotNone(self.mobile_soup.find(id="open-sheet-2"), "#open-sheet-2 missing")

    def test_modal_container_dom(self):
        """Verify Project/Service Modal container DOM elements in index.html."""
        modal = self.index_soup.find(id="projModal")
        self.assertIsNotNone(modal, "#projModal not found in index.html")
        overlay = self.index_soup.find(id="projOverlay")
        self.assertIsNotNone(overlay, "#projOverlay not found in index.html")
        visual = self.index_soup.find(id="projVisual")
        self.assertIsNotNone(visual, "#projVisual not found in index.html")
        body = self.index_soup.find(id="projBody")
        self.assertIsNotNone(body, "#projBody not found in index.html")
        close_btn = self.index_soup.find(id="projClose")
        self.assertIsNotNone(close_btn, "#projClose not found in index.html")


class TestTier2TechPillars(unittest.TestCase):
    """
    Tier 2: Core Technology Pillars Content Verification
    Must reflect genuine engineering specs from Workplace:
    1. Camera AI RK3588, <20ms latency, YOLOv10, Computer Vision
    2. KiCad PCB 4-8 layers, RF impedance, IPC-A-610, STM32WLE5 LoRa, ESP32-S3, ESD/TVS
    3. SmartFarm IoT, soil NPK/pH/EC, LoRaWAN 10km, SmartLight GIS realtime
    4. Enterprise ERP Clean Architecture & DDD, Multi-Agent AI with HITL
    """

    def setUp(self):
        self.index_html = read_file(INDEX_HTML_PATH)
        self.mobile_html = read_file(MOBILE_HTML_PATH)

    def test_pillar_1_camera_ai_edge_cv(self):
        """Verify Pillar 1: Camera AI & Edge Computing specs."""
        content = self.index_html + self.mobile_html

        self.assertTrue(
            re.search(r"RK3588|Jetson", content, re.IGNORECASE),
            "Pillar 1 must mention edge NPU chips: RK3588 or Jetson"
        )
        self.assertTrue(
            re.search(r"<20ms|dưới 20ms", content, re.IGNORECASE),
            "Pillar 1 must specify low latency (<20ms)"
        )
        self.assertTrue(
            re.search(r"YOLOv10|YOLO", content, re.IGNORECASE),
            "Pillar 1 must specify YOLO/YOLOv10 models"
        )
        self.assertTrue(
            re.search(r"khuôn mặt|dị thường|Computer Vision", content, re.IGNORECASE),
            "Pillar 1 must specify facial recognition, anomaly detection, or Computer Vision"
        )

    def test_pillar_2_pcb_hardware_kicad(self):
        """Verify Pillar 2: Hardware R&D & KiCad PCB Design specs."""
        content = self.index_html + self.mobile_html

        self.assertTrue(
            re.search(r"KiCad", content),
            "Pillar 2 must mention KiCad EDA"
        )
        self.assertTrue(
            re.search(r"4\s*-\s*8\s*lớp|4-8\s*layer", content, re.IGNORECASE),
            "Pillar 2 must specify 4-8 layer PCB design"
        )
        self.assertTrue(
            re.search(r"STM32WLE5|ESP32-S3", content),
            "Pillar 2 must mention STM32WLE5 LoRa or ESP32-S3 Gateway"
        )
        self.assertTrue(
            re.search(r"IPC-?A?-?610|trở kháng|ESD|TVS", content, re.IGNORECASE),
            "Pillar 2 must specify IPC standard, impedance control, or ESD/TVS protection"
        )
        self.assertTrue(
            re.search(r"FreeRTOS|Bare-metal", content, re.IGNORECASE),
            "Pillar 2 must specify embedded firmware (FreeRTOS or Bare-metal C)"
        )

    def test_pillar_3_smartfarm_smartlight_iot(self):
        """Verify Pillar 3: SmartFarm & SmartLight IoT Platform specs."""
        content = self.index_html + self.mobile_html

        self.assertTrue(
            re.search(r"SmartFarm", content),
            "Pillar 3 must mention SmartFarm"
        )
        self.assertTrue(
            re.search(r"NPK|pH|EC|vi khí hậu", content),
            "Pillar 3 must mention agricultural sensors (NPK/pH/EC/vi khí hậu)"
        )
        self.assertTrue(
            re.search(r"LoRaWAN|LoRa", content),
            "Pillar 3 must specify LoRaWAN connectivity"
        )
        self.assertTrue(
            re.search(r"10km", content),
            "Pillar 3 must specify 10km LoRaWAN coverage"
        )
        self.assertTrue(
            re.search(r"SmartLight", content),
            "Pillar 3 must mention SmartLight"
        )
        self.assertTrue(
            re.search(r"GIS|thiên văn", content, re.IGNORECASE),
            "Pillar 3 must mention GIS mapping or astronomical scheduling"
        )

    def test_pillar_4_enterprise_erp_ai_agents(self):
        """Verify Pillar 4: Enterprise ERP & AI Agents specs."""
        content = self.index_html + self.mobile_html

        self.assertTrue(
            re.search(r"Clean Architecture|DDD", content, re.IGNORECASE),
            "Pillar 4 must specify Clean Architecture or Domain-Driven Design"
        )
        self.assertTrue(
            re.search(r"kho vận|FIFO|chuỗi cung ứng", content, re.IGNORECASE),
            "Pillar 4 must mention warehouse logistics (FIFO) or supply chain"
        )
        self.assertTrue(
            re.search(r"AI Agent|Multi-Agent", content, re.IGNORECASE),
            "Pillar 4 must mention AI Agent or Multi-Agent systems"
        )
        self.assertTrue(
            re.search(r"HITL|Human-in-the-loop", content, re.IGNORECASE),
            "Pillar 4 must specify Human-In-The-Loop (HITL) checkpoints"
        )


class TestTier3LegacyKeywordsSanitation(unittest.TestCase):
    """
    Tier 3: 100% Elimination of Legacy Keywords & Services
    Chairman explicitly ordered removing:
    - "LINE apps" / "mini templates" / "piggy farm"
    - Legacy LINE contact channel (replace with WhatsApp or standard channel)
    - Legacy demo folders and references
    """

    def test_no_line_apps_or_line_channel_in_index_html(self):
        """Check index.html has no legacy 'LINE apps' or old LINE contact channel."""
        index_content = read_file(INDEX_HTML_PATH)

        self.assertNotIn(
            "LINE apps",
            index_content,
            "Legacy keyword 'LINE apps' found in index.html"
        )
        self.assertNotIn(
            "LINE Mini App",
            index_content,
            "Legacy keyword 'LINE Mini App' found in index.html"
        )

        # Check contact channel at line 384 of index.html
        soup = BeautifulSoup(index_content, "html.parser")
        line_methods = soup.find_all(
            lambda el: el.name == "a" and "line.me" in el.get("href", "")
        )
        self.assertEqual(
            len(line_methods),
            0,
            f"Found {len(line_methods)} legacy LINE contact links in index.html; should be replaced with WhatsApp or standard channel"
        )

    def test_no_mini_templates_in_workspace(self):
        """Check no 'mini templates' or 'mini template' exist in landing page files."""
        for path in [INDEX_HTML_PATH, MOBILE_HTML_PATH]:
            content = read_file(path)
            self.assertFalse(
                re.search(r"mini\s*templates?", content, re.IGNORECASE),
                f"Found legacy keyword 'mini template(s)' in {path.name}"
            )

    def test_no_piggy_farm_references_in_landing_pages(self):
        """Check index.html, mobile.html, and opensource.html have no piggy farm references."""
        for path in [INDEX_HTML_PATH, MOBILE_HTML_PATH, OPENSOURCE_HTML_PATH]:
            if not path.exists():
                continue
            content = read_file(path)
            self.assertFalse(
                re.search(r"piggy[\s\-_]*farm|đếm heo", content, re.IGNORECASE),
                f"Found legacy keyword 'piggy farm' or 'đếm heo' in {path.name}"
            )

    def test_piggy_farm_demo_isolated_or_removed(self):
        """Check demo/piggy-farm/ folder is isolated or cleaned from public projects."""
        piggy_dir = WORKSPACE_DIR / "demo" / "piggy-farm"
        # The demo folder should ideally not exist or not be served in active project portfolio
        self.assertFalse(
            piggy_dir.exists(),
            f"Legacy directory {piggy_dir} still exists in codebase; should be deleted or isolated"
        )


class TestTier4MultilingualI18n(unittest.TestCase):
    """
    Tier 4: Multilingual Translation Engine & Data Binding Verification
    - T object supports 4 languages: VI, EN, JA, KO
    - Every data-i18n attribute on HTML matches a valid key in all 4 language dictionaries
    - Mobile services list (.svc-list) has data-i18n bindings
    - Modal popup data (SERVICES and PROJECTS) supports multilingual localization
    - Hotline on mobile is properly configured to real number (0966 818 075)
    """

    def setUp(self):
        self.index_html = read_file(INDEX_HTML_PATH)
        self.mobile_html = read_file(MOBILE_HTML_PATH)

    def test_t_object_has_4_languages_index(self):
        """Verify T object in index.html defines vi, en, ja, ko."""
        t_obj = extract_js_object_with_node(INDEX_HTML_PATH, r"/const T = ({[\s\S]*?\n\s*};)/")
        expected_langs = ["vi", "en", "ja", "ko"]
        for lang in expected_langs:
            self.assertIn(lang, t_obj, f"Language '{lang}' missing in T object of index.html")
            self.assertGreater(len(t_obj[lang]), 30, f"Language '{lang}' has too few keys in index.html")

    def test_t_object_has_4_languages_mobile(self):
        """Verify T object in mobile.html defines vi, en, ja, ko."""
        t_obj = extract_js_object_with_node(MOBILE_HTML_PATH, r"/const T = ({[\s\S]*?\n\s*};)/")
        expected_langs = ["vi", "en", "ja", "ko"]
        for lang in expected_langs:
            self.assertIn(lang, t_obj, f"Language '{lang}' missing in T object of mobile.html")
            self.assertGreater(len(t_obj[lang]), 25, f"Language '{lang}' has too few keys in mobile.html")

    def test_all_data_i18n_keys_bound_in_index_html(self):
        """Verify all data-i18n and data-i18n-placeholder tags in index.html exist in all 4 languages."""
        t_obj = extract_js_object_with_node(INDEX_HTML_PATH, r"/const T = ({[\s\S]*?\n\s*};)/")
        soup = BeautifulSoup(self.index_html, "html.parser")

        i18n_keys = [el["data-i18n"] for el in soup.find_all(attrs={"data-i18n": True})]
        ph_keys = [el["data-i18n-placeholder"] for el in soup.find_all(attrs={"data-i18n-placeholder": True})]
        all_keys = set(i18n_keys + ph_keys)

        for lang in ["vi", "en", "ja", "ko"]:
            dict_keys = set(t_obj.get(lang, {}).keys())
            missing = all_keys - dict_keys
            self.assertEqual(
                len(missing),
                0,
                f"Missing i18n keys in index.html T['{lang}']: {missing}"
            )

    def test_all_data_i18n_keys_bound_in_mobile_html(self):
        """Verify all data-i18n and data-i18n-placeholder tags in mobile.html exist in all 4 languages."""
        t_obj = extract_js_object_with_node(MOBILE_HTML_PATH, r"/const T = ({[\s\S]*?\n\s*};)/")
        soup = BeautifulSoup(self.mobile_soup_str(), "html.parser")

        i18n_keys = [el["data-i18n"] for el in soup.find_all(attrs={"data-i18n": True})]
        ph_keys = [el["data-i18n-placeholder"] for el in soup.find_all(attrs={"data-i18n-placeholder": True})]
        all_keys = set(i18n_keys + ph_keys)

        for lang in ["vi", "en", "ja", "ko"]:
            dict_keys = set(t_obj.get(lang, {}).keys())
            missing = all_keys - dict_keys
            self.assertEqual(
                len(missing),
                0,
                f"Missing i18n keys in mobile.html T['{lang}']: {missing}"
            )

    def mobile_soup_str(self):
        return self.mobile_html

    def test_mobile_services_list_has_data_i18n(self):
        """Verify the 4 service names in mobile.html .svc-list have data-i18n attributes."""
        soup = BeautifulSoup(self.mobile_html, "html.parser")
        svc_names = soup.select(".svc-list .svc-name")
        self.assertEqual(len(svc_names), 4, f"Expected 4 .svc-name elements in mobile.html, found {len(svc_names)}")

        for i, el in enumerate(svc_names, 1):
            key = el.get("data-i18n")
            self.assertIsNotNone(
                key,
                f"Service #{i} ('{el.get_text()}') in mobile.html is missing data-i18n attribute"
            )

    def test_modal_popups_support_multilingual(self):
        """
        Verify that Modal Popups (SERVICES and PROJECTS) support multilingual content.
        If hardcoded in Vietnamese only, this test fails and reports defect.
        """
        # Check if SERVICES in index.html is keyed by language or if openService handles language
        code = f"""
        const fs = require('fs');
        const html = fs.readFileSync('{INDEX_HTML_PATH}', 'utf8');

        // Check if openService uses currentLang or localized dictionary
        const hasLangAwareService = html.includes('SERVICES[currentLang]') ||
                                    html.includes('SERVICES[lang]') ||
                                    html.includes('openService') && html.includes('T[currentLang]');

        // Check if modal section titles in JS are localized rather than hardcoded Vietnamese
        const hardcodedSectionTitles = html.includes('>Chỉ số nổi bật<') ||
                                       html.includes('>Tính năng & khả năng<') ||
                                       html.includes('>Công nghệ sử dụng<');

        console.log(JSON.stringify({{
            hasLangAwareService: hasLangAwareService,
            hasHardcodedVietnameseTitles: hardcodedSectionTitles
        }}));
        """
        res = subprocess.run(["node", "-e", code], capture_output=True, text=True)
        self.assertEqual(res.returncode, 0, f"Node script failed: {res.stderr}")
        data = json.loads(res.stdout)

        self.assertFalse(
            data["hasHardcodedVietnameseTitles"],
            "Modal popup section titles in index.html are hardcoded in Vietnamese ('Chỉ số nổi bật', etc.). Must be localized via i18n."
        )
        self.assertTrue(
            data["hasLangAwareService"],
            "openService / SERVICES in index.html is not language-aware (hardcoded in Vietnamese). Must support VI, EN, JA, KO."
        )

    def test_mobile_hotline_number_standardized(self):
        """Verify hotline number in mobile.html is standardized to 0966 818 075, not dummy 0123 456 789."""
        self.assertNotIn(
            "0123 456 789",
            self.mobile_html,
            "Dummy phone number '0123 456 789' still exists in mobile.html. Should be '0966 818 075'"
        )
        self.assertIn(
            "0966 818 075",
            self.mobile_html,
            "Standard phone number '0966 818 075' not found in mobile.html"
        )


class TestTier5HttpServerAndResources(unittest.TestCase):
    """
    Tier 5: Local HTTP Server (http://localhost:8000), Resource Links & JS Syntax Integrity
    - http://localhost:8000/index.html responds 200 OK
    - http://localhost:8000/mobile.html responds 200 OK
    - All linked CSS files return 200 OK and exist on filesystem
    - All linked JS files return 200 OK and exist on filesystem
    - JS files in js/ and inline script blocks in HTML parse without SyntaxError
    """

    def test_http_server_serves_index_html(self):
        """Verify HTTP server at http://localhost:8000 serves index.html with 200 OK."""
        url = f"{HTTP_BASE_URL}/index.html"
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "MizsoftTestHarness/1.0"})
            with urllib.request.urlopen(req, timeout=5) as resp:
                self.assertEqual(resp.status, 200, f"Expected 200 from {url}, got {resp.status}")
                body = resp.read().decode("utf-8")
                self.assertIn("Mizsoft", body, "Response body does not contain 'Mizsoft'")
        except urllib.error.URLError as e:
            self.fail(f"Failed to connect to local HTTP server at {url}: {e.reason}")

    def test_http_server_serves_mobile_html(self):
        """Verify HTTP server at http://localhost:8000 serves mobile.html with 200 OK."""
        url = f"{HTTP_BASE_URL}/mobile.html"
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "MizsoftTestHarness/1.0"})
            with urllib.request.urlopen(req, timeout=5) as resp:
                self.assertEqual(resp.status, 200, f"Expected 200 from {url}, got {resp.status}")
                body = resp.read().decode("utf-8")
                self.assertIn("Mizsoft", body, "Response body does not contain 'Mizsoft'")
        except urllib.error.URLError as e:
            self.fail(f"Failed to connect to local HTTP server at {url}: {e.reason}")

    def test_local_css_resources_accessible(self):
        """Verify all local CSS files linked in index.html and mobile.html exist and return 200 OK."""
        css_files = set()
        for html_file in [INDEX_HTML_PATH, MOBILE_HTML_PATH]:
            soup = BeautifulSoup(read_file(html_file), "html.parser")
            for link in soup.find_all("link", rel="stylesheet"):
                href = link.get("href", "")
                if href and not href.startswith("http") and not href.startswith("//"):
                    css_files.add(href.split("?")[0])

        self.assertGreater(len(css_files), 0, "No local CSS files found in HTML")

        for css_rel in css_files:
            file_path = WORKSPACE_DIR / css_rel
            self.assertTrue(file_path.exists(), f"CSS file does not exist on disk: {file_path}")

            # Verify HTTP server response
            url = f"{HTTP_BASE_URL}/{css_rel}"
            try:
                with urllib.request.urlopen(url, timeout=5) as resp:
                    self.assertEqual(resp.status, 200, f"CSS file HTTP status is {resp.status} for {url}")
            except urllib.error.URLError as e:
                self.fail(f"Could not fetch CSS file via HTTP {url}: {e.reason}")

    def test_local_js_resources_accessible(self):
        """Verify all local JS files linked in index.html and mobile.html exist and return 200 OK."""
        js_files = set()
        for html_file in [INDEX_HTML_PATH, MOBILE_HTML_PATH]:
            soup = BeautifulSoup(read_file(html_file), "html.parser")
            for script in soup.find_all("script", src=True):
                src = script.get("src", "")
                if src and not src.startswith("http") and not src.startswith("//"):
                    js_files.add(src.split("?")[0])

        self.assertGreater(len(js_files), 0, "No local JS files found in HTML")

        for js_rel in js_files:
            file_path = WORKSPACE_DIR / js_rel
            self.assertTrue(file_path.exists(), f"JS file does not exist on disk: {file_path}")

            # Verify HTTP server response
            url = f"{HTTP_BASE_URL}/{js_rel}"
            try:
                with urllib.request.urlopen(url, timeout=5) as resp:
                    self.assertEqual(resp.status, 200, f"JS file HTTP status is {resp.status} for {url}")
            except urllib.error.URLError as e:
                self.fail(f"Could not fetch JS file via HTTP {url}: {e.reason}")

    def test_standalone_js_syntax_integrity(self):
        """Verify all JS files in js/ pass Node syntax check (node -c)."""
        js_dir = WORKSPACE_DIR / "js"
        js_files = list(js_dir.glob("*.js"))
        self.assertGreater(len(js_files), 0, "No JS files found in js/ directory")

        for js_file in js_files:
            res = subprocess.run(["node", "-c", str(js_file)], capture_output=True, text=True)
            self.assertEqual(
                res.returncode,
                0,
                f"Syntax error in JS file {js_file.name}: {res.stderr}"
            )

    def test_inline_scripts_syntax_integrity(self):
        """Verify all inline script tags in index.html and mobile.html have valid JS syntax."""
        for html_file in [INDEX_HTML_PATH, MOBILE_HTML_PATH]:
            soup = BeautifulSoup(read_file(html_file), "html.parser")
            inline_scripts = [s.string for s in soup.find_all("script") if not s.get("src") and s.string]

            for idx, script_content in enumerate(inline_scripts, 1):
                res = subprocess.run(
                    ["node", "--input-type=module", "-c"],
                    input=script_content,
                    capture_output=True,
                    text=True
                )
                # If module parse fails, fallback to commonjs check
                if res.returncode != 0:
                    res_cjs = subprocess.run(
                        ["node", "--check"],
                        input=script_content,
                        capture_output=True,
                        text=True
                    )
                    self.assertEqual(
                        res_cjs.returncode,
                        0,
                        f"Syntax error in inline script #{idx} of {html_file.name}: {res_cjs.stderr}"
                    )


if __name__ == "__main__":
    unittest.main(verbosity=2)
