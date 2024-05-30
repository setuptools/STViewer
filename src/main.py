from kivymd.app import MDApp
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.label import MDLabel , MDIcon
from kivymd.uix.behaviors.focus_behavior import FocusBehavior
from kivymd.uix.behaviors import HoverBehavior
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.slider import MDSlider , MDSliderHandle , MDSliderValueLabel

from kivy.uix.image import Image
from kivy.uix.video import Video
from kivy.core.window import Window
from kivy.uix.behaviors import ButtonBehavior
from kivy.clock import Clock
from kivy.properties import (
    ListProperty,
    StringProperty
)
from kivy.animation import Animation



import sys
import os
import pyperclip
import win32clipboard

from io import BytesIO
from PIL import Image as Imger

os.environ["KIVY_VIDEO"] = "ffpyplayer"

material = sys.argv#change it to sys.argv if you want tot compile app else ["", "path_to_your_file" ] (Don't / use \\)

class ButtonControl(MDFloatLayout , FocusBehavior  ,ButtonBehavior):
    icon = StringProperty("window-close")
    focus_color = ListProperty([0.6,0.6,0.6,0.3])
    unfocus_color = ListProperty([0,0,0,0])

    def __init__(self, *args, **kwargs):
        super(ButtonControl , self).__init__(*args, **kwargs)
        self.draggable = False
        self.md_bg_color = [0,0,0,0]

        self._icon = MDIcon(icon = self.icon , 
                            size_hint = [1,1], 
                            pos_hint = {"center_x":.5 , "center_y":.5},
                            theme_icon_color = "Custom",
                            icon_color = [1,1,1,1])
        
        self.on_enter = self.focusing_self
        self.on_leave = self.unfocusing_self

        Window.bind(on_cursor_enter = self.focusing_self)
        Window.bind(on_cursor_leave = self.unfocusing_self)

        self.add_widget(self._icon)

    def on_touch_down(self , touch):
        if self.collide_point(*touch.pos) and touch.button == "left":
            self.callback(touch)

    def focusing_self(self , *args):
        if self.collide_point(*Window.mouse_pos):
            Animation.cancel_all(self , "md_bg_color")
            self.md_bg_color = self.focus_color

    def unfocusing_self(self , *args):
        Animation.cancel_all(self , "md_bg_color")

        anim = Animation(md_bg_color = self.unfocus_color , d = 0.025)
        anim.start(self)

    def callback(self , *args):
        ...

class ControllButtons(MDFloatLayout, HoverBehavior):
    def __init__(self , *args , **kwargs):
        super(ControllButtons , self).__init__(*args , **kwargs)
        self.size_hint = [1, None]
        self.size = (Window.size[0] , 30)
        self.pos = (0, Window.size[1]-self.size[1])
        self.size_hint = [1 , None]
        self.pos_hint = {"center_x":.5}
        self.md_bg_color = [0,0,0,0.5]
        self.full_size = False
        self.prev_size= None

        Window.bind(size = self._adjusting)

        self._title = MDLabel(text = Window.title,
                            size_hint= [None, None],
                            font_size = self.size[1]/2.25,
                            valign = "bottom",
                            theme_text_color = "Custom",
                            theme_font_size = "Custom",
                            text_color = [1,1,1,1],
                            pos_hint= {"center_y":.5}
                            )
        self._title.pos= (5, 0)

        self.add_widget(self._title)
        self.buttons_controll_layout = MDGridLayout(cols = 3 , 
                                                    rows = 1, 
                                                    size_hint = [None , 1], 
                                                    md_bg_color = [1,1,1,0],
                                                    size = (100,0), 
                                                    pos_hint = {'center_y':.5},
                                                    orientation = "rl-tb")
        self.buttons_controll_layout.pos = (Window.size[0]-self.buttons_controll_layout.size[0], 0)

        self.exit_button = ButtonControl(focus_color = [.82,0,.28,1])
        self.exit_button.callback = lambda x: x == sys.exit(0)
        self.buttons_controll_layout.add_widget(self.exit_button)

        self.maximize_button = ButtonControl(icon = "dock-window")
        self.maximize_button.callback = lambda x: x == Window.maximize()
        self.buttons_controll_layout.add_widget(self.maximize_button)

        self.minimize_button = ButtonControl(icon = "window-minimize")
        self.minimize_button.callback = lambda x: x == Window.minimize()
        self.buttons_controll_layout.add_widget(self.minimize_button)

        self.add_widget(self.buttons_controll_layout)
    
        self.bind(pos = self._adjusting)
    def _adjusting(self , *args):
        self.pos = (0, Window.size[1]-self.size[1])
        self.buttons_controll_layout.pos = (Window.size[0]-self.buttons_controll_layout.size[0], 0)      

    def collider(self):

        return self.collide_point(*Window.mouse_pos)

