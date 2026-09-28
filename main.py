"""
MINE Store - KivyMD E-commerce App
A dark-themed, modern shopping app with Home, Product Detail, Cart and
Checkout screens.
"""

from kivy.core.window import Window
from kivy.metrics import dp
from kivy.properties import NumericProperty, StringProperty
from kivy.uix.scrollview import ScrollView

from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton, MDFlatButton, MDIconButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.dialog import MDDialog
from kivymd.uix.snackbar import Snackbar

try:
    from kivymd.uix.divider import MDDivider
except Exception:
    MDDivider = None


# ---------------------------------------------------------------------------
# Product catalogue
# ---------------------------------------------------------------------------
PRODUCTS = [
    {"id": 1, "name": "Classic Crew Tee", "category": "Clothes", "price": 19.99,
     "icon": "tshirt-crew", "desc": "Soft 100% cotton crew-neck t-shirt. "
     "A wardrobe essential, available in multiple colors and built to last "
     "wash after wash."},
    {"id": 2, "name": "Denim Jacket", "category": "Clothes", "price": 59.99,
     "icon": "hanger", "desc": "Timeless denim jacket with a relaxed fit. "
     "Perfect layering piece for spring and autumn days."},
    {"id": 3, "name": "Hooded Sweatshirt", "category": "Clothes", "price": 34.99,
     "icon": "tshirt-v", "desc": "Cozy fleece-lined hoodie with an adjustable "
     "drawstring hood and a spacious front pocket."},
    {"id": 4, "name": "Running Sneakers", "category": "Shoes", "price": 79.99,
     "icon": "shoe-sneaker", "desc": "Lightweight running sneakers with "
     "breathable mesh uppers and responsive cushioning for daily miles."},
    {"id": 5, "name": "Leather Loafers", "category": "Shoes", "price": 89.99,
     "icon": "shoe-formal", "desc": "Handcrafted leather loafers combining "
     "classic style with all-day comfort."},
    {"id": 6, "name": "High Heel Pumps", "category": "Shoes", "price": 64.99,
     "icon": "shoe-heel", "desc": "Elegant high heel pumps designed for both "
     "comfort and standout style at any occasion."},
    {"id": 7, "name": "Wireless Headphones", "category": "Gadgets", "price": 129.99,
     "icon": "headphones", "desc": "Over-ear wireless headphones with active "
     "noise cancellation and 30-hour battery life."},
    {"id": 8, "name": "Smart Watch", "category": "Gadgets", "price": 149.99,
     "icon": "watch-variant", "desc": "Track your fitness, notifications and "
     "heart rate with this sleek always-on display smart watch."},
    {"id": 9, "name": "Bluetooth Speaker", "category": "Gadgets", "price": 49.99,
     "icon": "speaker-wireless", "desc": "Portable waterproof Bluetooth "
     "speaker with rich bass and 12 hours of playtime."},
    {"id": 10, "name": "4K Action Camera", "category": "Gadgets", "price": 199.99,
     "icon": "camera", "desc": "Capture every adventure in stunning 4K with "
     "this rugged, waterproof action camera."},
    {"id": 11, "name": "Slim Fit Chinos", "category": "Clothes", "price": 44.99,
     "icon": "human-male", "desc": "Comfortable stretch-cotton chinos with a "
     "modern slim fit, great for work or weekends."},
    {"id": 12, "name": "Canvas High-Tops", "category": "Shoes", "price": 39.99,
     "icon": "shoe-sneaker", "desc": "Retro-style canvas high-top sneakers "
     "that pair with just about anything."},
]

CATEGORIES = ["All", "Clothes", "Shoes", "Gadgets"]


def get_app():
    return MDApp.get_running_app()


