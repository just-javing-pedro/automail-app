import gi
import sys
import time
import json
import os
import re
import SendMailerSender
import SendSmtplibGmail

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILE = os.path.join(BASE_DIR, "accounts.json")

try:
    with open(FILE, "r") as file:
        accounts = json.load(file)
except Exception as e:
    print(f"Fatal error: {e}")
    Gtk.main_quit()


gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import Gtk, Gdk
from gi.repository import GLib

css = Gtk.CssProvider()
css_path = os.path.join(os.path.dirname(__file__), "style.css")
css.load_from_path(css_path)
Gtk.StyleContext.add_provider_for_screen(
    Gdk.Screen.get_default(),
    css,
    Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
)

ErrorSendingEmail = None

def email_error(erro):
    global ErrorSendingEmail
    ErrorSendingEmail = erro



builder = Gtk.Builder()
builder_path = os.path.join(os.path.dirname(__file__), "../Automail_UI/Interface.glade")
builder.add_from_file(builder_path)

# PASTAS

pics_folder = os.path.join(os.path.dirname(__file__), "../Automail_UI/pics") 

# JANELAS

signup_window = builder.get_object("SignUpWindow")
signup_window.connect("destroy", Gtk.main_quit)

login_window = builder.get_object("LoginWindow")
login_window.connect("destroy", Gtk.main_quit)

sucess_window = builder.get_object("SucessCreatingAcc")
sucess_window.connect(
    "delete-event",
    lambda widget, event: (widget.set_visible(False), True)[1]
)

main_window = builder.get_object("MainWindow")
main_window.connect("destroy", Gtk.main_quit)

recovery_window = builder.get_object("ForgotPasswordWindow")
recovery_window.connect(
    "delete-event",
    lambda widget, event: (widget.set_visible(False), True)[1]
)

recovery_window_sucess = builder.get_object("ForgotPasswordSucessWindow")
recovery_window_sucess.connect(
    "delete-event",
    lambda widget, event: (widget.set_visible(False), True)[1]
)


# LOGIN

SignUp_btn_login = builder.get_object("SignUp-button-login")
UserOrEm_entry_login = builder.get_object("Username-entry-login")
Password_entry_login = builder.get_object("Password-entry-login")
Continue_btn_login = builder.get_object("Continue-button-login")
ShowOrHide_pas_login = builder.get_object("ShowOrHide-login")
Username_label_login = builder.get_object("Username-label-login")
SwitchEmAnPas_btn_login = builder.get_object("SwitchEmailAndPas-button-login")
ForgotPas_btn_login = builder.get_object("Forgot-password-login")
Eye_image_login = builder.get_object("Eye-image-login")

using_emorpas = 1

# RECOVERY

Email_entry_recovery = builder.get_object("Email-entry-recovery")
SendVerCod_btn_recovery = builder.get_object("SendVerificationCode-btn-recovery")
Request_box_recovery = builder.get_object("Request-box-recovery")

Code_entry_recovery = builder.get_object("MainCode-entry-recovery")
VerCode_btn_recovery = builder.get_object("Verify-btn-recovery")
SendCodeAg_btn_recovery = builder.get_object("SendAgain-btn-recovery")
Verification_box_recovery = builder.get_object("Verification-box-recovery")


NewPas_entry_recovery = builder.get_object("MainNewPas-entry-recovery")
ConfirmNewPas_btn_recovery = builder.get_object("MainNewPas-button-recovery")
NewPas_box_recovery = builder.get_object("NewPas-box-recovery")

# SIGNUP

Name_entry_signup = builder.get_object("Name-entry-signup")
Username_entry_signup = builder.get_object("Username-entry-signup")
Email_entry_signup = builder.get_object("Email-entry-signup")
Password_entry_signup = builder.get_object("Password-entry-signup")
ConfirmPassword_entry_signup = builder.get_object("Conf-pas-entry-signup")
Continue_btn_signup = builder.get_object("Continue-button-signup")
Login_btn_signup = builder.get_object("Login-button-signup")
ShowOrHide_pas_signup = builder.get_object("ShowOrHide-signup")
Eye_image_signup = builder.get_object("Eye-image-signup")

# SUCESS

Login_acc_sucess = builder.get_object("LoginAcc-sucess")
Leave_sucess = builder.get_object("Leave-sucess")

