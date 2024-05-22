import flet as ft


class MyButton(ft.ElevatedButton):
    def __init__(self, text, on_click):
        super().__init__()
        self.bgcolor = ft.colors.ORANGE_300
        self.color = ft.colors.GREEN_800
        self.text = text
        self.on_click = on_click


class St:
    height = 1.80
    weight = 75


def main(page: ft.Page):
    page.adaptive = True

    # page.appbar = ft.AppBar(
    #     leading=ft.TextButton("New", style=ft.ButtonStyle(padding=0)),
    #     title=ft.Text("Adaptive AppBar"),
    #     actions=[
    #         ft.IconButton(ft.cupertino_icons.ADD, style=ft.ButtonStyle(padding=0))
    #     ],
    #     bgcolor=ft.colors.with_opacity(0.04, ft.cupertino_colors.SYSTEM_BACKGROUND),
    # )
    # page.navigation_bar = ft.NavigationBar(
    #     destinations=[
    #         ft.NavigationDestination(icon=ft.icons.EXPLORE, label="Explore"),
    #         ft.NavigationDestination(icon=ft.icons.COMMUTE, label="Commute"),
    #         ft.NavigationDestination(
    #             icon=ft.icons.BOOKMARK_BORDER,
    #             selected_icon=ft.icons.BOOKMARK,
    #             label="Bookmark",
    #         ),
    #     ],
    #     border=ft.Border(
    #         top=ft.BorderSide(color=ft.cupertino_colors.SYSTEM_GREY2, width=0)
    #     ),
    # )
    st = St()

    def update_text():
        show_text.value = f"BMI value is:{st.weight/pow(st.height,2):.2f} kg/m^2"
        print("sldkjf")
        page.update()

    def change_height(e):
        st.height = float(e.control.value)
        print("sldkjf")
        print(st.height, type(st.height))
        update_text()

    def change_weight(e):
        st.weight = float(e.control.value)
        print("sldkjfdfs")
        print(st.weight, type(st.weight))
        update_text()

    height_text = ft.TextField(
        label="height/身高/m", value=st.height, on_change=change_height
    )
    weight_text = ft.TextField(
        label="weight/体重/kg", value=st.weight, on_change=change_weight
    )
    show_text = ft.Text(
        f"BMI value is:{(st.weight/pow(st.height,2)):.2f} kg/m^2", size=30
    )
    page.add(
        ft.SafeArea(
            ft.Column(
                [
                    height_text,
                    weight_text,
                    show_text,
                ]
            )
        )
    )


ft.app(target=main)
