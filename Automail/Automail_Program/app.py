import gi
import sys
import time as t
import json
import os
import re
import SendMailerSender
import SendSmtplibGmail

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILE = os.path.join(BASE_DIR, "accounts.json")

try:
    with open(FILE, "r") as arquivo:
        contas = json.load(arquivo)
except Exception as e:
    print(f"Erro fatal: {e}")
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

ErroAoEnviarEmail = None

def erro_email(erro):
    global ErroAoEnviarEmail
    ErroAoEnviarEmail = erro



builder = Gtk.Builder()
builder_path = os.path.join(os.path.dirname(__file__), "../Automail_UI/Interface.glade")
builder.add_from_file(builder_path)

# PASTAS

pics_folder = os.path.join(os.path.dirname(__file__), "../Automail_UI/pics") 

# JANELAS

janela_signup = builder.get_object("SignUpWindow")
janela_signup.connect("destroy", Gtk.main_quit)

janela_login = builder.get_object("LoginWindow")
janela_login.connect("destroy", Gtk.main_quit)

janela_sucess = builder.get_object("SucessCreatingAcc")
janela_sucess.connect(
    "delete-event",
    lambda widget, event: (widget.set_visible(False), True)[1]
)

janela_main = builder.get_object("MainWindow")
janela_main.connect("destroy", Gtk.main_quit)

janela_recovery = builder.get_object("ForgotPasswordWindow")
janela_recovery.connect(
    "delete-event",
    lambda widget, event: (widget.set_visible(False), True)[1]
)