# MAIN

FirstOne_entry_main = builder.get_object("Sender-name-entry-main")
SecondOne_entry_main = builder.get_object("Sender-email-entry-main")
ThirdOne_entry_main = builder.get_object("Port-entry-main")
ReceiverEmail_entry_main = builder.get_object("Receiver-entry-main")
Title_entry_main = builder.get_object("Title-entry-main")
Content_entry_main = builder.get_object("Content-entry-main")
SendMsg_btn_main = builder.get_object("SendMsg-main")
MailMode_combo_main = builder.get_object("Mail-mode-main")
Port_sep_main = builder.get_object("Port-sep-main")
FirstOne_label_main = builder.get_object("Sender-name-label-main")
SecondOne_label_main = builder.get_object("Sender-email-label-main")

Menu_box_main = builder.get_object("Menu-box-main")
MenuDad_box_main = builder.get_object("Main2-main")
Menu_image_main = builder.get_object("Menu-main")
CloseMenu_btn_main = builder.get_object("CloseMenu-main")
OpenMenu_btn_main = builder.get_object("OpenMenu-button-main")
Settings_btn_menu_main = builder.get_object("Settings-button-menu-main")
SendEmail_btn_menu_main = builder.get_object("SendEmail-button-menu-main")
Inbox_btn_menu_main = builder.get_object("Inbox-button-menu-main")
Preferences_btn_menu_main = builder.get_object("Preferences-button-menu-main")

program_theme = "dark"
whereiam_menu_main = "send email"


def interpolate_menudad(start, end, duration, show):
    if show:
        MenuDad_box_main.set_visible(True)

    start_time = time.time()

    def update():
        elapsed = time.time() - start_time
        t = max(0, min(1, elapsed / duration))

        value = start + (end - start) * t
        MenuDad_box_main.set_opacity(value)

        if elapsed >= duration:
            MenuDad_box_main.set_opacity(end)

            if not show:
                MenuDad_box_main.set_visible(False)

            return False

        return True

    GLib.timeout_add(16, update)

def ChangeMenu(order):
    global fadein_opacity
    if order:
        interpolate_menudad(0, 1, 0.1, True)
    else:
        interpolate_menudad(1, 0, 0.1, False)

MenuDad_box_main.set_opacity(0)
ChangeMenu(False)


def TurnOffButton(button, order, text):
    if order == True:
        button.set_label(text)
        button.set_sensitive(False)
    else:
        button.set_label(text)
        button.set_sensitive(True)

def ChangeMode_main(order):
    global whereiam_menu_main
    global program_theme

    things = [Inbox_btn_menu_main, SendEmail_btn_menu_main, Preferences_btn_menu_main, Settings_btn_menu_main]

    def put_border(button):
        for bt in things:
                style = bt.get_style_context()

                style.remove_class("menu-active-bt-dark")
                style.remove_class("menu-active-bt-white")

                if bt == button:
                    style.add_class(f"menu-active-bt-{program_theme}")

    match order:
        case 1:
            ChangeMenu(False)
            whereiam_menu_main = "send email"

            put_border(SendEmail_btn_menu_main)
        case 2:
            ChangeMenu(False)
            whereiam_menu_main = "inbox"

            put_border(Inbox_btn_menu_main)
        case 3:
            ChangeMenu(False)
            whereiam_menu_main = "preferences"

            put_border(Preferences_btn_menu_main)
        case 4:
            ChangeMenu(False)
            whereiam_menu_main = "settings"

            put_border(Settings_btn_menu_main)
        

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

# STYLING