class FloatFocusBehavior(MDFloatLayout , FocusBehavior):
    ...

class SceneWorkSpace(MDFloatLayout, FocusBehavior):
    def __init__(self, *args, **kwargs):
        super(SceneWorkSpace , self).__init__(*args, **kwargs)
        Window.bind(size = self._adjusting)
        self.hidded = False

        self.size_hint = [1,0.125]
        self.md_bg_color = [0,0,0,0.5]
        self.pos= (0 , 0 )

        Window.bind(on_cursor_enter = self.show,
                    on_cursor_leave = self.hide)
        
        self.on_enter = self.show
        self.on_leave = self.hide

        Clock.schedule_once(self.hide , 3)

        self.bind(pos = self._adjusting , size= self._adjusting)

    def show(self, *args):
        if self.collide_point(*Window.mouse_pos) and self.hidded == False: 
            Animation.cancel_all(self, "opacity")

            anim = Animation(opacity = 1 , d = 0.25)
            anim.start(self)
    
    def hide(self, *args):
        if self.hidded == False:
            Animation.cancel_all(self, "opacity")

            anim = Animation(opacity = 0 , d =0.25)
            anim.start(self)

    def _adjusting(self , *args):
        self.pos = (0,self.parent.parent.parent.children[0].pos[1]-self.size[1]+0.5)

class BufferMessage(MDFloatLayout):
    text = StringProperty()

    def __init__(self,buffer = None, *args , **kwargs):
        super(BufferMessage, self).__init__(*args , **kwargs)
        
        self.buffer = buffer

        self.size_hint = [1 , None]
        self.size[1] = self.buffer.size[1]/8
        self.pos_hint = {'center_x':-2}
        self.radius = 10
        self.md_bg_color = [.2,.2,.2,0.5]

        self._text = MDLabel(text = self.text,
                            theme_text_color= "Custom",
                            text_color = [1,1,1,1],
                            theme_font_size = "Custom",
                            halign = "center",
                            font_size = self.size[1]/4.5,
                            size_hint = [1 , None],
                            pos_hint = {"center_x":.5 , "center_y":.5})
        self.add_widget(self._text)

        if len(self.buffer.children) >= 8:
            self.buffer.remove_widget(self.buffer.children[-1])

        self.buffer.add_widget(self)

        anim = Animation(pos_hint = {"center_x":.5}, d = 0.25)
        anim.start(self)
        anim.on_complete = lambda x:x == Clock.schedule_once(self.remove, 1.5)
    
    def remove(self, *args):
        try:
            anim = Animation(opacity = 0 , d = 0.25)
            anim.start(self)
            anim.on_complete = lambda y:y == self.buffer.remove_widget(self)
        except Exception as a:
            print(a)
    
    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos) and touch.button == "left":
            Clock.schedule_once(self.remove, 0)

