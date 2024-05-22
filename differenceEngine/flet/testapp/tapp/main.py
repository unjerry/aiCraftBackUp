import flet as ft
import time


def main(page: ft.Page):
    def add_clicked(e):
        page.add(ft.Checkbox(label=new_task.value))
        new_task.value = ""
        new_task.focus()
        new_task.update()

    new_task = ft.TextField(hint_text="What's needs to be done?", width=300)
    page.add(ft.Row([new_task, ft.ElevatedButton("Add", on_click=add_clicked)]))
    t = ft.Text()
    page.add(t)  # it's a shortcut for page.controls.append(t) and then page.update()
    page.add(ft.Row(controls=[ft.Text("A"), ft.Text("B"), ft.Text("C")]))
    page.add(
        ft.Row(
            controls=[
                ft.TextField(label="Your name"),
                ft.ElevatedButton(text="Say my name!"),
            ]
        )
    )
    def button_clicked(e):
        page.add(ft.Text("Clicked!"))

    page.add(ft.ElevatedButton(text="Click me", on_click=button_clicked))
    for i in range(10):
        t.value = f"Step {i}"
        page.update()
        time.sleep(1)


ft.app(target=main)