def ChangeTheme(widget, order):
    global program_theme
    if order == "dark":
        program_theme = order

        SendEmail_btn_menu_main.get_style_context().add_class(f"menu-active-bt-{program_theme}")

        Eye_image_login.set_from_file(f"{pics_folder}/Eye-{order}.png")
        Eye_image_signup.set_from_file(f"{pics_folder}/Eye-{order}.png")
        Menu_image_main.set_from_file(f"{pics_folder}/Menu-{order}.png")

        Menu_box_main.get_style_context().add_class("dark-menu-box-main")


        if isinstance(widget, Gtk.Window):
            widget.get_style_context().add_class("dark-background")

        elif isinstance(widget, Gtk.Button):
            if widget != CloseMenu_btn_main:
                widget.get_style_context().add_class("dark-background-button")
            else:
                widget.get_style_context().add_class("close-menu")
        
        elif isinstance(widget, Gtk.Entry):
            widget.get_style_context().add_class("dark-background")
        
        elif isinstance(widget, Gtk.Label):
            widget.get_style_context().add_class("dark-background")
        
        elif isinstance(widget, Gtk.ComboBoxText):
            widget.get_style_context().add_class("dark-background")
        
        elif isinstance(widget, Gtk.TextView):
            widget.get_style_context().add_class("dark-background")

        elif isinstance(widget, Gtk.MenuItem):
            widget.get_style_context().add_class("dark-background")
        
        elif isinstance(widget, Gtk.ScrolledWindow):
            widget.get_style_context().add_class("dark-background")
                
        try:
            for child in widget.get_children():
                ChangeTheme(child, "dark")
        except:
            pass
    elif order == "white":
        program_theme = order

        SendEmail_btn_menu_main.get_style_context().add_class(f"menu-active-bt-{program_theme}")

        Eye_image_login.set_from_file(f"{pics_folder}/Eye-{order}.png")
        Eye_image_signup.set_from_file(f"{pics_folder}/Eye-{order}.png")
        Menu_image_main.set_from_file(f"{pics_folder}/Menu-{order}.png")

        Menu_box_main.get_style_context().add_class("white-menu-box-main")

        if isinstance(widget, Gtk.Window):
            widget.get_style_context().add_class("white-background")

        elif isinstance(widget, Gtk.Button):
            if widget != CloseMenu_btn_main:
                widget.get_style_context().add_class("white-background-button")
            else:
                widget.get_style_context().add_class("close-menu")
        
        elif isinstance(widget, Gtk.Entry):
            widget.get_style_context().add_class("white-background")
        
        elif isinstance(widget, Gtk.Label):
            widget.get_style_context().add_class("white-background")
        
        elif isinstance(widget, Gtk.ComboBoxText):
            widget.get_style_context().add_class("white-background")
        
        elif isinstance(widget, Gtk.TextView):
            widget.get_style_context().add_class("white-background")

        elif isinstance(widget, Gtk.MenuItem):
            widget.get_style_context().add_class("white-background")

        elif isinstance(widget, Gtk.ScrolledWindow):
            widget.get_style_context().add_class("white-background")

        try:
            for child in widget.get_children():
                ChangeTheme(child, "white")
        except:
            pass


#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