class Scene(MDFloatLayout):    
    def __init__(self,main = None, *args, **kwargs):
        super(Scene , self).__init__(*args , **kwargs)

        Window.bind(size = self._adjusting)
        Window.bind(on_keyboard = self.keybinding)

        Window.bind(on_drop_file = lambda x , *args: x == print(1))

        self.m = main
        self.size_hint = [1,1]
        self.pos_hint = {"center_x":.5,'cemter_y':.5}
        self.up_scroll_up , self.down_scroll_up = 10,10

        if len(material) > 1:
            # loading material
            if material[1].split("\\")[-1].endswith((".png",".jpg",".jpeg",".ico",".gif")):
                Window.bind(on_cursor_leave = self.hide_title)
                Window.bind(on_cursor_enter = self.show_title)

                image = Imger.open(material[1])
                self.scene_image = Image(
                            source = material[1],
                            size_hint = [1,1],
                            anim_delay = 0.075,
                            pos_hint = {"center_x":.5,"center_y":.5},
                            keep_ratio = False,
                            fit_mode = "contain"
                            )   
                self.up_scroll_up , self.down_scroll_up = 1.25 , 1.25

                self.scene = MDFloatLayout(size_hint = [None , None], size = image.size, md_bg_color = [1,1,1,0])
                self.scene.add_widget(self.scene_image)

                self.scene.pos = (Window.size[0]/2-self.scene.size[0]/2 ,Window.size[1]/2-self.scene.size[1]/2)
                self.scene.bind(size = self._adjusting, pos = self._adjusting)
                self.scene.on_touch_down = self.sizing
        
                self.add_widget(self.scene)

                self.file_background = FloatFocusBehavior(md_bg_color = [0,0,0,.5], size_hint = [1,None])
                self.file_background.size = (0 , Window.size[1]/14)
                self.file_background.pos = (0,0)

                self.file_background.on_enter = self.show_title
                self.file_background.on_leave = self.hide_title

                # file naming
                self.file_name = MDLabel(text = f"{os.path.basename(material[1])[0:30]}",
                                    size_hint = [None , None],
                                    halign = "left" , 
                                    font_size = self.file_background.size[1]/3,
                                    text_color = [1,1,1,1],
                                    theme_text_color = "Custom",
                                    theme_font_size = "Custom",
                                    pos_hint = {"center_y":.5})
                
                self.file_name.pos = (10 ,0)
                self.file_background.add_widget(self.file_name)

                # opening file path as button
                self.open_file_folder = MDIcon(icon ="folder-open",
                                            size_hint = [None , None],
                                            theme_icon_color= "Custom",
                                            icon_color = [1,1,1,1],
                                            pos_hint = {'center_y':.5})
                self.open_file_folder.size = (self.file_background.size[1]/1.5,self.file_background.size[1]/1.5)
                self.open_file_folder.pos = (Window.size[0]-self.open_file_folder.size[0]-10, 0)
                self.open_file_folder.on_touch_down = lambda x, *args: x == os.system(f"start {str(material[1].split(self.file_name.text)[0])}") if x.button == "left" and self.open_file_folder.collide_point(*x.pos) and self.open_file_folder.opacity != 0 else None

                self.file_background.add_widget(self.open_file_folder)

                self.add_widget(self.file_background)
                Clock.schedule_once(self.hide_title , 3) 
            

            if material[1].split("\\")[-1].endswith((".mp4",".mov", ".avi")):
                self.scene = Video(source = material[1],
                                   size_hint = [1,1],
                                   allow_stretch = True,
                                   pos_hint = {'center_x':.5 , "center_y":.5},
                                   state = "play",
                                   volume = 0.1
                                   )
                self.buttons = PlayerButtons(scene = self)
                self.add_widget(self.scene)
                self.add_widget(self.buttons)
        
            self.work_space = SceneWorkSpace(opacity = 0)
            self.add_widget(self.work_space)

            if isinstance(self.scene , Video):
                self.work_space.opacity = 0 
                self.work_space.hidded =True
                self.work_space.disabled= True

            self.buffer_pos_adding = 0

            if hasattr(self , "file_background"):
                self.buffer_pos_adding += self.file_background.size[1]
            
            if hasattr(self , "buttons"):
                self.buffer_pos_adding += self.buttons.size[1]*2

            self.buffer_messager = MDBoxLayout(size_hint = [None , None],orientation = "vertical",spacing = 5,
                                    md_bg_color = [1,1,1,0],)

            self.buffer_messager.pos = (0 ,0+self.buffer_pos_adding+10)
            self.buffer_messager.size = (150, Window.size[1]-self.work_space.size[1]*2)
            self.add_widget(self.buffer_messager)
    # binding
    def keybinding(self , window , keycode , poimt , key , addition):
        if key == "c" and addition != [] and addition[0] == "ctrl":
            if self.scene.collide_point(*Window.mouse_pos) and not isinstance(self.scene , Video):
                image =Imger.open(material[1])
                output = BytesIO()
                image.convert('RGBA').save(output, 'BMP')
                data = output.getvalue()[14:]
                output.close()

                win32clipboard.OpenClipboard()
                win32clipboard.EmptyClipboard()
                win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
                win32clipboard.CloseClipboard()
                BufferMessage(buffer = self.buffer_messager, text = "Картинка успешно скопирована")
            
            if isinstance(self.scene , Video) == False:
                if self.file_name.collide_point(*Window.mouse_pos) and self.file_name.opacity !=0:
                    BufferMessage(buffer = self.buffer_messager, text = "Имя файла успешно скопирован")
                    pyperclip.copy(os.path.basename(material[1]))
                
                if self.open_file_folder.collide_point(*Window.mouse_pos) and self.open_file_folder.opacity !=0:
                    BufferMessage(buffer = self.buffer_messager, text = "Путь успешно скопирован")
                    pyperclip.copy(material[1])

    def hide_title(self, *args):
        Animation.cancel_all(self.file_background , "md_bg_color")
        anim = Animation(opacity = 0 , d = 0.25)
        anim.start(self.file_background)
    
    def show_title(self, *args):
        if self.file_background.collide_point(*Window.mouse_pos):
            Animation.cancel_all(self.file_background , "md_bg_color")
            anim = Animation(opacity = 1, d = 0.25)
            anim.start(self.file_background)

    def _adjusting(self , *args):
        try:
            self.scene.pos = (Window.size[0]/2-self.scene.size[0]/2 ,Window.size[1]/2-self.scene.size[1]/2)
            self.file_background.size = (0 , Window.size[1]/14)
            self.file_name.font_size = self.file_background.size[1]/3

            self.open_file_folder.size = (self.file_background.size[1]/1.5,self.file_background.size[1]/1.5)
            self.open_file_folder.font_size = self.file_background.size[1]/1.5
            self.open_file_folder.pos = (Window.size[0]-self.open_file_folder.size[0]-10, 0)

            self.buffer_pos_adding = 0

            if hasattr(self , "buttons"):
                self.buffer_pos_adding += self.buttonsize[1]*2
                self.buffer_messager.pos[1] = self.buffer_pos_adding+10
            
            if hasattr(self , "file_background"):
                self.buffer_pos_adding += self.file_background.size[1]
                self.buffer_messager.pos[1] = self.buffer_pos_adding+10

        except Exception as a:
            pass
    
    def sizing(self , touch):
        if touch.is_mouse_scrolling:
            if touch.button == "scrolldown" and (self.scene.size[0] < self.size[0]*3 or self.scene.size[1] < self.size[1])*3:
                self.scene.size = (self.scene.size[0]*self.up_scroll_up , self.scene.size[1]*self.up_scroll_up)

            elif touch.button == "scrollup" and (self.scene.size[0] > 100 and self.scene.size[1] > 100):
                self.scene.size = (self.scene.size[0]/self.down_scroll_up , self.scene.size[1]/self.down_scroll_up)
            
            elif touch.button == "scrollup" and (self.scene.size[0] >= self.size[0]*3 or self.scene.size[1] >= self.size[1]*3):
                self.scene.size = (self.scene.size[0]/self.down_scroll_up , self.scene.size[1]/self.down_scroll_up)

