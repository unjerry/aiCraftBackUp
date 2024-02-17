import pygame
import pygame_gui

pygame.init()

pygame.display.set_caption("Quick Start")
window_surface = pygame.display.set_mode((800, 600))

background = pygame.Surface((600, 450))
background.fill(pygame.Color("#010770"))

manager = pygame_gui.UIManager((800, 600), 'theme.json')
hello_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((300, 250), (100, 100)), text="hello say", manager=manager
)

hello_window=pygame_gui.elements.UIWindow(rect=pygame.Rect((250, 100), (100, 100)),resizable=True)
clock = pygame.time.Clock()
is_running = True
hello_drop = pygame_gui.elements.UIDropDownMenu(["dd","dfd"],starting_option="dd",relative_rect=pygame.Rect((400, 250), (100, 100)),container=hello_window)
# button_layout_rect = pygame.Rect(30, 20, 100, 20)
hello_horiz = pygame_gui.elements.UIHorizontalSlider(start_value=0,value_range=[0,3],relative_rect=pygame.Rect((200, 250), (100, 100)))
hello_tex=pygame_gui.elements.UITextBox("<a href='id'>ddd</a>",relative_rect=pygame.Rect((200, 150), (100, 100)),manager=manager)
hello_texin=pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((200, 50), (100, 100)),manager=manager)
hello_label=pygame_gui.elements.UILabel(text="sdfsdf",relative_rect=pygame.Rect((200, 350), (100, 100)),manager=manager)

hello_pb=pygame_gui.elements.UIProgressBar(relative_rect=pygame.Rect((100, 50), (100, 100)),manager=manager)
hello_pb.set_current_progress(120)
print(hello_pb.status_text())
hello_sb=pygame_gui.elements.UIScreenSpaceHealthBar(relative_rect=pygame.Rect((0, 50), (100, 100)),manager=manager)
hello_slelis=pygame_gui.elements.UISelectionList(item_list=["sdf","sdsdgg"],relative_rect=pygame.Rect((0, 150), (100, 100)),manager=manager)
hello_slebar=pygame_gui.elements.UIStatusBar(relative_rect=pygame.Rect((0, 250), (100, 100)),manager=manager)
hello_ttp=pygame_gui.elements.UITooltip("<p>sss<\p>",manager=manager,hover_distance=[200,100])
hello_vsb=pygame_gui.elements.UIVerticalScrollBar(relative_rect=pygame.Rect((0, 250), (100, 100)),manager=manager,visible_percentage=0.1)

while is_running:
    time_delta = clock.tick(60) / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == hello_button:
                print("sldkfjsdlkfjsdlkf")
                # hello_window=pygame_gui.elements.UIWindow(rect=pygame.Rect((250, 100), (100, 100)),resizable=True)
                # hello_window.set_display_title("sdfsdf")
                hello_label.set_text(hello_texin.get_text())
        if event.type == pygame_gui.UI_WINDOW_CLOSE:
            if event.ui_element == hello_window:
                print(hello_window.visible)
                print("killed")
                print(hello_window.visible)
        if event.type==pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
            if event.ui_element==hello_horiz:
                print("slideee",hello_horiz.get_current_value())
        manager.process_events(event)

    manager.update(time_delta)

    window_surface.blit(background, (10, 50))
    manager.draw_ui(window_surface)

    pygame.display.update()