class Funcoes:

    # LOGIN

    def ForgotPasClicked(self):
        recovery_window.set_visible(True)

        NewPas_box_recovery.set_visible(False)
        Verification_box_recovery.set_visible(False)
        Request_box_recovery.set_visible(True)

        Code_entry_recovery.set_text("")
        Email_entry_recovery.set_text("")
        NewPas_entry_recovery.set_text("")
        

    def EmailOrUsername(self):
        global using_emorpas
        if using_emorpas == 1:
            using_emorpas = 2
            Username_label_login.set_text("E-mail:")
            UserOrEm_entry_login.set_placeholder_text("Your e-mail here...")
            UserOrEm_entry_login.set_text("")
            SwitchEmAnPas_btn_login.set_label("Use username")
        else:
            using_emorpas = 1
            Username_label_login.set_text("Username:")
            UserOrEm_entry_login.set_placeholder_text("Your username here...")
            UserOrEm_entry_login.set_text("")
            SwitchEmAnPas_btn_login.set_label("Use e-mail")



    def ContinueClicked_login(self):

        Username_text = (" ".join((UserOrEm_entry_login.get_text()).split())).lower()
        Password_text = Password_entry_login.get_text()

        if all([Username_text, Password_text]):
            for a in accounts:
                if using_emorpas == 1:
                    if Username_text == a["username"] and Password_text == a["password"]:
                        login_window.set_visible(False)
                        main_window.set_visible(True)
                    else:
                        TurnOffButton(Continue_btn_login, True, "Something is wrong.")
                        GLib.timeout_add(1000, lambda: TurnOffButton(Continue_btn_login, False, "Continue"))
                else:
                    if Username_text == a["email"] and Password_text == a["password"]:
                        login_window.set_visible(False)
                        main_window.set_visible(True)
                    else:
                        TurnOffButton(Continue_btn_login, True, "Something is wrong.")
                        GLib.timeout_add(1000, lambda: TurnOffButton(Continue_btn_login, False, "Continue"))
        else:
            TurnOffButton(Continue_btn_login, True, "All fields are required.")
            GLib.timeout_add(1000, lambda: TurnOffButton(Continue_btn_login, False, "Continue"))

    def EyeClicked_login(self, state):
        if state == 1:
            Password_entry_login.set_visibility(True)
        else:
            Password_entry_login.set_visibility(False)

    def SignUpClicked(self):
        login_window.set_visible(False)
        recovery_window_sucess.set_visible(False)
        recovery_window.set_visible(False)
        signup_window.set_visible(True)

    # RECOVERY

    def Recovery_step1(self):
        global Email_recovery_text
        Email_recovery_text = " ".join((Email_entry_recovery.get_text()).split())

        if Email_recovery_text:
            if any(Email_recovery_text == a["email"] for a in accounts):
                Request_box_recovery.set_visible(False)
                Verification_box_recovery.set_visible(True)
                SendSmtplibGmail.receive_values(
                    "",
                    "",
                    Email_recovery_text,
                    "",
                    "",
                    True
                )
            else:
                TurnOffButton(SendVerCod_btn_recovery, True, "This account does not exist.")
                GLib.timeout_add(1000, lambda: TurnOffButton(SendVerCod_btn_recovery, False, "Send verification code"))
        else:
            TurnOffButton(SendVerCod_btn_recovery, True, "The field are required.")
            GLib.timeout_add(1000, lambda: TurnOffButton(SendVerCod_btn_recovery, False, "Send verification code"))

    def Recovery_step2(self):
        Code_recovery_text = " ".join((Code_entry_recovery.get_text()).split())
        
        if Code_recovery_text:
            if SendSmtplibGmail.VerifyCode(Code_recovery_text):
                Verification_box_recovery.set_visible(False)
                NewPas_box_recovery.set_visible(True)
            else:
                TurnOffButton(VerCode_btn_recovery, True, "Incorrect code!")
                GLib.timeout_add(1000, lambda: TurnOffButton(VerCode_btn_recovery, False, "Verify"))
        else:
            TurnOffButton(VerCode_btn_recovery, True, "The field are required.")
            GLib.timeout_add(1000, lambda: TurnOffButton(VerCode_btn_recovery, True, "Verify"))

    def Recovery_step2_sendagain(self):
        SendSmtplibGmail.receive_values(
                    "",
                    "",
                    Email_recovery_text,
                    "",
                    "",
                    True
        )
        TurnOffButton(SendCodeAg_btn_recovery, True, "Sucess!")
        GLib.timeout_add(10000, lambda: TurnOffButton(SendCodeAg_btn_recovery, False, "Send again"))
    
    def Recovery_step3(self):
        NewPas_recovery_text = NewPas_entry_recovery.get_text()

        if NewPas_recovery_text:
            if any(NewPas_recovery_text == a["password"] for a in accounts):
                TurnOffButton(ConfirmNewPas_btn_recovery, True, "This is your current password!")
                GLib.timeout_add(1000, lambda: TurnOffButton(ConfirmNewPas_btn_recovery, False, "Set as new password"))
            else:
                for a in accounts:
                    if a["email"] == Email_recovery_text:
                        a["password"] = NewPas_recovery_text

                recovery_window.set_visible(False)
                recovery_window_sucess.set_visible(True)
        else:
            TurnOffButton(ConfirmNewPas_btn_recovery, True, "The field are required.")
            GLib.timeout_add(1000, lambda: TurnOffButton(ConfirmNewPas_btn_recovery, False, "Send recovery code"))



    # SIGNUP
    
    def LoginClicked(self):
        signup_window.set_visible(False)
        login_window.set_visible(True)

    def ContinueClicked_signup(self):

        Name_text = " ".join((Name_entry_signup.get_text()).split())
        Username_text = " ".join((Username_entry_signup.get_text()).split())
        Email_text = " ".join((Email_entry_signup.get_text()).split())
        Password_text = Password_entry_signup.get_text()
        ConfirmPassword_text = " ".join((ConfirmPassword_entry_signup.get_text()).split())

        things = [Name_text, Username_text, Email_text, Password_text, ConfirmPassword_text]
        

        if all(things):
            if not re.fullmatch(r'[a-zA-Z0-9._+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', Email_text) or re.search(r'[^a-zA-Z0-9_.-]', Username_text) or re.search(r'[^a-zA-Z0-9_.\- ]', Name_text):
                TurnOffButton(Continue_btn_signup, True, "Special characters are not allowed.")
                GLib.timeout_add(1000, lambda: TurnOffButton(Continue_btn_signup, False, "Continue"))
            else:
                if not any((a["username"] == Username_text or a["email"] == Email_text) for a in accounts):
                    if ConfirmPassword_text != Password_text:
                        TurnOffButton(Continue_btn_signup, True, "The passwords don't match.")
                        GLib.timeout_add(1000, lambda: TurnOffButton(Continue_btn_signup, False, "Continue"))
                    else:
                        accounts.append({
                            "name": Name_text,
                            "username": Username_text.lower(),
                            "email": Email_text.lower(),
                            "password": Password_text
                        })

                        try:
                            with open(FILE, "w") as file:
                                json.dump(accounts, file, indent=4)
                        except Exception as e:
                            print(f"Fatal error: {e}")
                            Gtk.main_quit()

                        signup_window.set_visible(False)
                        sucess_window.set_visible(True)
                else:
                    TurnOffButton(Continue_btn_signup, True, "This account already exists.")
                    GLib.timeout_add(1000, lambda: TurnOffButton(Continue_btn_signup, False, "Continue"))
        else:
            TurnOffButton(Continue_btn_signup, True, "All fields are required.")
            GLib.timeout_add(1000, lambda: TurnOffButton(Continue_btn_signup, False, "Continue"))
    
    def EyeClicked_signup(self, state):
        if state == 1:
            Password_entry_signup.set_visibility(True)
            ConfirmPassword_entry_signup.set_visibility(True)
        else:
            Password_entry_signup.set_visibility(False)
            ConfirmPassword_entry_signup.set_visibility(False)

    # SUCESS

    def LoginClicked_sucess(self):
        sucess_window.set_visible(False)
        main_window.set_visible(True)
    
    def LeaveClicked_sucess(self):
        Gtk.main_quit()

    # MAIN


    def MailType_main(self):
        Mail_mode = MailMode_combo_main.get_active_id()
        if Mail_mode == "m":
            Port_sep_main.set_visible(True)
            FirstOne_label_main.set_text("Sender name:")
            SecondOne_label_main.set_text("Sender e-mail:")
            
        elif Mail_mode == "g":
            Port_sep_main.set_visible(False)
            FirstOne_label_main.set_text("Sender e-mail:")
            SecondOne_label_main.set_text("Sender password:")

    def SendMsgClicked_main(self):

        FirstEntry_text_main = " ".join((FirstOne_entry_main.get_text()).split())
        SecondEntry_text_main = " ".join((SecondOne_entry_main.get_text()).split())
        ThirdEntry_text_main = " ".join((ThirdOne_entry_main.get_text()).split())
        ReceiverEmail_text_main = (" ".join((ReceiverEmail_entry_main.get_text()).split())).lower()
        Title_text_main = " ".join((Title_entry_main.get_text()).split())

        Content_buffer_main = Content_entry_main.get_buffer()
        start_iter = Content_buffer_main.get_start_iter()
        end_iter = Content_buffer_main.get_end_iter()

        Content_text_main = Content_buffer_main.get_text(start_iter, end_iter, False)

        things = [FirstEntry_text_main, ThirdEntry_text_main, SecondEntry_text_main, ReceiverEmail_text_main, Title_text_main, Content_text_main]

        Mail_mode = MailMode_combo_main.get_active_id()

        if Mail_mode == "m":
            things.append(ThirdEntry_text_main)
            things[2] = things[2].lower()
        elif Mail_mode == "g":
            things.remove(ThirdEntry_text_main)
            things[0] = things[0].lower()


        if all(things):

            if Mail_mode == "m":
                SendMailerSender.receive_values(
                    SecondEntry_text_main,
                    FirstEntry_text_main,
                    ReceiverEmail_text_main,
                    Title_text_main,
                    Content_text_main,
                    ThirdEntry_text_main
                )
            elif Mail_mode == "g":
                SendSmtplibGmail.receive_values(
                    FirstEntry_text_main,
                    SecondEntry_text_main,
                    ReceiverEmail_text_main,
                    Title_text_main,
                    Content_text_main,
                    False
                )

            if ErrorSendingEmail:
                print(ErrorSendingEmail)
                TurnOffButton(SendMsg_btn_main, True, "Something unexpected happened.")
                GLib.timeout_add(1000, lambda: TurnOffButton(SendMsg_btn_main, False, "Send message"))
            else:
                TurnOffButton(SendMsg_btn_main, True, "Sucess! (10s)")
                
                def StartCooldown():
                    cooldown = 10

                    def update():
                        nonlocal cooldown
                        cooldown -= 1
                        SendMsg_btn_main.set_label(f"Success! ({cooldown}s)")

                        if cooldown <= 0:
                            TurnOffButton(SendMsg_btn_main, False, "Send Message")
                            return False

                        return True
                    
                    GLib.timeout_add(1000, update)
                
                StartCooldown()

        else:
            TurnOffButton(SendMsg_btn_main, True, "All the fields are required.")
            GLib.timeout_add(1000, lambda: TurnOffButton(SendMsg_btn_main, False, "Send message"))