class PlayerButtons(MDFloatLayout):
    def __init__(self,scene: Scene , *args, **kwargs):
        super(PlayerButtons , self).__init__(*args, **kwargs)

        Window.bind(mouse_pos = self.show_all)
        Window.bind(size = self._adjusting)
        Window.bind(on_key_down = self.keybinds)
        Window.bind(on_cursor_enter = self.show_all)

        self.scene = scene

        self.size_hint = [1 , None]
        self.size = (0, Window.size[1]/16)
        self.pos = (0,0)
        self.md_bg_color = [1,1,1,0.3]

        self.timer = 0
        self.stop_checking= False
        self.mouse_pos = None
        self.interaction = False

        self.volume_saver = 0
        self.state_saver = None

        # widgets
        self.video_slider = MDSlider(MDSliderHandle(radius = 10 , state_layer_size = (0,0), size = (10,10)) , 
                              size_hint = [None, None], 
                              pos_hint = {'center_x':.5, "center_y":1},
                              max = self.scene.scene.duration,
                              padding = 20,
                              border_vertical = [0,0,0,0],
                              min = 0,
                              step_point_size = 0,
                              step = 0,
                              size = (Window.size[0],10))
        self.video_slider.bind(on_touch_up = self.moveVideo,
                               on_touch_down = self.moveVideoDown)
        self.scene.scene.volume = 0.1
        self.volume_saver = self.scene.scene.volume
        self.add_widget(self.video_slider)


        self.title_video = MDLabel(text =  os.path.basename(material[1])[0:30],
                                   font_size= self.size[1]/2,
                                   theme_font_size = "Custom",
                                   theme_text_color ="Custom",
                                   text_color = [1,1,1,1],
                                   pos = (self.video_slider.padding, self.size[1]+40))
        self.add_widget(self.title_video)

        # pausing
        self.pause_button = MDIcon(pos = (self.video_slider.padding, 0),
                                   pos_hint = {'center_y':.5},
                                   theme_font_size = "Custom",
                                   theme_icon_color = "Custom",
                                   icon = "pause",
                                   icon_color = [1,1,1,1],
                                   font_size = self.size[1]/1.5)

                            
        self.pause_button.on_touch_down = lambda touch: self.pauseUnpauseVideo(touch) if self.pause_button.collide_point(*Window.mouse_pos) and touch.button == "left" else None
        self.add_widget(self.pause_button)

        # voluming
        self.volume = MDIcon(pos = (self.pause_button.pos[0]*2+10 , 0),
                            pos_hint = {"center_y":.5},
                            theme_font_size = "Custom",
                            theme_icon_color= "Custom",
                            icon = "volume-low",
                            icon_color = [1,1,1,1],
                            font_size = self.size[1]/1.5)
        self.volume.on_enter = self.addVolumeMaster
        self.volume.on_leave = self.removeVolumeMaster
        self.volume.on_touch_down = self.onOffVolume

        self.add_widget(self.volume)

        self.volume_master = FloatFocusBehavior(size_hint = [None ,None],
                                         size = (self.volume.size[0]*3 , self.volume.size[1]),
                                         pos = (self.volume.pos[0]+self.volume.size[0], 0),   
                                         pos_hint = {"center_y":.5},
                                         md_bg_color = [0,0,0,0])
        self.volume_master.on_leave = lambda: self.remove_widget(self.volume_master) if self.volume.collide_point(*Window.mouse_pos) == False else None
        self.volume_slider = MDSlider(MDSliderHandle(radius = 10 , state_layer_size = (0,0), size = (10,10)) , 
                              size_hint = [1,0.25], 
                              pos_hint = {'center_x':.35, "center_y":.5},
                              max = 100,
                              padding = 20,
                              border_vertical = [0,0,0,0],
                              min = 0,
                              step_point_size = 0,
                              step = 0)
        self.volume_slider.bind(on_touch_move = lambda x , *args:x == (
                                                                    setattr(self.scene.scene , "volume", self.volume_slider.value/100),
                                                                    setattr(self, "volume_saver" , self.volume_slider.value/100),
                                                                    Clock.schedule_once(self.setVolumeIcons ,0)) if self.volume_master.collide_point(*Window.mouse_pos) else None,
                                on_touch_down = lambda y , touch:y == (
                                                                    setattr(self.scene.scene , "volume", self.volume_slider.value/100),
                                                                    setattr(self, "volume_saver" , self.volume_slider.value/100),
                                                                    Clock.schedule_once(self.setVolumeIcons ,0)) if self.volume_master.collide_point(*Window.mouse_pos) and touch.is_mouse_scrolling else None)
        self.volume_master.add_widget(self.volume_slider)

        # video duration label
        self.video_now = "00:00"
        self.video_all = "00:00"

        self.video_durater = MDLabel(text = f"{self.video_now}/{self.video_all}",
                                     theme_font_size = "Custom",
                                     theme_text_color = "Custom",
                                     font_size = self.size[1]/3,
                                     text_color = [1,1,1,1],
                                     valign = "bottom",
                                     size_hint = [.5 , 1],
                                     pos_hint= {'center_y':.45},
                                     )
        self.add_widget(self.video_durater)
        # clocks
        Clock.schedule_interval(self.mouse_check , 1)
        Clock.schedule_interval(self._adjusting , 0)
        Clock.schedule_interval(self.checkVideo , 0)

        self.bind(pos = self._adjusting , size= self._adjusting)

        self.video_updating = Clock.schedule_interval(self.update_video , 0)
        self.video_durator_clock = Clock.schedule_interval(self.setVideoDurater , 0)
    
    def setVolumeIcons(self , *args):
        if self.scene.scene.volume <= 0.0:
            self.volume.icon = "volume-variant-off"
                        
        elif self.scene.scene.volume >= 0 and self.scene.scene.volume < 0.25:
            self.volume.icon = "volume-low"
                        
        elif self.scene.scene.volume >= 0.25 and self.scene.scene.volume < 0.6:
            self.volume.icon = "volume-medium"
                        
        elif self.scene.scene.volume >= 0.6:
            self.volume.icon = "volume-high"              

    def onOffVolume(self, touch):
        if self.volume.collide_point(*touch.pos) and touch.button == "left":
            if self.volume_slider.value != 0:
                self.scene.scene.volume = -0.01
                self.volume_slider.value = 0

                Clock.schedule_once(self.setVolumeIcons)
            
            else:
                self.scene.scene.volume = self.volume_saver
                self.volume_slider.value = self.volume_saver*100

                Clock.schedule_once(self.setVolumeIcons)
            
    def keybinds(self , window , keycode ,keypoint , key , adittion):

        if key == "c" and adittion != []:
            if adittion[0] == "ctrl":
                if self.title_video.collide_point(*Window.mouse_pos):
                    BufferMessage(self.scene.buffer_messager , text = "Имя файла успешно скопировано")
                    pyperclip.copy(os.path.basename(material[1]))
        
        elif key == " ":
            self.pauseUnpauseVideo(key)
            Clock.schedule_once(self.show_all , 0)

        if keycode == 273: # arrow-up
            if self.scene.scene.volume <= 1:
                self.scene.scene.volume += 0.125
                self.volume_saver = self.scene.scene.volume
                self.volume_slider.value = self.scene.scene.volume*100
                
                Clock.schedule_once(self.setVolumeIcons ,0)
                Clock.schedule_once(self.show_all , 0)
        
        elif keycode == 274: # arrow-down
            if self.scene.scene.volume >= 0:
                self.scene.scene.volume -= 0.125
                self.volume_saver = self.scene.scene.volume
                self.volume_slider.value = self.scene.scene.volume*100

                Clock.schedule_once(self.setVolumeIcons ,0)
                Clock.schedule_once(self.show_all , 0)
        
        elif keycode == 275: # arrow-right
            Animation.cancel_all(self.video_slider , "value")
            
            self.state_saver = self.scene.scene.state
            self.scene.scene.state = "pause"
            self.scene.scene.position = self.scene.scene.position + 5


            if self.scene.scene.position < self.scene.scene.duration:
                self.scene.scene.seek(self.scene.scene.position/self.scene.scene.duration)
                
                self.video_slider.value_normalized = self.scene.scene.position/self.scene.scene.duration
            
            else:
                self.scene.scene.seek(0)
                self.video_slider.value_normalized = 0
            
            self.scene.scene.state =self.state_saver

            if self.scene.scene.state not in ["stop","pause"]:
                self.scene.scene.state = "play"
                self.video_updating = Clock.schedule_once(self.update_video , 0)
            
        
        elif keycode == 276: # arrow-left
            Animation.cancel_all(self.video_slider , "value")
            
            self.state_saver = self.scene.scene.state
            self.scene.scene.state = "pause"
            self.scene.scene.position = self.scene.scene.position - 5

            print(self.scene.scene.position)
            if self.scene.scene.position > 0:
                self.scene.scene.seek(self.scene.scene.position/self.scene.scene.duration)

                self.video_slider.value_normalized = self.scene.scene.position/self.scene.scene.duration

            else:
                self.scene.scene.seek(1)
                
                self.video_slider.value_normalized = 1
            
            self.scene.scene.state =self.state_saver

            if self.scene.scene.state not in ["stop","pause"]:
                self.scene.scene.state = "play"
                self.video_updating = Clock.schedule_once(self.update_video , 0)
            
            self.scene.scene.volume = self.volume_saver

    def pauseUnpauseVideo(self, *args):
        if self.scene.scene.state == "play":

            self.scene.scene.state = "pause"
            self.pause_button.icon = "play"
            Animation.cancel_all(self.video_slider , "value")

        elif self.scene.scene.state == "pause": 
            self.scene.scene.volume = self.volume_saver     
            self.scene.scene.state = "play"
            self.pause_button.icon = "pause"

            self.video_updating = Clock.schedule_interval(self.update_video , 0)

        elif self.scene.scene.state == "stop":
            self.scene.scene.seek(0)
            self.video_slider.value = 0
            self.scene.scene.state = "play"
            self.pause_button.icon = "pause"

            self.video_updating = Clock.schedule_once(self.update_video , 0)
    # video duraccel
    def setVideoDurater(self , *args):
        if self.scene.scene.loaded:
            if self.scene.scene.duration <= 3600:
                minutes, reminder = divmod(int(self.scene.scene.duration), 60)
                self.video_all = f"{'0' if len(str(minutes)) <= 1 else ''}{minutes}:{'0' if len(str(reminder)) <= 1 else ''}{reminder}"
                
                min_pos , rem_pos = divmod(int(self.scene.scene.position), 60)
                self.video_now = f"{'0' if len(str(min_pos)) <= 1 else ''}{min_pos}:{'0' if len(str(rem_pos)) <= 1 else ''}{rem_pos}"

                self.video_durater.text = f"{self.video_now}/{self.video_all}"

    # voluem master
    def addVolumeMaster(self ,*args):
        self.volume_master.size = (self.volume.size[0]*3 , self.volume.size[1]) 
        self.volume_master.pos = (self.volume.pos[0]+self.volume.size[0], 0)  

        if self.volume_master not in self.children:  
            self.add_widget(self.volume_master)
    
    def removeVolumeMaster(self , *args):
        if not self.volume_master.collide_point(*Window.mouse_pos):
            self.remove_widget(self.volume_master)

    # move video
    def moveVideoDown(self,  *touch):
        if self.video_slider.collide_point(*touch[1].pos)  and touch[1].button == "left":
            Animation.cancel_all(self.video_slider , "value")
            self.interaction = True

    def moveVideo(self,*touch):
        if self.interaction and touch[1].button == "left":
            
            self.interaction = False
            self.scene.scene.seek(self.video_slider.value/self.scene.scene.duration)
            self.video_slider.value_normalized = self.video_slider.value/self.scene.scene.duration

            if self.scene.scene.state == "stop":
                self.scene.scene.state = "play"
                self.scene.scene.state = "pause"
                self.scene.scene.seek(self.video_slider.value/self.scene.scene.duration)
                self.pause_button.icon = "play"
                return None

            elif self.scene.scene.state == "pause":
                self.scene.scene.volume = 0
                return None

            self.video_updating = Clock.schedule_once(self.update_video , 0)

    # updating video
    def update_video(self, *args):
        if self.scene.scene.loaded:
            Clock.unschedule(self.video_updating)

            anim = Animation(value = self.video_slider.max , d = self.scene.scene.duration-self.video_slider.value)
            anim.start(self.video_slider)


    def checkVideo(self, *args):
        if self.scene.scene.eos:
            self.pause_button.icon = "play"

    
    # check mosue staying
    def mouse_check(self , *args):
        if self.stop_checking == False and self.scene.scene.state == "play":
            if self.timer == 2:
                Clock.schedule_once(self.hide_all , 0)
                self.stop_checking =True

            elif Window.mouse_pos == self.mouse_pos:
                self.timer +=1    
            self.mouse_pos = Window.mouse_pos

    def hide_all(self, *args):
        Window.show_cursor = False

        anim = Animation(opacity = 0, d = 0.25)
        anim.start(Window.children[0])
        anim.start(self)

    def show_all(self , *args):
        self.timer = 0
        self.stop_checking = False 
        Window.show_cursor = True  

        anim = Animation(opacity = 1, d = 0.1)
        anim.start(Window.children[0])   
        anim.start(self)   
    
    # adjust widgets
    def _adjusting(self,  *args):
        self.video_slider.size[0] = Window.size[0]
        self.video_slider.max = self.scene.scene.duration
        self.title_video.pos = (self.video_slider.padding, self.size[1])
        self.video_durater.pos[0] = self.volume.pos[0]+self.volume.size[0]+10 if self.volume_master not in self.children else self.volume.pos[0]+self.volume.size[0]+self.volume_master.size[0]-10

class MediaPlayer(MDApp):

    def build(self):
        self.title = "STViewer"
        self.icon = "icons/stv.ico"
        Window.title = self.title
        Clock.schedule_once(self.title_bar , -1)
        self.main = MDFloatLayout(size_hint = [1,1], 
                                  md_bg_color = [.13,.13,.13,1],
                                  pos_hint = {"center_x":.5,"center_y":.5})


        self.scene = Scene(main = self)
        self.main.add_widget(self.scene)

        return self.main

    def title_bar(self , *args):
        self.controller = ControllButtons()
        Window.parent.add_widget(self.controller)
        if Window.set_custom_titlebar(self.controller):
            return True

    def open_settings(self,  *args):
        ...

MediaPlayer().run()