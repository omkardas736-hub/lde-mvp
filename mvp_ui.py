#1
# mvp_ui.py
import os
import sys
import threading

from kivy.lang import Builder
from kivy.clock import Clock, mainthread
from kivy.core.window import Window
from kivy.graphics import Color, Line

from kivymd.app import MDApp

# Ensure local imports work in Pydroid
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mvp_core as core  # step A completed core

KV = """
#:import MDNavigationLayout kivymd.uix.navigationdrawer.MDNavigationLayout
#:import MDScreen kivymd.uix.screen.MDScreen
#:import MDScreenManager kivymd.uix.screenmanager.MDScreenManager
#:import MDBoxLayout kivymd.uix.boxlayout.MDBoxLayout
#:import MDTopAppBar kivymd.uix.toolbar.MDTopAppBar
#:import MDRaisedButton kivymd.uix.button.MDRaisedButton
#:import MDLabel kivymd.uix.label.MDLabel
#:import MDTextField kivymd.uix.textfield.MDTextField
#:import MDNavigationDrawer kivymd.uix.navigationdrawer.MDNavigationDrawer

MDScreenManager:
    id: root_sm

    # ---------------- Home ----------------
    MDScreen:
        name: "home"

        MDNavigationLayout:
            id: home_right_layer

            MDNavigationLayout:
                id: home_left_layer

                MDScreen:
                    MDBoxLayout:
                        orientation: "vertical"
                        md_bg_color: 0.9, 0.95, 1, 1

                        MDTopAppBar:
                            title: "LDE App"
                            elevation: 2
                            pos_hint: {"top": 1}
                            left_action_items: [["menu", lambda x: home_left_drawer.set_state("open")]]
                            right_action_items: [["dots-vertical", lambda x: home_right_drawer.set_state("open")]]

                        MDBoxLayout:
                            orientation: "vertical"
                            spacing: "16dp"
                            padding: "24dp"

                            MDLabel:
                                text: "Welcome to LDE"
                                halign: "center"
                                font_style: "H5"

                            MDRaisedButton:
                                text: "Learning (VSTS)"
                                pos_hint: {"center_x": 0.5}
                                on_release: app.goto_learning()

                            MDRaisedButton:
                                text: "Developer Terminal"
                                pos_hint: {"center_x": 0.5}
                                on_release: app.goto_terminal()

                            MDRaisedButton:
                                text: "Earnings Dashboard"
                                pos_hint: {"center_x": 0.5}
                                on_release: app.goto_earnings()

                MDNavigationDrawer:
                    id: home_left_drawer
                    radius: (0, 16, 16, 0)
                    anchor: "left"
                    MDBoxLayout:
                        orientation: "vertical"
                        padding: "16dp"
                        spacing: "12dp"

                        MDLabel:
                            text: "Home Menu"
                            font_style: "H6"

                        MDRaisedButton:
                            text: "Learning"
                            on_release:
                                home_left_drawer.set_state("close")
                                app.goto_learning()

                        MDRaisedButton:
                            text: "Terminal"
                            on_release:
                                home_left_drawer.set_state("close")
                                app.goto_terminal()

                        MDRaisedButton:
                            text: "Earnings"
                            on_release:
                                home_left_drawer.set_state("close")
                                app.goto_earnings()

            MDNavigationDrawer:
                id: home_right_drawer
                radius: (16, 0, 0, 16)
                anchor: "right"
                MDBoxLayout:
                    orientation: "vertical"
                    padding: "16dp"
                    spacing: "12dp"
                    MDLabel:
                        text: "About / Settings"
                        font_style: "H6"
                    MDLabel:
                        text: "Theme, Privacy, Version"

    # --------------- Learning ---------------
    MDScreen:
        name: "learning"

        MDNavigationLayout:
            id: learning_right_layer

            MDNavigationLayout:
                id: learning_left_layer

                MDScreen:
                    MDBoxLayout:
                        orientation: "vertical"
                        md_bg_color: 0.9, 0.95, 1, 1

                        MDTopAppBar:
                            title: "Learning"
                            elevation: 2
                            pos_hint: {"top": 1}
                            left_action_items: [["menu", lambda x: learning_left_drawer.set_state("open")]]
                            right_action_items: [["menu", lambda x: learning_right_drawer.set_state("open")]]

                        MDBoxLayout:
                            orientation: "vertical"
                            padding: "16dp"
                            spacing: "12dp"

                            MDLabel:
                                text: "Explainer"
                                halign: "center"
                                font_style: "H6"

                            MDTextField:
                                id: style_input
                                hint_text: "Style (simple / detailed / compare)"
                                text: "simple"

                            MDTextField:
                                id: question_input
                                hint_text: "Type your question (e.g., what is python)"

                            MDRaisedButton:
                                text: "Explainer"
                                pos_hint: {"center_x": 0.5}
                                on_release: app.learning_explainer(style_input.text, question_input.text)

                            MDLabel:
                                id: learning_answer
                                text: ""
                                halign: "center"

                            MDRaisedButton:
                                text: "Back to Home"
                                pos_hint: {"center_x": 0.5}
                                on_release: app.goto_home()

                MDNavigationDrawer:
                    id: learning_left_drawer
                    radius: (0, 16, 16, 0)
                    anchor: "left"
                    MDBoxLayout:
                        orientation: "vertical"
                        padding: "16dp"
                        spacing: "8dp"

                        MDLabel:
                            text: "Chats"
                            font_style: "H6"

                        MDBoxLayout:
                            id: chat_list_box
                            orientation: "vertical"
                            spacing: "6dp"

                        MDRaisedButton:
                            text: "Refresh Chats"
                            on_release: app.learning_refresh_chats()

                        MDLabel:
                            text: "Tap a chat to open (stub)."

            MDNavigationDrawer:
                id: learning_right_drawer
                radius: (16, 0, 0, 16)
                anchor: "right"
                MDBoxLayout:
                    orientation: "vertical"
                    padding: "16dp"
                    spacing: "8dp"

                    MDLabel:
                        text: "Learning Dashboard"
                        font_style: "H6"

                    MDLabel:
                        id: learn_msg_stats
                        text: "Messages: 0 used, 0 remaining"

                    MDLabel:
                        id: learn_power_stats
                        text: "Plan: free (exp: -)"

                    MDLabel:
                        id: learn_rom_label
                        text: "Virtual ROM: -"

                    MDLabel:
                        id: learn_ram_label
                        text: "Virtual RAM: -"

                    MDLabel:
                        id: learn_cpu_label
                        text: "CPU Priority: -"

                    MDRaisedButton:
                        text: "Contribute Battery (Mock)"
                        on_release: app.learning_contribute_battery()

                    MDRaisedButton:
                        text: "Upgrade to Pro (Mock)"
                        on_release: app.learning_upgrade_pro()

                    MDRaisedButton:
                        text: "Back to Free"
                        on_release: app.learning_back_free()

    # --------------- Terminal ---------------
    MDScreen:
        name: "terminal"

        MDNavigationLayout:
            id: terminal_right_layer

            MDNavigationLayout:
                id: terminal_left_layer

                MDScreen:
                    MDBoxLayout:
                        orientation: "vertical"
                        md_bg_color: 0.9, 0.95, 1, 1

                        MDTopAppBar:
                            title: "Terminal"
                            elevation: 2
                            pos_hint: {"top": 1}
                            left_action_items: [["menu", lambda x: terminal_left_drawer.set_state("open")]]
                            right_action_items: [["menu", lambda x: terminal_right_drawer.set_state("open")]]

                        MDBoxLayout:
                            orientation: "vertical"
                            padding: "16dp"
                            spacing: "12dp"

                            MDLabel:
                                text: "Console actions"
                                halign: "center"

                            MDRaisedButton:
                                text: "Open Developer Console"
                                pos_hint: {"center_x": 0.5}
                                on_release: app.run_terminal()

                            MDRaisedButton:
                                text: "Run FPS (Threaded)"
                                pos_hint: {"center_x": 0.5}
                                on_release: app.run_fps_thread()

                            MDRaisedButton:
                                text: "Run DPS (Threaded)"
                                pos_hint: {"center_x": 0.5}
                                on_release: app.run_dps_thread()

                            MDRaisedButton:
                                text: "Stress Test"
                                pos_hint: {"center_x": 0.5}
                                on_release: app.terminal_run_stress()

                            MDRaisedButton:
                                text: "Back to Home"
                                pos_hint: {"center_x": 0.5}
                                on_release: app.goto_home()

                MDNavigationDrawer:
                    id: terminal_left_drawer
                    radius: (0, 16, 16, 0)
                    anchor: "left"
                    MDBoxLayout:
                        orientation: "vertical"
                        padding: "16dp"
                        spacing: "8dp"

                        MDLabel:
                            text: "Available Files"
                            font_style: "H6"

                        MDBoxLayout:
                            id: files_list_box
                            orientation: "vertical"
                            spacing: "6dp"

                        MDRaisedButton:
                            text: "Refresh Files"
                            on_release: app.terminal_refresh_files()

                        MDLabel:
                            text: "Tap a file to set path (stub)."

            MDNavigationDrawer:
                id: terminal_right_drawer
                radius: (16, 0, 0, 16)
                anchor: "right"
                MDBoxLayout:
                    orientation: "vertical"
                    padding: "16dp"
                    spacing: "8dp"

                    MDLabel:
                        text: "Developer Dashboard"
                        font_style: "H6"

                    MDLabel:
                        id: term_res_label
                        text: "Resources: -"

                    MDLabel:
                        id: dev_fps_stats
                        text: "FPS: 0 files processed"

                    MDLabel:
                        id: dev_dps_stats
                        text: "DPS: last run none"

                    MDRaisedButton:
                        text: "Update Stats"
                        on_release: app.terminal_update_dashboard()

    # --------------- Earnings ---------------
    MDScreen:
        name: "earnings"
        MDBoxLayout:
            orientation: "vertical"
            md_bg_color: 0.9, 0.95, 1, 1

            MDTopAppBar:
                title: "Earnings"
                elevation: 2
                pos_hint: {"top": 1}
                left_action_items: [["arrow-left", lambda x: app.goto_home()]]

            MDBoxLayout:
                orientation: "vertical"
                padding: "16dp"
                spacing: "12dp"

                MDLabel:
                    id: credits_label
                    text: "Credits: 0"
                    halign: "center"

                MDRaisedButton:
                    text: "Process Data Service"
                    pos_hint: {"center_x": 0.5}
                    on_release: app.earnings_process_service()

                MDLabel:
                    id: service_info
                    text: ""

                MDLabel:
                    id: today_label
                    text: "Today: read 0 MB, written 0 MB"

                MDRaisedButton:
                    text: "View last 7 days"
                    pos_hint: {"center_x": 0.5}
                    on_release: app.earnings_show_7days()

                MDLabel:
                    id: history_label
                    text: ""
"""

class MVPApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.primary_hue = "700"

        root = Builder.load_string(KV)

        Clock.schedule_once(self._add_border, 0)
        Clock.schedule_interval(self._update_border, 0.25)

        # Initial UI refreshes
        Clock.schedule_once(lambda dt: self.refresh_credits(), 0.3)
        Clock.schedule_once(lambda dt: self.learning_update_dashboard(), 0.4)
        Clock.schedule_once(lambda dt: self.terminal_refresh_files(), 0.5)
        Clock.schedule_once(lambda dt: self.terminal_update_resources(), 0.6)
        Clock.schedule_once(lambda dt: self.earnings_update_today(), 0.7)
        return root

    def _add_border(self, dt):
        try:
            Window.canvas.after.clear()
            with Window.canvas.after:
                Color(1, 0, 0, 1)
                self._border = Line(rectangle=(1, 1, Window.width - 2, Window.height - 2), width=1.0)
            Window.bind(size=self._update_border, pos=self._update_border)
            self._update_border()
        except Exception:
            pass

    def _update_border(self, *args):
        try:
            if hasattr(self, "_border") and self._border:
                self._border.rectangle = (1, 1, Window.width - 2, Window.height - 2)
        except Exception:
            pass

    # Navigation
    def goto_home(self):
        try:
            self.root.ids.root_sm.current = "home"
        except Exception:
            pass

    def goto_learning(self):
        try:
            self.root.ids.root_sm.current = "learning"
            Clock.schedule_once(lambda dt: self.learning_update_dashboard(), 0.1)
        except Exception:
            pass

    def goto_terminal(self):
        try:
            self.root.ids.root_sm.current = "terminal"
            Clock.schedule_once(lambda dt: self.terminal_update_dashboard(), 0.1)
            Clock.schedule_once(lambda dt: self.terminal_update_resources(), 0.15)
        except Exception:
            pass

    def goto_earnings(self):
        try:
            self.root.ids.root_sm.current = "earnings"
            self.refresh_credits()
            Clock.schedule_once(lambda dt: self.earnings_update_today(), 0.1)
        except Exception:
            pass

    # Learning
    def learning_explainer(self, style_text, question_text):
        msg = core.explainer_answer(style_text, question_text)
        try:
            scr = self.root.ids.root_sm.get_screen("learning")
            scr.ids.learning_answer.text = msg
            self.learning_update_dashboard()
        except Exception:
            pass

    def learning_refresh_chats(self):
        try:
            scr = self.root.ids.root_sm.get_screen("learning")
            box = scr.ids.get("chat_list_box")
            if not box:
                return
            box.clear_widgets()
            from kivymd.uix.button import MDRaisedButton
            chats = ["Welcome chat", "Python basics", "Hackathon tips"]
            for title in chats:
                btn = MDRaisedButton(text=title, size_hint_x=1)
                def _cb(inst, t=title):
                    self._open_chat_stub(t)
                btn.bind(on_release=_cb)
                box.add_widget(btn)
        except Exception:
            pass

    def _open_chat_stub(self, title):
        try:
            scr = self.root.ids.root_sm.get_screen("learning")
            scr.ids.learning_answer.text = f"Opened chat: {title}"
        except Exception:
            pass

    def _format_resources(self):
        try:
            res = core.get_effective_resources()
            wr_mb, rd_mb = core.get_mb_today()
            tier = core.get_tier()
            exp = core.STATE["contribution"].get("entitlement_expires")
            used = core.STATE["usage_counters"]["messages_used_today"]
            cap = res["daily_cap"]
            return {
                "tier": tier, "expiry": exp or "-",
                "used": used, "remaining": max(0, cap - used),
                "rom": res["workspace_cache_mb"], "ram": res["processing_memory_mb"],
                "cpu": res["cpu_priority"], "read_mb": rd_mb, "write_mb": wr_mb
            }
        except Exception:
            return {"tier":"free","expiry":"-","used":0,"remaining":0,"rom":0,"ram":0,"cpu":"-","read_mb":0,"write_mb":0}

    def learning_update_dashboard(self):
        try:
            scr = self.root.ids.root_sm.get_screen("learning")
            m = self._format_resources()
            scr.ids.learn_msg_stats.text = f"Messages: {m['used']} used, {m['remaining']} remaining"
            scr.ids.learn_power_stats.text = f"Plan: {m['tier']} (exp: {m['expiry']})"
            if scr.ids.get("learn_rom_label"):
                scr.ids.learn_rom_label.text = f"Virtual ROM: {m['read_mb']} MB read today / {m['rom']} MB"
            if scr.ids.get("learn_ram_label"):
                scr.ids.learn_ram_label.text = f"Virtual RAM: {m['ram']} MB reserved"
            if scr.ids.get("learn_cpu_label"):
                scr.ids.learn_cpu_label.text = f"CPU Priority: {m['cpu']}"
        except Exception:
            pass

    def learning_contribute_battery(self):
        try:
            core.simulate_battery_contribution(18)
            self.learning_update_dashboard()
        except Exception:
            pass

    def learning_upgrade_pro(self):
        try:
            core.set_tier("pro")
            self.learning_update_dashboard()
        except Exception:
            pass

def learning_back_