def main():

    
    # LOGIN

    Continue_btn_login.connect("clicked", Funcoes.ContinueClicked_login)
    SignUp_btn_login.connect("clicked", Funcoes.SignUpClicked)

    SwitchEmAnPas_btn_login.connect("clicked", Funcoes.EmailOrUsername)

    ShowOrHide_pas_login.connect("pressed", Funcoes.EyeClicked_login, 1)
    ShowOrHide_pas_login.connect("released", Funcoes.EyeClicked_login, 2)
    Password_entry_login.set_visibility(False)

    ForgotPas_btn_login.connect("clicked", Funcoes.ForgotPasClicked)


    # RECOVERY

    SendVerCod_btn_recovery.connect("clicked", Funcoes.Recovery_step1)
    VerCode_btn_recovery.connect("clicked", Funcoes.Recovery_step2)
    SendCodeAg_btn_recovery.connect("clicked", Funcoes.Recovery_step2_sendagain)
    ConfirmNewPas_btn_recovery.connect("clicked", Funcoes.Recovery_step3)


    # SIGNUP

    Continue_btn_signup.connect("clicked", Funcoes.ContinueClicked_signup)
    Login_btn_signup.connect("clicked", Funcoes.LoginClicked)


    ShowOrHide_pas_signup.connect("pressed", Funcoes.EyeClicked_signup, 1)
    ShowOrHide_pas_signup.connect("released", Funcoes.EyeClicked_signup, 2)

    ConfirmPassword_entry_signup.set_visibility(False)
    Password_entry_signup.set_visibility(False)

    # SUCESS

    Login_acc_sucess.connect("clicked", Funcoes.LoginClicked_sucess)
    Leave_sucess.connect("clicked", Funcoes.LeaveClicked_sucess)

    # MAIN

    SendMsg_btn_main.connect("clicked", Funcoes.SendMsgClicked_main)
    MailMode_combo_main.connect("changed", Funcoes.MailType_main)
    OpenMenu_btn_main.connect("clicked", lambda btn: ChangeMenu(True))
    CloseMenu_btn_main.connect("clicked", lambda btn: ChangeMenu(False))
    SendEmail_btn_menu_main.connect("clicked", lambda btn: ChangeMode_main(1))
    Inbox_btn_menu_main.connect("clicked", lambda btn: ChangeMode_main(2))
    Preferences_btn_menu_main.connect("clicked", lambda btn: ChangeMode_main(3))
    Settings_btn_menu_main.connect("clicked", lambda btn: ChangeMode_main(4))


    #-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

    # STYLING

    ChangeTheme(login_window, "dark")
    ChangeTheme(signup_window, "dark")
    ChangeTheme(main_window, "dark")
    ChangeTheme(recovery_window, "dark")
    ChangeTheme(recovery_window_sucess, "dark")
    ChangeTheme(sucess_window, "dark")
    ChangeTheme(Menu_box_main, "dark")

    #-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

    login_window.set_visible(True)
    Gtk.main()

if __name__ == "__main__":
    main()