# ---------------------------------------------------------------------------
# Reusable widgets
# ---------------------------------------------------------------------------
class ProductCard(MDCard):
    def __init__(self, product, **kwargs):
        super().__init__(**kwargs)
        self.product = product
        self.orientation = "vertical"
        self.padding = dp(12)
        self.spacing = dp(6)
        self.size_hint = (1, None)
        self.height = dp(220)
        self.radius = [18, 18, 18, 18]
        self.elevation = 2
        self.md_bg_color = get_app().theme_cls.bg_light
        self.ripple_behavior = True
        self.on_release = lambda *a: get_app().open_product_detail(product)

        icon_box = MDBoxLayout(size_hint=(1, None), height=dp(100))
        icon_widget = MDIconButton(
            icon=product["icon"],
            theme_text_color="Custom",
            text_color=get_app().theme_cls.primary_color,
            icon_size=dp(56),
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            disabled=True,
        )
        icon_box.add_widget(icon_widget)
        self.add_widget(icon_box)

        name_lbl = MDLabel(
            text=product["name"],
            font_style="Subtitle1",
            bold=True,
            halign="center",
            size_hint_y=None,
            height=dp(24),
        )
        self.add_widget(name_lbl)

        price_lbl = MDLabel(
            text=f"${product['price']:.2f}",
            halign="center",
            theme_text_color="Custom",
            text_color=get_app().theme_cls.primary_color,
            size_hint_y=None,
            height=dp(22),
        )
        self.add_widget(price_lbl)

        add_btn = MDRaisedButton(
            text="ADD TO CART",
            size_hint=(1, None),
            height=dp(36),
            md_bg_color=get_app().theme_cls.accent_color,
        )
        add_btn.bind(on_release=lambda *a: get_app().add_to_cart(product))
        self.add_widget(add_btn)


class CartRow(MDCard):
    def __init__(self, item, **kwargs):
        super().__init__(**kwargs)
        self.item = item
        product = item["product"]
        self.orientation = "horizontal"
        self.padding = dp(10)
        self.spacing = dp(10)
        self.size_hint = (1, None)
        self.height = dp(96)
        self.radius = [14, 14, 14, 14]
        self.elevation = 1
        self.md_bg_color = get_app().theme_cls.bg_light

        icon_widget = MDIconButton(
            icon=product["icon"],
            theme_text_color="Custom",
            text_color=get_app().theme_cls.primary_color,
            icon_size=dp(40),
            disabled=True,
        )
        self.add_widget(icon_widget)

        info_box = MDBoxLayout(orientation="vertical", spacing=dp(2))
        info_box.add_widget(MDLabel(text=product["name"], bold=True,
                                     shorten=True, shorten_from="right"))
        info_box.add_widget(MDLabel(
            text=f"${product['price']:.2f} each",
            theme_text_color="Secondary",
            font_style="Caption",
        ))
        self.add_widget(info_box)

        qty_box = MDBoxLayout(orientation="horizontal", size_hint=(None, 1),
                               width=dp(120), spacing=dp(2))
        minus_btn = MDIconButton(icon="minus-circle-outline")
        minus_btn.bind(on_release=lambda *a: get_app().change_qty(product["id"], -1))
        self.qty_label = MDLabel(text=str(item["qty"]), halign="center",
                                  size_hint=(None, 1), width=dp(30))
        plus_btn = MDIconButton(icon="plus-circle-outline")
        plus_btn.bind(on_release=lambda *a: get_app().change_qty(product["id"], 1))
        qty_box.add_widget(minus_btn)
        qty_box.add_widget(self.qty_label)
        qty_box.add_widget(plus_btn)
        self.add_widget(qty_box)

        remove_btn = MDIconButton(icon="trash-can-outline",
                                   theme_text_color="Custom",
                                   text_color=(1, 0.4, 0.4, 1))
        remove_btn.bind(on_release=lambda *a: get_app().remove_from_cart(product["id"]))
        self.add_widget(remove_btn)


