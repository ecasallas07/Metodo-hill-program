"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import reflex as rx

from rxconfig import config


# Back-end
class FormState(rx.State):
    form_data = {}

    def handle_submit(self, form_data: dict):
        "Handle the form submit."
        self.form_data = form_data

    ...


# Front-end
def action_bar() -> rx.Component:
    return rx.hstack(rx.input(placeholder="message encription"), rx.button("Start"))


def index() -> rx.Component:
    return rx.container(
        rx.color_mode.button(position="top-right"),
        rx.box(
            rx.vstack(
                rx.heading("Enigma machine", size="9"),
                rx.text(
                    "Decrypts hidden messages",
                    rx.text.strong(" with the hill method"),
                    size="5",
                ),
                rx.link(
                    rx.button(
                        "Start",
                        color="white",
                        background_color="#D14747",
                        border_radius="5px",
                        padding="10px",
                        margin_bottom="10px",
                        cursor="pointer",
                        font_size="25px",
                    ),
                    href="/machine",
                    is_external=False,
                ),
                spacing="5",
                justify="center",
                min_height="85vh",
                width="600px",
            ),
            rx.image(
                src="machine-image.png",
                width="500px",
                height="auto",
                margin_left="100px",
            ),
            display="flex",
            flex_direction="row",
            justify_content="space-between",
            align_items="center",
            width="1000px",
        ),
    )


def machine():
    return rx.container(
        rx.tabs.root(
            rx.tabs.list(
                rx.tabs.trigger("Decrypt", value="tab1"),
                rx.tabs.trigger("Encrypt", value="tab2"),
                display="flex",
                justify_content="center",
                margin_bottom="20px",
            ),
            rx.tabs.content(
                rx.vstack(
                    rx.form(
                        rx.heading("Discover the message", size="7", margin_bottom="20px"),
                        rx.vstack(
                            rx.input(
                                id="nombre",
                                type_="text",  
                                width="100%",
                                height="auto",
                                padding="10px",
                                border="1px solid #ccc",
                                border_radius="5px",
                                margin_bottom="20px",
                                style={
                                "text-align": "left"
                                }
                            ),
                            rx.heading(
                                "Write the matrix by commas",size="5"
                            ),
                            rx.text(
                                "Example: "    
                            ),
                            rx.box(
                                rx.image(
                                    src="/example.png",
                                    width="500px",
                                    height="auto",
                                    margin_left="100px",
                                    ),
                            ),
                            rx.input(placeholder="Matrix", id="last_name"),
                            rx.radio(
                                ["Alphabet (27 char. A=0) ABCDEFGHIJKLMNOPQRSTUVWXYZ_", "Alphabet (28 char. A=0) ABCDEFGHIJKLMN1OPQRSTUVWXYZ_"],
                                name="radio",
                                required=True,
                            ),
                            
                            rx.button(
                                "Submit",
                                type_="submit",
                                bg="#ecfdf5",
                                color="#047857",
                                border_radius="lg",
                            ),
                        ),
                        on_submit=FormState.handle_submit,
                    ),
                    rx.divider(),
                    rx.heading("Results"),
                    rx.text(FormState.form_data.to_string()),
                    width="100%",
                ),
                value="tab1",
            ),
            rx.tabs.content(
                rx.text("item on tab 2"),
                value="tab2",
            ),
            default_value="tab1",
            orientation="horizontal",
        ),
    )


app = rx.App()
app.add_page(index)
app.add_page(machine, route="/machine")