janela_recovery_sucess = builder.get_object("ForgotPasswordSucessWindow")
janela_recovery_sucess.connect(
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

usando_emoupas = 1

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

tema_programa = "dark"
onde_estou_menu_main = "send email"


def interpolar_menudad(comeco, fim, duracao, pedido):
    if pedido:
        MenuDad_box_main.set_visible(True)

        def sub_interpolar(tempo_decorrido):
            t = tempo_decorrido / duracao
            t = max(0, min(1, t))

            return comeco + (fim - comeco) * t
        
        inicio = t.time()

        def atualizar():
            tempo  = t.time() - inicio

            valor = sub_interpolar(tempo)
            MenuDad_box_main.set_opacity(valor)

            return tempo < duracao

        GLib.timeout_add(16, atualizar)
    else:
        def sub_interpolar(tempo_decorrido):
            t = tempo_decorrido / duracao
            t = max(0, min(1, t))

            return comeco + (fim - comeco) * t
        
        inicio = t.time()

        def atualizar():
            tempo  = t.time() - inicio

            valor = sub_interpolar(tempo)
            MenuDad_box_main.set_opacity(valor)

            if tempo >= duracao:
                if fim == 0:
                    MenuDad_box_main.set_visible(False)
                return False

            return True

        GLib.timeout_add(16, atualizar)

def AlterarMenu(pedido):
    global fadein_opacity
    if pedido:
        interpolar_menudad(0, 1, 0.1, True)
    else:
        interpolar_menudad(1, 0, 0.1, False)

MenuDad_box_main.set_opacity(0)
AlterarMenu(False)


def DesligarBotao(botao, pedido, texto):
    if pedido == True:
        botao.set_label(texto)
        botao.set_sensitive(False)
    else:
        botao.set_label(texto)
        botao.set_sensitive(True)

def MudarModo_main(pedido):
    global onde_estou_menu_main
    global tema_programa

    things = [Inbox_btn_menu_main, SendEmail_btn_menu_main, Preferences_btn_menu_main, Settings_btn_menu_main]

    def botar_border(botao):
        for bt in things:
                style = bt.get_style_context()

                style.remove_class("menu-active-bt-dark")
                style.remove_class("menu-active-bt-white")

                if bt == botao:
                    style.add_class(f"menu-active-bt-{tema_programa}")

    match pedido:
        case 1:
            AlterarMenu(False)
            onde_estou_menu_main = "send email"

            botar_border(SendEmail_btn_menu_main)
        case 2:
            AlterarMenu(False)
            onde_estou_menu_main = "inbox"

            botar_border(Inbox_btn_menu_main)
        case 3:
            AlterarMenu(False)
            onde_estou_menu_main = "preferences"

            botar_border(Preferences_btn_menu_main)
        case 4:
            AlterarMenu(False)
            onde_estou_menu_main = "settings"

            botar_border(Settings_btn_menu_main)
        

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

# STYLING

def MudarTema(widget, pedido):
    global tema_programa
    if pedido == "dark":
        tema_programa = pedido

        SendEmail_btn_menu_main.get_style_context().add_class(f"menu-active-bt-{tema_programa}")

        Eye_image_login.set_from_file(f"{pics_folder}/Eye-{pedido}.png")
        Eye_image_signup.set_from_file(f"{pics_folder}/Eye-{pedido}.png")
        Menu_image_main.set_from_file(f"{pics_folder}/Menu-{pedido}.png")

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
                MudarTema(child, "dark")
        except:
            pass
    elif pedido == "white":
        tema_programa = pedido

        SendEmail_btn_menu_main.get_style_context().add_class(f"menu-active-bt-{tema_programa}")

        Eye_image_login.set_from_file(f"{pics_folder}/Eye-{pedido}.png")
        Eye_image_signup.set_from_file(f"{pics_folder}/Eye-{pedido}.png")
        Menu_image_main.set_from_file(f"{pics_folder}/Menu-{pedido}.png")

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
                MudarTema(child, "white")
        except:
            pass


#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

class Funcoes:

    # LOGIN

    def ForgotPasClicado(self):
        janela_recovery.set_visible(True)

        NewPas_box_recovery.set_visible(False)
        Verification_box_recovery.set_visible(False)
        Request_box_recovery.set_visible(True)

        Code_entry_recovery.set_text("")
        Email_entry_recovery.set_text("")
        NewPas_entry_recovery.set_text("")
        

    def EmailOuUsername(self):
        global usando_emoupas
        if usando_emoupas == 1:
            usando_emoupas = 2
            Username_label_login.set_text("E-mail:")
            UserOrEm_entry_login.set_placeholder_text("Your e-mail here...")
            UserOrEm_entry_login.set_text("")
            SwitchEmAnPas_btn_login.set_label("Use username")
        else:
            usando_emoupas = 1
            Username_label_login.set_text("Username:")
            UserOrEm_entry_login.set_placeholder_text("Your username here...")
            UserOrEm_entry_login.set_text("")
            SwitchEmAnPas_btn_login.set_label("Use e-mail")



    def ContinueClicado_login(self):

        Username_texto = (" ".join((UserOrEm_entry_login.get_text()).split())).lower()
        Password_texto = Password_entry_login.get_text()

        if all([Username_texto, Password_texto]):
            for a in contas:
                if usando_emoupas == 1:
                    if Username_texto == a["username"] and Password_texto == a["password"]:
                        janela_login.set_visible(False)
                        janela_main.set_visible(True)
                    else:
                        DesligarBotao(Continue_btn_login, True, "Something is wrong.")
                        GLib.timeout_add(1000, lambda: DesligarBotao(Continue_btn_login, False, "Continue"))
                else:
                    if Username_texto == a["email"] and Password_texto == a["password"]:
                        janela_login.set_visible(False)
                        janela_main.set_visible(True)
                    else:
                        DesligarBotao(Continue_btn_login, True, "Something is wrong.")
                        GLib.timeout_add(1000, lambda: DesligarBotao(Continue_btn_login, False, "Continue"))
        else:
            DesligarBotao(Continue_btn_login, True, "All fields are required.")
            GLib.timeout_add(1000, lambda: DesligarBotao(Continue_btn_login, False, "Continue"))

    def EyeClicado_login(self, state):
        if state == 1:
            Password_entry_login.set_visibility(True)
        else:
            Password_entry_login.set_visibility(False)

    def SignUpClicado(self):
        janela_login.set_visible(False)
        janela_recovery_sucess.set_visible(False)
        janela_recovery.set_visible(False)
        janela_signup.set_visible(True)

    # RECOVERY

    def Recovery_etapa1(self):
        global Email_recovery_text
        Email_recovery_text = " ".join((Email_entry_recovery.get_text()).split())

        if Email_recovery_text:
            if any(Email_recovery_text == a["email"] for a in contas):
                Request_box_recovery.set_visible(False)
                Verification_box_recovery.set_visible(True)
                SendSmtplibGmail.receber_valores(
                    "",
                    "",
                    Email_recovery_text,
                    "",
                    "",
                    True
                )
            else:
                DesligarBotao(SendVerCod_btn_recovery, True, "This account does not exist.")
                GLib.timeout_add(1000, lambda: DesligarBotao(SendVerCod_btn_recovery, False, "Send verification code"))
        else:
            DesligarBotao(SendVerCod_btn_recovery, True, "The field are required.")
            GLib.timeout_add(1000, lambda: DesligarBotao(SendVerCod_btn_recovery, False, "Send verification code"))

    def Recovery_etapa2(self):
        Code_recovery_text = " ".join((Code_entry_recovery.get_text()).split())
        
        if Code_recovery_text:
            if SendSmtplibGmail.VerificarCodigo(Code_recovery_text):
                Verification_box_recovery.set_visible(False)
                NewPas_box_recovery.set_visible(True)
            else:
                DesligarBotao(VerCode_btn_recovery, True, "Incorrect code!")
                GLib.timeout_add(1000, lambda: DesligarBotao(VerCode_btn_recovery, False, "Verify"))
        else:
            DesligarBotao(VerCode_btn_recovery, True, "The field are required.")
            GLib.timeout_add(1000, lambda: DesligarBotao(VerCode_btn_recovery, True, "Verify"))

    def Recovery_etapa2_mandardnv(self):
        SendSmtplibGmail.receber_valores(
                    "",
                    "",
                    Email_recovery_text,
                    "",
                    "",
                    True
        )
        DesligarBotao(SendCodeAg_btn_recovery, True, "Sucess!")
        GLib.timeout_add(10000, lambda: DesligarBotao(SendCodeAg_btn_recovery, False, "Send again"))
    
    def Recovery_etapa3(self):
        NewPas_recovery_text = NewPas_entry_recovery.get_text()

        if NewPas_recovery_text:
            if any(NewPas_recovery_text == a["password"] for a in contas):
                DesligarBotao(ConfirmNewPas_btn_recovery, True, "This is your current password!")
                GLib.timeout_add(1000, lambda: DesligarBotao(ConfirmNewPas_btn_recovery, False, "Set as new password"))
            else:
                for a in contas:
                    if a["email"] == Email_recovery_text:
                        a["password"] = NewPas_recovery_text

                janela_recovery.set_visible(False)
                janela_recovery_sucess.set_visible(True)
        else:
            DesligarBotao(ConfirmNewPas_btn_recovery, True, "The field are required.")
            GLib.timeout_add(1000, lambda: DesligarBotao(ConfirmNewPas_btn_recovery, False, "Send recovery code"))



    # SIGNUP
    
    def LoginClicado(self):
        janela_signup.set_visible(False)
        janela_login.set_visible(True)

    def ContinueClicado_signup(self):

        Name_texto = " ".join((Name_entry_signup.get_text()).split())
        Username_texto = " ".join((Username_entry_signup.get_text()).split())
        Email_texto = " ".join((Email_entry_signup.get_text()).split())
        Password_texto = Password_entry_signup.get_text()
        ConfirmPassword_texto = " ".join((ConfirmPassword_entry_signup.get_text()).split())

        things = [Name_texto, Username_texto, Email_texto, Password_texto, ConfirmPassword_texto]
        

        if all(things):
            if not re.fullmatch(r'[a-zA-Z0-9._+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', Email_texto) or re.search(r'[^a-zA-Z0-9_.-]', Username_texto) or re.search(r'[^a-zA-Z0-9_.\- ]', Name_texto):
                DesligarBotao(Continue_btn_signup, True, "Special characters are not allowed.")
                GLib.timeout_add(1000, lambda: DesligarBotao(Continue_btn_signup, False, "Continue"))
            else:
                if not any((a["username"] == Username_texto or a["email"] == Email_texto) for a in contas):
                    if ConfirmPassword_texto != Password_texto:
                        DesligarBotao(Continue_btn_signup, True, "The passwords don't match.")
                        GLib.timeout_add(1000, lambda: DesligarBotao(Continue_btn_signup, False, "Continue"))
                    else:
                        contas.append({
                            "name": Name_texto,
                            "username": Username_texto.lower(),
                            "email": Email_texto.lower(),
                            "password": Password_texto
                        })

                        try:
                            with open(FILE, "w") as arquivo:
                                json.dump(contas, arquivo, indent=4)
                        except Exception as e:
                            print(f"Erro fatal: {e}")
                            Gtk.main_quit()

                        janela_signup.set_visible(False)
                        janela_sucess.set_visible(True)
                else:
                    DesligarBotao(Continue_btn_signup, True, "This account already exists.")
                    GLib.timeout_add(1000, lambda: DesligarBotao(Continue_btn_signup, False, "Continue"))
        else:
            DesligarBotao(Continue_btn_signup, True, "All fields are required.")
            GLib.timeout_add(1000, lambda: DesligarBotao(Continue_btn_signup, False, "Continue"))
    
    def EyeClicado_signup(self, state):
        if state == 1:
            Password_entry_signup.set_visibility(True)
            ConfirmPassword_entry_signup.set_visibility(True)
        else:
            Password_entry_signup.set_visibility(False)
            ConfirmPassword_entry_signup.set_visibility(False)

    # SUCESS

    def LoginClicado_sucess(self):
        janela_sucess.set_visible(False)
        janela_main.set_visible(True)
    
    def LeaveClicado_sucess(self):
        Gtk.main_quit()

    # MAIN


    def TipoMail_main(self):
        Mail_mode = MailMode_combo_main.get_active_id()
        if Mail_mode == "m":
            Port_sep_main.set_visible(True)
            FirstOne_label_main.set_text("Sender name:")
            SecondOne_label_main.set_text("Sender e-mail:")
            
        elif Mail_mode == "g":
            Port_sep_main.set_visible(False)
            FirstOne_label_main.set_text("Sender e-mail:")
            SecondOne_label_main.set_text("Sender password:")

    def SendMsgClicado_main(self):

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
                SendMailerSender.receber_valores(
                    SecondEntry_text_main,
                    FirstEntry_text_main,
                    ReceiverEmail_text_main,
                    Title_text_main,
                    Content_text_main,
                    ThirdEntry_text_main
                )
            elif Mail_mode == "g":
                SendSmtplibGmail.receber_valores(
                    FirstEntry_text_main,
                    SecondEntry_text_main,
                    ReceiverEmail_text_main,
                    Title_text_main,
                    Content_text_main,
                    False
                )

            if ErroAoEnviarEmail:
                print(ErroAoEnviarEmail)
                DesligarBotao(SendMsg_btn_main, True, "Something unexpected happened.")
                GLib.timeout_add(1000, lambda: DesligarBotao(SendMsg_btn_main, False, "Send message"))
            else:
                DesligarBotao(SendMsg_btn_main, True, "Sucess! (10s)")
                
                def IniciarCooldown():
                    cooldown = 10

                    def atualizar():
                        nonlocal cooldown
                        cooldown -= 1
                        SendMsg_btn_main.set_label(f"Success! ({cooldown}s)")

                        if cooldown <= 0:
                            DesligarBotao(SendMsg_btn_main, False, "Send Message")
                            return False

                        return True
                    
                    GLib.timeout_add(1000, atualizar)
                
                IniciarCooldown()

        else:
            DesligarBotao(SendMsg_btn_main, True, "All the fields are required.")
            GLib.timeout_add(1000, lambda: DesligarBotao(SendMsg_btn_main, False, "Send message"))





def main():

    
    # LOGIN

    Continue_btn_login.connect("clicked", Funcoes.ContinueClicado_login)
    SignUp_btn_login.connect("clicked", Funcoes.SignUpClicado)

    SwitchEmAnPas_btn_login.connect("clicked", Funcoes.EmailOuUsername)

    ShowOrHide_pas_login.connect("pressed", Funcoes.EyeClicado_login, 1)
    ShowOrHide_pas_login.connect("released", Funcoes.EyeClicado_login, 2)
    Password_entry_login.set_visibility(False)

    ForgotPas_btn_login.connect("clicked", Funcoes.ForgotPasClicado)


    # RECOVERY

    SendVerCod_btn_recovery.connect("clicked", Funcoes.Recovery_etapa1)
    VerCode_btn_recovery.connect("clicked", Funcoes.Recovery_etapa2)
    SendCodeAg_btn_recovery.connect("clicked", Funcoes.Recovery_etapa2_mandardnv)
    ConfirmNewPas_btn_recovery.connect("clicked", Funcoes.Recovery_etapa3)


    # SIGNUP

    Continue_btn_signup.connect("clicked", Funcoes.ContinueClicado_signup)
    Login_btn_signup.connect("clicked", Funcoes.LoginClicado)


    ShowOrHide_pas_signup.connect("pressed", Funcoes.EyeClicado_signup, 1)
    ShowOrHide_pas_signup.connect("released", Funcoes.EyeClicado_signup, 2)

    ConfirmPassword_entry_signup.set_visibility(False)
    Password_entry_signup.set_visibility(False)

    # SUCESS

    Login_acc_sucess.connect("clicked", Funcoes.LoginClicado_sucess)
    Leave_sucess.connect("clicked", Funcoes.LeaveClicado_sucess)

    # MAIN

    SendMsg_btn_main.connect("clicked", Funcoes.SendMsgClicado_main)
    MailMode_combo_main.connect("changed", Funcoes.TipoMail_main)
    OpenMenu_btn_main.connect("clicked", lambda btn: AlterarMenu(True))
    CloseMenu_btn_main.connect("clicked", lambda btn: AlterarMenu(False))
    SendEmail_btn_menu_main.connect("clicked", lambda btn: MudarModo_main(1))
    Inbox_btn_menu_main.connect("clicked", lambda btn: MudarModo_main(2))
    Preferences_btn_menu_main.connect("clicked", lambda btn: MudarModo_main(3))
    Settings_btn_menu_main.connect("clicked", lambda btn: MudarModo_main(4))


    #-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

    # STYLING

    MudarTema(janela_login, "dark")
    MudarTema(janela_signup, "dark")
    MudarTema(janela_main, "dark")
    MudarTema(janela_recovery, "dark")
    MudarTema(janela_recovery_sucess, "dark")
    MudarTema(janela_sucess, "dark")
    MudarTema(Menu_box_main, "dark")

    #-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

    janela_login.set_visible(True)
    Gtk.main()

if __name__ == "__main__":
    main()