# ---------------------------------------------------------------------------
# Screens
# ---------------------------------------------------------------------------
class HomeScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "home"
        self.current_category = "All"
        self.search_text = ""
        self._build_ui()

    def _build_ui(self):
        root = MDBoxLayout(orientation="vertical")

        self.toolbar = MDTopAppBar(
            title="MINE Store",
            elevation=4,
            left_action_items=[["store", lambda x: None]],
            right_action_items=[["cart-outline", lambda x: get_app().open_cart()]],
        )
        root.add_widget(self.toolbar)

        search_box = MDBoxLayout(
            size_hint=(1, None), height=dp(56),
            padding=(dp(12), dp(6)),
        )
        self.search_field = MDTextField(
            hint_text="Search products...",
            icon_left="magnify",
            mode="round",
        )
        self.search_field.bind(text=self._on_search)
        search_box.add_widget(self.search_field)
        root.add_widget(search_box)

        cat_box = MDBoxLayout(
            size_hint=(1, None), height=dp(48),
            padding=(dp(8), 0), spacing=dp(6),
        )
        self.cat_buttons = {}
        for cat in CATEGORIES:
            btn = MDFlatButton(
                text=cat,
                on_release=lambda inst, c=cat: self._select_category(c),
            )
            self.cat_buttons[cat] = btn
            cat_box.add_widget(btn)
        root.add_widget(cat_box)

        self.scroll = ScrollView()
        self.grid = MDGridLayout(cols=2, spacing=dp(12), padding=dp(12),
                                  size_hint_y=None)
        self.grid.bind(minimum_height=self.grid.setter("height"))
        self.scroll.add_widget(self.grid)
        root.add_widget(self.scroll)

        self.add_widget(root)
        self._highlight_category()
        self.populate_grid()

    def _highlight_category(self):
        app = get_app()
        for cat, btn in self.cat_buttons.items():
            if cat == self.current_category:
                btn.theme_text_color = "Custom"
                btn.text_color = app.theme_cls.primary_color
            else:
                btn.theme_text_color = "Primary"

    def _select_category(self, cat):
        self.current_category = cat
        self._highlight_category()
        self.populate_grid()

    def _on_search(self, instance, value):
        self.search_text = value.strip().lower()
        self.populate_grid()

    def populate_grid(self):
        self.grid.clear_widgets()
        for product in PRODUCTS:
            if self.current_category != "All" and product["category"] != self.current_category:
                continue
            if self.search_text and self.search_text not in product["name"].lower():
                continue
            self.grid.add_widget(ProductCard(product, size_hint_x=1))
        if not self.grid.children:
            self.grid.add_widget(
                MDLabel(text="No products found.", halign="center",
                         size_hint_y=None, height=dp(80))
            )

    def on_pre_enter(self, *args):
        self.populate_grid()


class ProductDetailScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "detail"
        self.product = None
        self.qty = 1
        self._build_ui()

    def _build_ui(self):
        self.root_box = MDBoxLayout(orientation="vertical")

        self.toolbar = MDTopAppBar(
            title="Product Details",
            elevation=4,
            left_action_items=[["arrow-left", lambda x: get_app().go_back("home")]],
            right_action_items=[["cart-outline", lambda x: get_app().open_cart()]],
        )
        self.root_box.add_widget(self.toolbar)

        scroll = ScrollView()
        self.content = MDBoxLayout(orientation="vertical", spacing=dp(14),
                                    padding=dp(20), size_hint_y=None)
        self.content.bind(minimum_height=self.content.setter("height"))
        scroll.add_widget(self.content)
        self.root_box.add_widget(scroll)

        self.add_widget(self.root_box)

    def set_product(self, product):
        self.product = product
        self.qty = 1
        self.content.clear_widgets()

        icon_card = MDCard(size_hint=(1, None), height=dp(220),
                            radius=[20, 20, 20, 20], elevation=2,
                            md_bg_color=get_app().theme_cls.bg_light)
        icon_widget = MDIconButton(
            icon=product["icon"],
            theme_text_color="Custom",
            text_color=get_app().theme_cls.primary_color,
            icon_size=dp(96),
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            disabled=True,
        )
        icon_card.add_widget(icon_widget)
        self.content.add_widget(icon_card)

        self.content.add_widget(MDLabel(
            text=product["name"], font_style="H5", bold=True,
            size_hint_y=None, height=dp(40),
        ))
        self.content.add_widget(MDLabel(
            text=product["category"], theme_text_color="Secondary",
            size_hint_y=None, height=dp(24),
        ))
        self.content.add_widget(MDLabel(
            text=f"${product['price']:.2f}", font_style="H6",
            theme_text_color="Custom", text_color=get_app().theme_cls.primary_color,
            size_hint_y=None, height=dp(36),
        ))
        if MDDivider:
            self.content.add_widget(MDDivider())
        desc_label = MDLabel(
            text=product["desc"], theme_text_color="Secondary",
            size_hint_y=None,
        )
        desc_label.bind(
            width=lambda inst, val: setattr(inst, "text_size", (val, None)),
            texture_size=lambda inst, val: setattr(inst, "height", val[1]),
        )
        self.content.add_widget(desc_label)

        qty_row = MDBoxLayout(size_hint=(1, None), height=dp(48), spacing=dp(12))
        qty_row.add_widget(MDLabel(text="Quantity", size_hint_x=0.5))
        minus_btn = MDIconButton(icon="minus-circle-outline")
        minus_btn.bind(on_release=lambda *a: self._change_qty(-1))
        self.qty_label = MDLabel(text=str(self.qty), halign="center")
        plus_btn = MDIconButton(icon="plus-circle-outline")
        plus_btn.bind(on_release=lambda *a: self._change_qty(1))
        qty_row.add_widget(minus_btn)
        qty_row.add_widget(self.qty_label)
        qty_row.add_widget(plus_btn)
        self.content.add_widget(qty_row)

        add_btn = MDRaisedButton(
            text="ADD TO CART", size_hint=(1, None), height=dp(48),
            md_bg_color=get_app().theme_cls.accent_color,
        )
        add_btn.bind(on_release=lambda *a: self._add_to_cart())
        self.content.add_widget(add_btn)

        buy_btn = MDFlatButton(
            text="BUY NOW", size_hint=(1, None), height=dp(48),
        )
        buy_btn.bind(on_release=lambda *a: self._buy_now())
        self.content.add_widget(buy_btn)

    def _change_qty(self, delta):
        self.qty = max(1, self.qty + delta)
        self.qty_label.text = str(self.qty)

    def _add_to_cart(self):
        get_app().add_to_cart(self.product, self.qty)

    def _buy_now(self):
        get_app().add_to_cart(self.product, self.qty)
        get_app().open_checkout()


class CartScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "cart"
        self._build_ui()

    def _build_ui(self):
        root = MDBoxLayout(orientation="vertical")

        self.toolbar = MDTopAppBar(
            title="Your Cart",
            elevation=4,
            left_action_items=[["arrow-left", lambda x: get_app().go_back("home")]],
        )
        root.add_widget(self.toolbar)

        self.scroll = ScrollView()
        self.list_box = MDBoxLayout(orientation="vertical", spacing=dp(10),
                                     padding=dp(12), size_hint_y=None)
        self.list_box.bind(minimum_height=self.list_box.setter("height"))
        self.scroll.add_widget(self.list_box)
        root.add_widget(self.scroll)

        bottom = MDBoxLayout(orientation="vertical", size_hint=(1, None),
                              height=dp(110), padding=dp(16), spacing=dp(8))
        self.total_label = MDLabel(text="Total: $0.00", font_style="H6", bold=True)
        bottom.add_widget(self.total_label)
        checkout_btn = MDRaisedButton(
            text="PROCEED TO CHECKOUT", size_hint=(1, None), height=dp(48),
            md_bg_color=get_app().theme_cls.accent_color,
        )
        checkout_btn.bind(on_release=lambda *a: get_app().open_checkout())
        bottom.add_widget(checkout_btn)
        root.add_widget(bottom)

        self.add_widget(root)

    def refresh(self):
        self.list_box.clear_widgets()
        app = get_app()
        if not app.cart:
            self.list_box.add_widget(
                MDLabel(text="Your cart is empty.", halign="center",
                         size_hint_y=None, height=dp(80))
            )
        else:
            for item in app.cart:
                self.list_box.add_widget(CartRow(item, size_hint=(1, None)))
        self.total_label.text = f"Total: ${app.cart_total():.2f}"

    def on_pre_enter(self, *args):
        self.refresh()


class CheckoutScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "checkout"
        self.dialog = None
        self._build_ui()

    def _build_ui(self):
        root = MDBoxLayout(orientation="vertical")

        self.toolbar = MDTopAppBar(
            title="Checkout",
            elevation=4,
            left_action_items=[["arrow-left", lambda x: get_app().go_back("cart")]],
        )
        root.add_widget(self.toolbar)

        scroll = ScrollView()
        form = MDBoxLayout(orientation="vertical", spacing=dp(16),
                            padding=dp(20), size_hint_y=None)
        form.bind(minimum_height=form.setter("height"))

        self.name_field = MDTextField(hint_text="Full Name", mode="rectangle")
        self.address_field = MDTextField(hint_text="Delivery Address", mode="rectangle")
        self.city_field = MDTextField(hint_text="City", mode="rectangle")
        self.phone_field = MDTextField(hint_text="Phone Number",
                                        input_filter="int", mode="rectangle")

        for f in (self.name_field, self.address_field, self.city_field, self.phone_field):
            form.add_widget(f)

        self.summary_label = MDLabel(
            text="", theme_text_color="Secondary", size_hint_y=None, height=dp(40),
        )
        form.add_widget(self.summary_label)

        place_btn = MDRaisedButton(
            text="PLACE ORDER", size_hint=(1, None), height=dp(50),
            md_bg_color=get_app().theme_cls.accent_color,
        )
        place_btn.bind(on_release=lambda *a: self._place_order())
        form.add_widget(place_btn)

        scroll.add_widget(form)
        root.add_widget(scroll)
        self.add_widget(root)

    def on_pre_enter(self, *args):
        app = get_app()
        count = sum(i["qty"] for i in app.cart)
        self.summary_label.text = (
            f"{count} item(s) in cart  •  Total: ${app.cart_total():.2f}"
        )

    def _place_order(self):
        app = get_app()
        if not app.cart:
            Snackbar(text="Your cart is empty.").open()
            return
        if not self.name_field.text.strip() or not self.address_field.text.strip():
            Snackbar(text="Please fill in your name and address.").open()
            return

        name = self.name_field.text.strip()
        self.dialog = MDDialog(
            title="Order Placed!",
            text=(f"Thank you, {name}! Your order totaling "
                  f"${app.cart_total():.2f} has been placed successfully."),
            buttons=[MDFlatButton(text="OK", on_release=self._close_dialog)],
        )
        self.dialog.open()
        app.clear_cart()
        self.name_field.text = ""
        self.address_field.text = ""
        self.city_field.text = ""
        self.phone_field.text = ""

    def _close_dialog(self, *args):
        if self.dialog:
            self.dialog.dismiss()
        get_app().go_back("home")


# ---------------------------------------------------------------------------
# Main App
# ---------------------------------------------------------------------------
class MineStoreApp(MDApp):
    def build(self):
        self.title = "MINE Store"
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Teal"
        self.theme_cls.accent_palette = "Amber"
        Window.softinput_mode = "below_target"

        self.cart = []  # list of {"product": dict, "qty": int}
        self._last_screen = "home"

        self.sm = MDScreenManager()
        self.home_screen = HomeScreen()
        self.detail_screen = ProductDetailScreen()
        self.cart_screen = CartScreen()
        self.checkout_screen = CheckoutScreen()

        self.sm.add_widget(self.home_screen)
        self.sm.add_widget(self.detail_screen)
        self.sm.add_widget(self.cart_screen)
        self.sm.add_widget(self.checkout_screen)

        return self.sm

    # -- navigation helpers --------------------------------------------
    def open_product_detail(self, product):
        self._last_screen = self.sm.current
        self.detail_screen.set_product(product)
        self.sm.current = "detail"

    def open_cart(self):
        self._last_screen = self.sm.current
        self.sm.current = "cart"

    def open_checkout(self):
        self._last_screen = self.sm.current
        self.sm.current = "checkout"

    def go_back(self, screen_name="home"):
        self.sm.current = screen_name

    # -- cart logic -------------------------------------------------------
    def add_to_cart(self, product, qty=1):
        for item in self.cart:
            if item["product"]["id"] == product["id"]:
                item["qty"] += qty
                Snackbar(text=f"Updated {product['name']} quantity in cart.").open()
                return
        self.cart.append({"product": product, "qty": qty})
        Snackbar(text=f"{product['name']} added to cart.").open()

    def remove_from_cart(self, product_id):
        self.cart = [i for i in self.cart if i["product"]["id"] != product_id]
        self.cart_screen.refresh()

    def change_qty(self, product_id, delta):
        for item in self.cart:
            if item["product"]["id"] == product_id:
                item["qty"] = max(1, item["qty"] + delta)
        self.cart_screen.refresh()

    def clear_cart(self):
        self.cart = []

    def cart_total(self):
        return sum(i["product"]["price"] * i["qty"] for i in self.cart)


if __name__ == "__main__":
    MineStoreApp().run()
