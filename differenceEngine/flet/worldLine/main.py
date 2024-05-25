import requests
import flet as ft
import socket
import json
import shutil


def get_ipv6_addresses(host):
    try:
        # 获取主机的名称
        hostname = socket.getfqdn(host)
        # 获取主机的IPv6地址列表
        addrs = socket.getaddrinfo(hostname, None, socket.AF_INET6)
        # 提取并返回IPv6地址
        ipv6_addrs = [addr[4][0] for addr in addrs if addr[0] == socket.AF_INET6]
        return ipv6_addrs
    except socket.error:
        return []


def get_public_ipv6():
    try:
        response = requests.get("https://ipv6.icanhazip.com/")
        return response.text.strip()
    except requests.RequestException:
        return None


class IPV6:
    ipv6_addresses = [1, 2, 3]
    email_tex = ""


class APP_data_structure:
    def __init__(self, name) -> None:
        self.name = name
        self.data = {}
        try:
            print(name)
            with open(name, "r") as file:
                self.data = json.load(file)
            print("dddddddddd")
        except:
            print("load emty data")

    def save(self):
        with open(self.name, "w") as file:
            json.dump(self.data, file)


def main(page: ft.Page):
    ipv6_list = IPV6
    data_struct = APP_data_structure("logs.iii")
    print(data_struct.data.keys())
    if "IPv6" in data_struct.data.keys():
        print("lskdjfksldjf")
        ipv6_list.ipv6_addresses = data_struct.data["IPv6"]
    if "PubEmail" in data_struct.data.keys():
        print("pubemaillskdjfksldjf")
        ipv6_list.email_tex = data_struct.data["PubEmail"]

    # def select_file():
    #     root = tk.Tk()
    #     root.withdraw()  # 隐藏主窗口
    #     file_path = filedialog.askopenfilename()
    #     print(f"选择的文件路径是: {file_path}")

    # select_file()
    # select_file()

    def change_email(e: ft.ControlEvent):
        print(type(e))
        print(e.control.value)
        data_struct.data["PubEmail"] = e.control.value
        data_struct.save()

    def on_dialog_result(e: ft.FilePickerResultEvent):
        print("Selected files:", e.files)
        print("Selected file or directory:", e.path)

    def get_directory_result(e: ft.FilePickerResultEvent):
        if e.path:
            with open(e.path + "/loggg.iii", "w") as file:
                file.write(f"{1}sldkfjlsdkfjhellollllleeeeeeeeeee\n")
            shutil.copy("logs.iii",e.path+"/logs.iii")
        # print(e.path + "\\loggg.iii")

        directory_path.value = e.path if e.path else "Cancelled!"
        directory_path.update()

    get_directory_dialog = ft.FilePicker(on_result=get_directory_result)
    page.overlay.append(get_directory_dialog)
    directory_path = ft.Text()

    file_picker = ft.FilePicker(on_result=on_dialog_result)
    # file_picker = ft.FilePicker()
    page.overlay.append(file_picker)
    page.update()

    def open_file(e: ft.Control):
        print("sldkfjskldf")
        # select_file()
        # root = tk.Tk()
        # root.withdraw()

        # file_path = filedialog.askopenfilenames()
        # print(file_path)

    email_text = ft.TextField(
        label="your public email", value=ipv6_list.email_tex, on_change=change_email
    )
    but = ft.ElevatedButton(
        "Choose files...",
        on_click=lambda _: file_picker.pick_files(allow_multiple=True),
    )
    # try:
    #     with open("logs.in", "r") as file:
    #         file.read()
    # except:
    #     pass

    def update_ipv6(e):
        ipv6_list.ipv6_addresses = [get_public_ipv6()]
        print(ipv6_list.ipv6_addresses)
        print(ip_column.controls)
        ip_column.controls = [ft.Text(f"{it}") for it in ipv6_list.ipv6_addresses]
        page.update()
        data_struct.data["IPv6"] = ipv6_list.ipv6_addresses
        data_struct.save()

    # ipv6_addresses = get_ipv6_addresses("localhost")
    # print(ipv6_addresses)
    ip_column = ft.Column(
        controls=[ft.Text(f"{it}") for it in ipv6_list.ipv6_addresses]
    )
    page.add(
        ft.SafeArea(
            ft.Column(
                controls=[
                    email_text,
                    ft.Text("press refresh to get ipv6/按fresh按钮获取ipv6"),
                    ip_column,
                    ft.ElevatedButton(text="refresh", on_click=update_ipv6),
                    ft.ElevatedButton(text="export", on_click=open_file),
                    but,
                    ft.ElevatedButton(
                        text="dir",
                        on_click=lambda _: get_directory_dialog.get_directory_path(),
                    ),
                    directory_path,
                ]
            )
        )
    )
    page.update()


ft.app(main)
