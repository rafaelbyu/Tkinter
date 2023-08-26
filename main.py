from tkinter import *
import cv2
from PIL import Image, ImageTk


class VideoPlayer:
    def __init__(self, video_source):
        self.video_source = video_source
        self.cap = cv2.VideoCapture(self.video_source)
        self.root = Tk()
        self.root.title("Изображения")
        self.is_playing = False

        self.f_left = LabelFrame(self.root, text="До")
        self.f_left.pack(side=LEFT, padx=10, pady=10)
        self.f_left_label = Label(self.f_left, text="изображение1")
        self.f_left_label.pack()

        self.f_right = LabelFrame(self.root, text="После")
        self.f_right.pack(side=RIGHT, padx=10, pady=10)
        self.f_right_label = Label(self.f_right, text="изображение2")
        self.f_right_label.pack()

        self.start_btn = Button(self.f_left, text="Start", command=self.start)
        self.start_btn.pack(padx=10, pady=10)

        self.stop_btn = Button(self.f_right, text="Stop", command=self.stop)
        self.stop_btn.pack(padx=10, pady=10)

    def play_video(self):
        while self.is_playing:
            ret, frame = self.cap.read()
            scale_percent = 30  # )percent of original size
            width = int(frame.shape[1] * scale_percent / 100)
            height = int(frame.shape[0] * scale_percent / 100)
            dim = (width, height)
            frame = cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)
            # cv2.imshow("frame", frame)
            # cv2.waitKey(1)

            frame1 = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image1 = Image.fromarray(frame1)
            photo1 = ImageTk.PhotoImage(image1)
            self.f_left_label.config(image=photo1)
            self.f_left_label.image = photo1
            self.f_left_label.update()

            frame2 = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            image2 = Image.fromarray(frame2)
            photo2 = ImageTk.PhotoImage(image2)
            self.f_right_label.config(image=photo2)
            self.f_right_label.image = photo2
            self.f_right_label.update()

    def start(self):
        self.is_playing = True
        self.play_video()
        self.root.mainloop()

    def stop(self):
        self.is_playing = False


player = VideoPlayer("assets/GoogleChrom.mp4")
player.start()
