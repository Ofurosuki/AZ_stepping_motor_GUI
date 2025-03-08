import flet as ft
import comm
import time
import threading

def main(page: ft.Page):
    Comm = comm.Communication(address="192.168.1.20")
    target_pos=""
    dlg = ft.AlertDialog(
        title=ft.Text("Value out of range!")
        #on_dismiss=lambda e: page.add(ft.Text("Invalid value", color="red"))
    )
    dlg2 = ft.AlertDialog(
        title=ft.Text("Invalid value!")
        #on_dismiss=lambda e: page.add(ft.Text("Invalid value", color="red"))
    )
    def update_():
        while True:
            time.sleep(0.2)  
            current_pos.value = str(Comm.get_current_position())
            page.update()  # UIを更新
    def on_click(e):
        try :
            target_pos.value = int(target_pos.value)
        except:
            #page.add(ft.Text(value="invalid value", color="red"))
            page.open(dlg2)
            return
        if not Comm.set_target_position(int(target_pos.value)):
            #page.add(ft.Text(value="Value out of range", color="red"))
            page.open(dlg)
            return
        page.add(ft.Text(value=f">>Sent position command:{target_pos.value}", color="red"))
        Comm.send_target_position()
    def on_click_up(e):
        Comm.set_target_position(Comm.get_current_position()+int(step.value))
        page.add(ft.Text(value=f">>Sent position command:{Comm.get_current_position()+int(step.value)}", color="red"))
        Comm.send_target_position()
    def on_click_down(e):
        Comm.set_target_position(Comm.get_current_position()-int(step.value))
        page.add(ft.Text(value=f">>Sent position command:{Comm.get_current_position()-int(step.value)}", color="red"))
        Comm.send_target_position()
    buttons=[]
    buttons.append(ft.ElevatedButton(text="Down", on_click=on_click_down))
    buttons.append(ft.TextField(label="Step size"))
    buttons.append(ft.ElevatedButton(text="Up", on_click=on_click_up))
    step=buttons[1]
    step.value="100"
    row=ft.Row(buttons)
    # Text Control 生成
    current_pos = ft.Text(value="", color="green",size=40)
    current_pos_title = ft.Text(value="Current Position", color="green",size=20)
    target_pos= ft.TextField(label=f"Target Position range ({Comm.lower_lim} to {Comm.upper_lim})")
    #clear_button = ft.ElevatedButton(text="Clear", on_click=)
    # ページのコントロールリストに Control を追加
    #page.controls.append(t)
    # ページを更新
    #page.update()
    thread = threading.Thread(target=update_)
    thread.start()
    
    page.add(ft.ElevatedButton(text="Send position", on_click=on_click),
             target_pos,current_pos_title,current_pos,row)
    


ft.app(target=main)
